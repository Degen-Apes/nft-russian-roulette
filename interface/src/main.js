import { createApp } from "vue";
import App from "./App.vue";
import { router } from "./routes.js";
import "./index.css";

const app = createApp(App);
app.use(router);
app.mount("#app");
