import { createWebHashHistory, createRouter } from "vue-router";
import InitGamePage from "./components/InitGamePage.vue";
import GameStatusPage from "./components/GameStatusPage.vue";

const routes = [
  { path: "/", component: InitGamePage },
  { path: "/status", component: GameStatusPage },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});
