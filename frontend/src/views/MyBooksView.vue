<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
      <div>
        <h1 class="text-2xl font-semibold">Мои книги</h1>
        <p class="text-sm opacity-70 mt-1">
          Здесь отображаются книги, которые вы забронировали в каталоге.
        </p>
      </div>

      <div v-if="books.length" class="badge badge-neutral gap-1 self-start md:self-auto">
        Всего бронирований: <span class="font-semibold">{{ books.length }}</span>
      </div>
    </div>

    <!-- Пустое состояние -->
    <div
      v-if="books.length === 0"
      class="bg-base-100 border border-dashed border-base-300 rounded-2xl p-8 text-center"
    >
      <h2 class="text-lg font-medium mb-2">У вас ещё нет забронированных книг</h2>
      <p class="text-sm opacity-80 mb-4">
        Откройте каталог, выберите понравившуюся книгу и нажмите «Забронировать».
      </p>
      <router-link to="/" class="btn btn-primary btn-sm">
        Перейти в каталог
      </router-link>
    </div>

    <!-- Список книг -->
    <div
      v-else
      class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
    >
      <article
        v-for="book in books"
        :key="book.id"
        class="card bg-base-100 border border-base-200 shadow-sm rounded-2xl"
      >
        <div class="card-body gap-3">
          <div class="space-y-1">
            <h2 class="card-title text-base leading-snug">
              {{ book.title }}
            </h2>
            <p class="text-sm opacity-80">
              {{ book.author }}
            </p>
          </div>

          <p class="text-xs opacity-70">
            Год издания: {{ book.year }}
          </p>

          <div class="card-actions justify-between items-center mt-1 text-xs opacity-70">
            <span class="badge badge-outline">Забронирована</span>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const books = ref([]);

function loadMyBooks() {
  try {
    books.value = JSON.parse(localStorage.getItem("myBooks") || "[]");
  } catch (e) {
    books.value = [];
  }
}

onMounted(loadMyBooks);
</script>
