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
      <Btn
        v-else-if="state == PLAYER_STATE.HAS_DIED_NOT_WITHDRAWN"
        @click="clickPickUpGravestone"
        :inProgress="inProgress"
      >
        Pick up gravestone
      </Btn>
      <Btn
        v-else-if="state == PLAYER_STATE.HAS_SURVIVED_NOT_WITHDRAWN"
        @click="clickWithdrawSurvivor"
        :inProgress="inProgress"
      >
        Withdraw survivor
      </Btn>
    </div>
  </div>
</template>

<script>
import Btn from "./Btn.vue";
import NFT from "./NFT.vue";

export const PLAYER_STATE = {
  WAITING_FOR_ACCEPTANCE: 0,
  WAITING_FOR_TRIGGER: 1,
  WAITING_FOR_RANDOMNESS: 2,
  HAS_DIED_NOT_WITHDRAWN: 3,
  HAS_DIED_WITHDRAWN: 4,
  HAS_SURVIVED_NOT_WITHDRAWN: 5,
  HAS_SURVIVED_WITHDRAWN: 6,
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
    "signer",
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
      const signerAddress = await this.signer.getAddress();
      const tokenContract = new ethers.Contract(
        this.tokenContractAddress,
        erc721ABI,
        this.signer
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
    },
  },
};
</script>
