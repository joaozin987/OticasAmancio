import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    // Allow Railway production host so Vite preview/dev won't block the request
    allowedHosts: [
      "oticasamancio-production.up.railway.app"
    ]
  }
});
