<template>
  <div>
    <h1>Init game</h1>
    <div>
      <h2>Player 1</h2>
      <div class="grid grid-cols-1 gap-6">
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

      <h2>Player 2</h2>
      <div class="grid grid-cols-1 gap-6">
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

      <button @click="startGame">Start Game</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "InitGamePage",

  data() {
    return {
      player1Address: null,
      player1ID: null,
      player2Address: null,
      player2ID: null,
    };
  },

  methods: {
    startGame() {
      console.log(
        "start game",
        this.player1Address,
        this.player1ID,
        this.player2Address,
        this.player2ID
      );
    },
  },
};
</script>
