<template>
  <img :src="isDead ? '/gravestone.png' : src" />
</template>

<script>
import { ethers } from "ethers";
import { fetchERC721Metadata } from "../erc721MetadataFetching.js";
import { getSourceURL } from "../urls.js";
import * as config from "../config.js";

export default {
  name: "NFT",
  props: ["contractAddress", "tokenID", "isDead"],

  data() {
    return {
      src: null,
    };
  },

  watch: {
    contractAddress: {
      immediate: true,
      handler() {
        this.updateSRC();
      },
    },
    tokenID: {
      immediate: true,
      handler() {
        this.updateSRC();
      },
    },
  },

  methods: {
    async updateSRC() {
      if (!this.contractAddress || !this.tokenID) {
        this.src = null;
        return;
      }

      const provider = new ethers.providers.Web3Provider(window.ethereum);
      const metadata = await fetchERC721Metadata(
        provider,
        config.chainID,
        this.contractAddress,
        this.tokenID
      );
      this.src = getSourceURL(metadata);
      console.log(this.tokenID);
    },
  },
};
</script>
