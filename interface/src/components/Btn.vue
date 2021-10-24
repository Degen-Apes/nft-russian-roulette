<template>
  <button
    @click="onClick"
    :disabled="inProgress"
    class="button mt-5 w-52 h-10 mx-auto"
  >
    <p v-if="!inProgress">
      <slot></slot>
    </p>
    <div v-else class="flex justify-center items-center">
      <div
        class="animate-spin rounded-full h-5 w-5 border-b-2 border-gray-900"
      ></div>
    </div>
  </button>
</template>

<script>
export default {
  name: "Btn",
  props: ["inProgress"],
  emits: ["click"],

  methods: {
    onClick() {
      if (this.inProgress) {
        return;
      }
      this.$emit("click");
    },
  },
};
</script>
