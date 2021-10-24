<template>
  <Btn @click="requestAccounts" :inProgress="inProgress">Connect to Wallet</Btn>
</template>

<script>
import Btn from "./Btn.vue";

export default {
  name: "ConnectBtn",
  emits: ["connected"],

  components: {
    Btn,
  },

  data() {
    return {
      inProgress: false,
    };
  },

  async mounted() {
    const permissions = await window.ethereum.request({
      method: "wallet_getPermissions",
    });
    for (const permission of permissions) {
      if (permission.parentCapability === "eth_accounts") {
        await this.requestAccounts();
        break;
      }
    }
  },

  methods: {
    async requestAccounts() {
      if (this.inProgress) {
        return;
      }
      this.inProgress = true;
      try {
        const accounts = await window.ethereum.request({
          method: "eth_requestAccounts",
        });
        this.$emit("connected", accounts[0]);
      } finally {
        this.inProgress = false;
      }
    },
  },
};
</script>
