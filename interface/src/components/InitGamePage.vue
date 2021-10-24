<template>
  <div>
    <h1 class="h1">Init game</h1>
    <div class="w-full max-w-screen-lg mx-auto">
      <h2 class="h2">Player 1</h2>
      <div class="grid grid-cols-1 gap-3">
        <label class="block">
          <span class="text-gray-700">Contract address</span>
          <input
            type="text"
            class="mt-1 block w-full"
            v-model="player1Address"
          />
        </label>
        <label class="block">
          <span class="text-gray-700">Token ID</span>
          <input type="text" class="mt-1 block w-full" v-model="player1ID" />
        </label>
      </div>

      <h2 class="h2">Player 2</h2>
      <div class="grid grid-cols-1 gap-3">
        <label class="block">
          <span class="text-gray-700">Contract address</span>
          <input
            type="text"
            class="mt-1 block w-full"
            v-model="player2Address"
          />
        </label>
        <label class="block">
          <span class="text-gray-700">Token ID</span>
          <input type="text" class="mt-1 block w-full" v-model="player2ID" />
        </label>
      </div>

      <button
        @click="clickStartGame"
        :disabled="inProgress"
        class="button mt-5 w-52 h-10"
      >
        <div v-if="!inProgress">Start Game</div>
        <div v-else class="flex justify-center items-center">
          <div
            class="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-900"
          ></div>
        </div>
      </button>
    </div>
  </div>
</template>

<script>
import { ethers } from "ethers";
import erc721ABI from "../assets/erc721ABI.json";
import * as config from "../config.js";

export default {
  name: "InitGamePage",

  data() {
    return {
      player1Address: null,
      player1ID: null,
      player2Address: null,
      player2ID: null,
      inProgress: false,
    };
  },

  computed: {
    player1IDInt() {
      if (!this.player1ID) {
        return false;
      }
      return ethers.BigNumber.from(this.player1ID);
    },
    player2IDInt() {
      if (!this.player2ID) {
        return false;
      }
      return ethers.BigNumber.from(this.player2ID);
    },
    initTransferCallData() {
      if (!this.player2IDInt || !this.player2Address) {
        return null;
      }
      return ethers.utils.defaultAbiCoder.encode(
        ["address", "uint256"],
        [this.player2Address, this.player2IDInt]
      );
    },
  },

  methods: {
    async clickStartGame() {
      if (this.inProgress) {
        return;
      }
      this.inProgress = true;
      try {
        await this.startGame();
      } finally {
        this.inProgress = false;
      }
    },

    async startGame() {
      await window.ethereum.request({
        method: "eth_requestAccounts",
      });
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = provider.getSigner();
      const signerAddress = await signer.getAddress();

      const player1Contract = new ethers.Contract(
        this.player1Address,
        erc721ABI,
        signer
      );
      const tx = await player1Contract[
        "safeTransferFrom(address,address,uint256,bytes)"
      ](
        signerAddress,
        config.rouletteContractAddress,
        this.player1IDInt,
        this.initTransferCallData
      );
      const receipt = await tx.wait();
      console.log(receipt);
    },
  },
};
</script>
