import { defineStore } from "pinia";
import api from "@/services/api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    token: localStorage.getItem("token") || null,
    isAdmin: localStorage.getItem("is_admin") === "1",
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(credentials) {
      const res = await api.post("/auth/login", {
        email: credentials.email,
        password: credentials.password,
      });

      this.token = res.data.access_token;
      localStorage.setItem("token", this.token);

      await this.fetchMe();
    },

    async register(data) {
      await api.post("/auth/register", {
        email: data.email,
        password: data.password,
        full_name: data.full_name || "",
      });
    },

    async fetchMe() {
      const res = await api.get("/auth/me");
      this.user = res.data;
      this.isAdmin = res.data.is_admin;
      localStorage.setItem("is_admin", this.isAdmin ? "1" : "0");
    },

    logout() {
      this.user = null;
      this.token = null;
      this.isAdmin = false;
      localStorage.removeItem("token");
      localStorage.removeItem("is_admin");
    },
  },
});
