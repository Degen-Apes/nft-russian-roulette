<template>
  <div>
    <div v-if="userIsPlayer" class="flex justify-center">
      <Btn
        v-if="state == PLAYER_STATE.WAITING_FOR_ACCEPTANCE"
        @click="clickAcceptChallenge"
        :inProgress="inProgress"
      >
        Accept challenge
      </Btn>
      <Btn
        v-else-if="state == PLAYER_STATE.WAITING_FOR_TRIGGER"
        @click="clickPullTrigger"
        :inProgress="inProgress"
      >
        Pull trigger
      </Btn>
      <p v-else-if="state === PLAYER_STATE.WAITING_FOR_RANDOMNESS">
        waiting for result...
      </p>
      <Btn
        v-else-if="state == PLAYER_STATE.HAS_DIED_NOT_WITHDRAWN"
        @click="clickEvaluate"
        :inProgress="inProgress"
      >
        Pick up gravestone
      </Btn>
      <Btn
        v-else-if="state == PLAYER_STATE.HAS_SURVIVED_NOT_WITHDRAWN"
        @click="clickEvaluate"
        :inProgress="inProgress"
      >
        Withdraw survivor
      </Btn>
    </div>
  </div>
</template>

<script>
import { ethers } from "ethers";
import erc721ABI from "../assets/erc721ABI.json";
import rouletteABI from "../assets/rouletteABI.json";
import * as config from "../config.js";
import Btn from "./Btn.vue";
import NFT from "./NFT.vue";

export const PLAYER_STATE = {
  WAITING_FOR_OPPONENT: 0,
  WAITING_FOR_ACCEPTANCE: 1,
  WAITING_FOR_TRIGGER: 2,
  WAITING_FOR_RANDOMNESS: 3,
  HAS_DIED_NOT_WITHDRAWN: 4,
  HAS_DIED_WITHDRAWN: 5,
  HAS_SURVIVED_NOT_WITHDRAWN: 6,
  HAS_SURVIVED_WITHDRAWN: 7,
};

export default {
  name: "PlayerStatus",
  props: [
    "gameID",
    "playerIndex",
    "state",
    "tokenContractAddress",
    "tokenID",
    "userIsPlayer",
  ],

  components: {
    Btn,
    NFT,
  },

  data() {
    return {
      inProgress: false,
    };
  },
  computed: {
    PLAYER_STATE() {
      return PLAYER_STATE;
    },

    acceptanceTransferCallData() {
      return ethers.utils.defaultAbiCoder.encode(["uint256"], [this.gameID]);
    },
  },

  methods: {
    async clickAcceptChallenge() {
      if (this.inProgress) {
        return;
      }
      this.inProgress = true;
      try {
        await this.acceptChallenge();
      } finally {
        this.inProgress = false;
      }
    },
    async acceptChallenge() {
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = await provider.getSigner();
      const signerAddress = await signer.getAddress();
      const tokenContract = new ethers.Contract(
        this.tokenContractAddress,
        erc721ABI,
        signer
      );
      const tx = await tokenContract[
        "safeTransferFrom(address,address,uint256,bytes)"
      ](
        signerAddress,
        config.rouletteContractAddress,
        this.tokenID,
        this.acceptanceTransferCallData
      );
      await tx.wait();
      window.location.reload();
    },

    async clickPullTrigger() {
      if (this.inProgress) {
        return;
      }
      this.inProgress = true;
      try {
        await this.pullTrigger();
      } finally {
        this.inProgress = false;
      }
    },
    async pullTrigger() {
      console.log(this.gameID);
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = await provider.getSigner();
      const contract = new ethers.Contract(
        config.rouletteContractAddress,
        rouletteABI,
        signer
      );
      const tx = await contract.pulltrigger(this.gameID);
      await tx.wait();
      window.location.reload();
    },

    async clickEvaluate() {
      if (this.inProgress) {
        return;
      }
      this.inProgress = true;
      try {
        await this.evaluate();
      } finally {
        this.inProgress = false;
      }
    },
    async evaluate() {
      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const signer = await provider.getSigner();
      const contract = new ethers.Contract(
        config.rouletteContractAddress,
        rouletteABI,
        signer
      );
      const tx = await contract.evaluateOutcome(this.gameID);
      await tx.wait();
      window.location.reload();
    },
  },
};
</script>
