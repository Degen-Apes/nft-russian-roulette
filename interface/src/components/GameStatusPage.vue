<template>
  <div class="w-full max-w-screen-lg mx-auto">
    <h1 class="h1">Game {{ $route.params.gameID }}</h1>
    <div
      class="
        grid grid-cols-2
        items-center
        justify-items-center
        gap-6
        px-6
        mx-auto
      "
    >
      <h2 class="h2 text-center">Player 1</h2>
      <h2 class="h2 text-center">Player 2</h2>
      <NFT
        :contractAddress="player1TokenContractAddress"
        :tokenID="player1TokenID"
        :isDead="player1Survived === false"
      />
      <NFT
        :contractAddress="player2TokenContractAddress"
        :tokenID="player2TokenID"
        :isDead="player2Survived === false"
      />
      <PlayerStatus
        :playerIndex="1"
        :gameID="gameID"
        :state="player1State"
        :tokenContractAddress="player1TokenContractAddress"
        :tokenID="player1TokenID"
        :userIsPlayer="true"
      />
      <PlayerStatus
        :playerIndex="2"
        :gameID="gameID"
        :state="player2State"
        :tokenContractAddress="player2TokenContractAddress"
        :tokenID="player2TokenID"
        :userIsPlayer="true"
      />
    </div>

    <div v-if="!account" class="flex justify-center">
      <ConnectBtn @connected="onConnected" />
    </div>
  </div>
</template>

<script>
import { ethers } from "ethers";
import * as config from "../config.js";
import rouletteABI from "../assets/rouletteABI.json";
import PlayerStatus, { PLAYER_STATE } from "./PlayerStatus.vue";
import ConnectBtn from "./ConnectBtn.vue";
import NFT from "./NFT.vue";

export const GAME_STATE = {
  CHALLENGED: 0,
  TURN_OF_PLAYER1: 1,
  PLAYER1_AWAIT_RANDOMNESS: 2,
  TURN_OF_PLAYER2: 3,
  PLAYER2_AWAIT_RANDOMNESS: 4,
  CANCELLED: 5,
  ENDED: 6,
};

export default {
  name: "GameStatusPage",
  components: {
    PlayerStatus,
    ConnectBtn,
    NFT,
  },

  data() {
    return {
      account: null,
      gameID: null,
      signer: null,
      gameState: null,
      player1Survived: null,
      player2Survived: null,
    };
  },
  computed: {
    player1Address() {
      if (!this.gameState) {
        return null;
      }
      return this.gameState.player1;
    },
    player2Address() {
      if (!this.gameState) {
        return null;
      }
      return this.gameState.player2;
    },
    player1TokenContractAddress() {
      if (!this.gameState) {
        return null;
      }
      return this.gameState.tokenAddress1;
    },
    player2TokenContractAddress() {
      if (!this.gameState) {
        return null;
      }
      return this.gameState.tokenAddress2;
    },
    player1TokenID() {
      if (!this.gameState) {
        return null;
      }
      return this.gameState.tokenId1;
    },
    player2TokenID() {
      if (!this.gameState) {
        return null;
      }
      return this.gameState.tokenId2;
    },

    player1State() {
      if (!this.gameState) {
        return null;
      }
      switch (this.gameState.state) {
        case GAME_STATE.CHALLENGED:
          return PLAYER_STATE.WAITING_FOR_OPPONENT;
        case GAME_STATE.TURN_OF_PLAYER1:
          return PLAYER_STATE.WAITING_FOR_TRIGGER;
        case GAME_STATE.PLAYER1_AWAIT_RANDOMNESS:
          if (this.player1Survived === null) {
            return PLAYER_STATE.WAITING_FOR_RANDOMNESS;
          } else if (this.player1Survived) {
            return PLAYER_STATE.HAS_SURVIVED_NOT_WITHDRAWN;
          } else {
            return PLAYER_STATE.HAS_SURVIVED_WITHDRAWN;
          }
        case GAME_STATE.TURN_OF_PLAYER2:
          return PLAYER_STATE.WAITING_FOR_OPPONENT;
        case GAME_STATE.PLAYER2_AWAIT_RANDOMNESS:
          return PLAYER_STATE.WAITING_FOR_OPPONENT;
        case GAME_STATE.ENDED:
          return null;
      }
    },
    player2State() {
      if (!this.gameState) {
        return null;
      }
      switch (this.gameState.state) {
        case GAME_STATE.CHALLENGED:
          return PLAYER_STATE.WAITING_FOR_ACCEPTANCE;
        case GAME_STATE.TURN_OF_PLAYER1:
          return PLAYER_STATE.WAITING_FOR_OPPONENT;
        case GAME_STATE.PLAYER2_AWAIT_RANDOMNESS:
          return PLAYER_STATE.WAITING_FOR_OPPONENT;
        case GAME_STATE.TURN_OF_PLAYER2:
          return PLAYER_STATE.WAITING_FOR_TRIGGER;
        case GAME_STATE.PLAYER2_AWAIT_RANDOMNESS:
          if (this.player2Survived === null) {
            return PLAYER_STATE.WAITING_FOR_RANDOMNESS;
          } else if (this.player2Survived) {
            return PLAYER_STATE.HAS_SURVIVED_NOT_WITHDRAWN;
          } else {
            return PLAYER_STATE.HAS_SURVIVED_WITHDRAWN;
          }
        case GAME_STATE.ENDED:
          return null;
      }
    },
  },

  watch: {
    $route: {
      immediate: true,
      async handler() {
        if (this.$route.params.gameID === this.gameID) {
          return;
        }
        this.gameState = null;
        this.player1Survived = null;
        this.player2Survived = null;
        this.gameID = this.$route.params.gameID;
        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const contract = new ethers.Contract(
          config.rouletteContractAddress,
          rouletteABI,
          provider
        );
        this.gameState = await contract.games(this.gameID);
        if (this.gameState.state >= GAME_STATE.PLAYER1_AWAIT_RANDOMNESS) {
          try {
            this.player1Survived = await contract.didPlayerSurvive(
              this.gameID,
              0
            );
          } catch {
            this.player1Survived = null;
          }
        }
        if (this.gameState.state >= GAME_STATE.PLAYER1_AWAIT_RANDOMNESS) {
          try {
            this.player2Survived = await contract.didPlayerSurvive(
              this.gameID,
              1
            );
          } catch {
            this.player2Survived = null;
          }
        }
      },
    },
  },

  methods: {
    async onConnected(account) {
      this.account = ethers.utils.getAddress(account);
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      this.signer = await provider.getSigner();
    },
  },
};
</script>
