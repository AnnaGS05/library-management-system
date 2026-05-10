<template>
  <div class="min-h-screen bg-base-200">
    <!-- Navbar -->
    <div class="navbar bg-base-100 shadow-lg">
      <div class="flex-1">
        <router-link to="/" class="btn btn-ghost text-xl normal-case">
          Библиотека
        </router-link>
      </div>

      <div class="flex-none gap-2">
        <router-link to="/" class="btn btn-ghost btn-sm">
          Каталог
        </router-link>

        <template v-if="auth.isAuthenticated">
          <router-link to="/my-books" class="btn btn-ghost btn-sm">
            Мои книги
          </router-link>

          <div v-if="auth.isAdmin" class="dropdown dropdown-end">
            <label tabindex="0" class="btn btn-ghost btn-sm">
              Админка
            </label>
            <ul
              tabindex="0"
              class="menu dropdown-content z-10 p-2 shadow bg-base-100 rounded-box w-52"
            >
              <li>
                <router-link to="/admin/books">Книги</router-link>
              </li>
            </ul>
          </div>

          <button
            @click="auth.logout"
            class="btn btn-outline btn-error btn-sm"
          >
            Выйти
          </button>
        </template>

        <router-link
          v-else
          to="/login"
          class="btn btn-primary btn-sm"
        >
          Войти
        </router-link>
      </div>
    </div>

    <div class="container mx-auto p-6">
      <router-view />
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from "./stores/auth";

const auth = useAuthStore();
</script>
