//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

import {IERC721} from "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract Roulette is VRFConsumerBase {
    using Counters for Counters.Counter;

    // ======= VARIABLES ======
    Counters.Counter private gameIds;
    uint32 countdownTime = 7 days;
    address burnAddress = 0x0000000000000000000000000000000000000000;
    // CHAINLINK STUFF
    uint256 private constant ROLL_IN_PROGRESS = 42;
    bytes32 internal keyHash;
    uint256 internal fee;
    mapping(bytes32 => address) private s_rollers;
    mapping(address => uint256) private s_results;

    // ======= EVENTS =========

    event NewGameStarted(
        IERC721 token1,
        uint256 tokenId1,
        IERC721 token2,
        uint256 tokenId2,
        uint256 gameId
    );
    event ChallengeAccepted(uint256 gameId);
    event ChallengerRegretted(uint256 gameId);
    event PulledTrigger(IERC721 tokenContract, uint256 tokenId, uint256 gameId, bool survived);

    // ======= STRUCTS ========

    struct Game {
        address player1;
        IERC721 tokenAddress1;
        uint256 tokenId1;
        bool player1Survived;
        address player2;
        IERC721 tokenAddress2;
        uint256 tokenId2;
        bool player2Survived;
        GameState state;
        uint32 countdownTimer;
    }

    // ======== ENUMS ==========

    enum GameState {
        CHALLENGED,
        TURNOFPLAYER1,
        PLAYER1AWAITRESULT,
        TURNOFPLAYER2,
        PLAYER2AWAITRESULT,
        CANCELLED, 
        ENDED
    }

    // ======= MAPPINGS ========

    mapping(uint256 => Game) public games;

    // ======= CONSTRUCTOR =====
    /**
     * Constructor inherits VRFConsumerBase
     * 
     * Network: Kovan
     * Chainlink VRF Coordinator address: 0xdD3782915140c8f3b190B5D67eAc6dc5760C46E9
     * LINK token address:                0xa36085F69e2889c224210F603D836748e7dC0088
     * Key Hash: 0x6c3699283bda56ad74f6b855546325b68d482e983852a7a82979cc4807b641f4
     */
    constructor() 
        VRFConsumerBase(
            0xdD3782915140c8f3b190B5D67eAc6dc5760C46E9, // VRF Coordinator 
            0x01BE23585060835E02B77ef475b0Cc51aA1e0709  // LINK Token
        )
    {
        keyHash = 0x6c3699283bda56ad74f6b855546325b68d482e983852a7a82979cc4807b641f4;
        fee = 0.1 * 10 ** 18; // 0.1 LINK (Varies by network)
    }

    // ======== FUNCTIONS =======

    function onERC721Received(
        address operator,
        address from,
        uint256 tokenId,
        bytes memory data
    ) external returns (bytes4) {
        if (data.length == 32) {
            // Only receive gameID means that game has started
            uint256 gameId = abi.decode(data, (uint256));
            acceptChallenge(from, IERC721(msg.sender), tokenId, gameId);
        } else if (data.length == 52) {
            // Receive token address and token id if game didn't start
            (address _theirTokenAddress, uint256 _theirTokenId) = abi.decode(
                data,
                (address, uint256)
            );
            startGame(
                from,
                IERC721(msg.sender),
                tokenId,
                IERC721(_theirTokenAddress),
                _theirTokenId
            );
        } else {
            revert("Wrong input for data");
        }
        return 0x150b7a02;
    }

    function startGame(
        address player1Address,
        IERC721 ourTokenAddress,
        uint256 ourTokenId,
        IERC721 theirTokenAddress,
        uint256 theirTokenId
    ) internal {
        uint256 gameId = gameIds.current();
        games[gameId] = Game(
            player1Address,
            ourTokenAddress,
            ourTokenId,
            true,
            address(0),
            theirTokenAddress,
            theirTokenId,
            true,
            GameState.CHALLENGED,
            0
        );
        gameIds.increment();

        emit NewGameStarted(
            ourTokenAddress,
            ourTokenId,
            theirTokenAddress,
            theirTokenId,
            gameId
        );
    }

    function acceptChallenge(
        address player2Address,
        IERC721 tokenAddress,
        uint256 tokenId,
        uint256 gameId
    ) internal {
        Game storage game = games[gameId];
        require(game.state == GameState.CHALLENGED, "No challenge exists or challenge already accepted");
        require(game.tokenAddress2 == tokenAddress, "Not same token");
        require(game.tokenId2 == tokenId, "Not same token ID");
        game.player2 = player2Address;
        game.state = GameState.TURNOFPLAYER1;
        _triggerCooldown(game);
        emit ChallengeAccepted(gameId);
    }

    function pulltrigger(uint gameId) public returns (bytes32 requestId) {       
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK to pay fee");
        Game storage game = games[gameId];
        if (game.state == GameState.TURNOFPLAYER1) {
            require(msg.sender == game.player1);
            require(s_results[game.player1] == 0, "Already rolled");

            requestId = requestRandomness(keyHash, fee);
            s_rollers[requestId] = game.player1;
            s_results[game.player1] = ROLL_IN_PROGRESS;

            game.state = GameState.PLAYER1AWAITRESULT;
        } else if (game.state == GameState.TURNOFPLAYER2) {
            require(msg.sender == game.player2);
            require(s_results[game.player1] == 0, "Already rolled");

            requestId = requestRandomness(keyHash, fee);
            s_rollers[requestId] = game.player1;
            s_results[game.player1] = ROLL_IN_PROGRESS;

            game.state = GameState.PLAYER2AWAITRESULT;
        } else {
            revert("Function can't be called in current state");
        }
    }

    function didPlayerSurvive(uint256 gameId, uint256 playerId) public view returns (bool) {
        Game storage game = games[gameId];
        address player;
        if (playerId == 0) {
            player = game.player1;
        } else if (playerId == 1) {
            player = game.player2;
        } else {revert("Not a valid player ID");}

        require(s_results[player] != 42, "Randomness not yet received");
        uint256 rand = s_results[player];
        if (rand < 3) {
            return false;
        } else {
            return true;
        }     

    }

    function evaluateOutcome(uint gameId) public {
        Game storage game = games[gameId];
        if (game.state == GameState.PLAYER1AWAITRESULT) {
            require(msg.sender == game.player1);
            IERC721 tokenContract = game.tokenAddress1;
            if (!didPlayerSurvive(gameId, 0)) {
                game.player1Survived = false;
                game.player2Survived = true;
                tokenContract.safeTransferFrom(msg.sender, burnAddress, game.tokenId1);
                game.state = GameState.PLAYER2AWAITRESULT;
                // mintGravestone();
                emit PulledTrigger(game.tokenAddress1, game.tokenId1, gameId, false);
            } else {
                game.player1Survived = true;
                tokenContract.safeTransferFrom(msg.sender, game.player1, game.tokenId1);
                game.state = GameState.TURNOFPLAYER2;
                // mintReward();
                emit PulledTrigger(game.tokenAddress1, game.tokenId1, gameId, true);    
            }
        } else if (game.state == GameState.PLAYER2AWAITRESULT) {
            require(msg.sender == game.player2);
            IERC721 tokenContract = game.tokenAddress2;
            if (game.player2Survived || didPlayerSurvive(gameId, 1)) {
                tokenContract.safeTransferFrom(msg.sender, game.player2, game.tokenId2);
                game.state = GameState.ENDED;
                // mintReward();
                emit PulledTrigger(game.tokenAddress2, game.tokenId2, gameId, true);  
            } else {
                game.player2Survived = false;
                tokenContract.safeTransferFrom(msg.sender, burnAddress, game.tokenId2);
                game.state = GameState.ENDED;
                // mintGravestone();
                emit PulledTrigger(game.tokenAddress2, game.tokenId2, gameId, false);
            }
        }
    }

    function withdrawChallenge(uint gameId) public {
        Game storage game = games[gameId];
        require(game.player1 == msg.sender, "Only game initiator can withdraw challenge");
        require(game.state == GameState.CHALLENGED, "Challenge has already been accepted");
        IERC721 tokenContract = game.tokenAddress1;
        tokenContract.safeTransferFrom(msg.sender, game.player1, game.tokenId1);
        game.state = GameState.CANCELLED;
        emit ChallengerRegretted(gameId);
    }

    function chickenOut() public payable {}
        
    function _triggerCooldown(Game storage game) internal {
        game.countdownTimer = uint32(block.timestamp + countdownTime);
    }

    function _isCountdownOver(Game storage game) internal returns (bool) {
        return (game.countdownTimer < block.timestamp);
    }

    /** 
     * Requests randomness 
     */
    function getRandomNumber() public returns (bytes32 requestId) {
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK - fill contract with faucet");
        return requestRandomness(keyHash, fee);
    }

    /**
     * Callback function used by VRF Coordinator
     */
    function fulfillRandomness(bytes32 requestId, uint256 randomness) internal override {
        uint256 d6Value = randomness % 6;
        s_results[s_rollers[requestId]] = d6Value;
    }
    
}
