<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="card w-96 bg-base-100 shadow-2xl">
      <div class="card-body">
        <h2 class="card-title justify-center text-2xl">Вход в систему</h2>

        <div class="tabs tabs-boxed my-4">
          <a :class="{ 'tab-active': tab === 'login' }" class="tab" @click="tab = 'login'">Вход</a>
          <a :class="{ 'tab-active': tab === 'register' }" class="tab" @click="tab = 'register'">Регистрация</a>
        </div>

        <!-- Login -->
        <form v-if="tab === 'login'" @submit.prevent="login" class="space-y-4">
          <input v-model="form.email" type="email" placeholder="Email" class="input input-bordered w-full" required />
          <input v-model="form.password" type="password" placeholder="Пароль" class="input input-bordered w-full" required />
          <button type="submit" class="btn btn-primary w-full">Войти</button>
        </form>

        <!-- Register -->
        <form v-if="tab === 'register'" @submit.prevent="register" class="space-y-4">
          <input v-model="reg.full_name" placeholder="Имя" class="input input-bordered w-full" />
          <input v-model="reg.email" type="email" placeholder="Email" class="input input-bordered w-full" required />
          <input v-model="reg.password" type="password" placeholder="Пароль" class="input input-bordered w-full" required />
          <button type="submit" class="btn btn-success w-full">Зарегистрироваться</button>
        </form>

        <div v-if="error" class="alert alert-error mt-4">
          <span>{{ error }}</span>
        </div>

        <div class="text-sm text-center mt-4 opacity-70">
          Админ: <code>admin@local</code> / <code>admin</code>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import api from "@/services/api";

const router = useRouter();
const auth = useAuthStore();
const tab = ref("login");
const error = ref("");

const form = ref({ email: "", password: "" });
const reg = ref({ email: "", password: "", full_name: "" });

async function login() {
  try {
    await auth.login(form.value);
    router.push("/");
  } catch {
    error.value = "Неверный email или пароль";
  }
}

async function register() {
  try {
    await api.post("/auth/register", reg.value);
    alert("Успешно зарегистрированы! Теперь войдите.");
    tab.value = "login";
  } catch {
    error.value = "Ошибка регистрации";
  }
}
</script>