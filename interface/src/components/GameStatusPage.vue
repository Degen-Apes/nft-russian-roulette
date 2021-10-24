<template>
  <div class="w-full max-w-screen-lg mx-auto">
    <h1 class="h1">Game {{ $route.params.gameID }}</h1>
    <div class="grid grid-cols-2 items-center gap-6 px-6 mx-auto">
      <h2 class="h2 text-center">Player 1</h2>
      <h2 class="h2 text-center">Player 2</h2>
      <NFT
        :contractAddress="player1TokenContractAddress"
        :tokenID="player1TokenID"
      />
      <NFT
        :contractAddress="player1TokenContractAddress"
        :tokenID="player1TokenID"
      />
      <PlayerStatus
        :playerIndex="1"
        :gameID="gameID"
        :state="player1State"
        :userIsPlayer="signer && account === player1Address"
        :signer="signer"
      />
      <PlayerStatus
        :playerIndex="2"
        :gameID="gameID"
        :state="player2State"
        :userIsPlayer="signer && account === player1Address"
        :signer="signer"
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
      return PLAYER_STATE.WAITING_FOR_ACCEPTANCE;
    },
    player2State() {
      return PLAYER_STATE.WAITING_FOR_TRIGGER;
    },
    async userAddress() {
      if (!this.signer) {
        return null;
      }
      return await this.signer.getAddress();
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
        this.gameID = this.$route.params.gameID;
        const provider = new ethers.providers.Web3Provider(window.ethereum);
        const contract = new ethers.Contract(
          config.rouletteContractAddress,
          rouletteABI,
          provider
        );
        this.gameState = await contract.games(this.gameID);
      },
    },
  },

  methods: {
    async onConnected(account) {
      this.account = account;
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      this.signer = provider.getSigner();

      // TODO: check if user is player 1 or 2
    },
  },
};
</script>
