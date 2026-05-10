<template>
  <div class="space-y-6">
    <!-- Заголовок и статистика -->
    <div class="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
      <div>
        <h1 class="text-2xl font-semibold">Каталог книг</h1>
        <p class="text-sm opacity-70 mt-1">
          Найдите книгу и забронируйте её за пару кликов.
        </p>
      </div>

      <div class="flex flex-wrap gap-2 text-sm">
        <div class="badge badge-neutral gap-1">
          Всего: <span class="font-semibold">{{ books.length }}</span>
        </div>
        <div class="badge badge-success gap-1">
          Доступно: <span class="font-semibold">{{ availableCount }}</span>
        </div>
      </div>
    </div>

    <!-- Панель фильтров -->
    <div
      class="bg-base-100 border border-base-200 rounded-2xl p-4 md:p-5 flex flex-col gap-3 md:flex-row md:items-center md:justify-between shadow-sm"
    >
      <div class="flex-1">
        <label class="label py-0">
          <span class="label-text text-sm">Поиск по названию или автору</span>
        </label>
        <label class="input input-bordered flex items-center gap-2">
          <span class="opacity-60 text-sm">🔍</span>
          <input
            v-model="search"
            type="text"
            class="grow"
            placeholder="Например, «Толстой» или «Мастер и Маргарита»"
          />
        </label>
      </div>

      <div class="flex items-center gap-2 mt-2 md:mt-0 md:ml-4">
        <label class="cursor-pointer flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            class="checkbox checkbox-sm"
            v-model="showOnlyAvailable"
          />
          <span>Только доступные</span>
        </label>
      </div>
    </div>

    <!-- Состояния -->
    <div v-if="loading" class="text-sm opacity-70">
      Загружаем книги…
    </div>

    <div v-else-if="error" class="alert alert-error">
      <span>{{ error }}</span>
    </div>

    <div v-else>
      <!-- Пустой результат поиска -->
      <div
        v-if="filteredBooks.length === 0"
        class="bg-base-100 border border-dashed border-base-300 rounded-2xl p-8 text-center text-sm opacity-80"
      >
        <p class="mb-2">Ничего не найдено.</p>
        <p>Попробуйте изменить запрос или отключить фильтр «Только доступные».</p>
      </div>

      <!-- Сетка карточек -->
      <div
        v-else
        class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
      >
        <article
          v-for="book in filteredBooks"
          :key="book.id"
          class="card bg-base-100 border border-base-200 shadow-sm hover:shadow-md transition-shadow rounded-2xl flex flex-col"
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

            <div class="flex items-center justify-between text-xs opacity-70">
              <span>Год: {{ book.year }}</span>
              <span
                class="badge"
                :class="book.available ? 'badge-success' : 'badge-ghost'"
              >
                {{ book.available ? "Доступна" : "Занята" }}
              </span>
            </div>

            <div class="card-actions justify-end mt-2">
              <button
                class="btn btn-primary btn-sm"
                :disabled="!book.available || reservingId === book.id"
                @click="reserveBook(book)"
              >
                <span
                  v-if="reservingId === book.id"
                  class="loading loading-spinner loading-xs"
                />
                <span v-else>Забронировать</span>
              </button>
            </div>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../services/api";

const books = ref([]);
const loading = ref(true);
const error = ref("");
const reservingId = ref(null);

const search = ref("");
const showOnlyAvailable = ref(false);

const availableCount = computed(
  () => books.value.filter((b) => b.available).length
);

const filteredBooks = computed(() => {
  let list = [...books.value];

  if (showOnlyAvailable.value) {
    list = list.filter((b) => b.available);
  }

  const q = search.value.trim().toLowerCase();
  if (q) {
    list = list.filter(
      (b) =>
        b.title.toLowerCase().includes(q) ||
        b.author.toLowerCase().includes(q)
    );
  }

  return list;
});

function saveToMyBooks(book) {
  try {
    const stored = JSON.parse(localStorage.getItem("myBooks") || "[]");
    if (!stored.find((b) => b.id === book.id)) {
      stored.push({
        id: book.id,
        title: book.title,
        author: book.author,
        year: book.year,
      });
      localStorage.setItem("myBooks", JSON.stringify(stored));
    }
  } catch (e) {
    console.error("Ошибка сохранения myBooks", e);
  }
}

async function loadBooks() {
  loading.value = true;
  error.value = "";
  try {
    const res = await api.get("/books/");
    books.value = res.data;
  } catch (e) {
    error.value = "Не удалось загрузить список книг";
  } finally {
    loading.value = false;
  }
}

async function reserveBook(book) {
  reservingId.value = book.id;
  error.value = "";

  try {
    await api.post("/reservations/", { book_id: book.id });
    book.available = false;
    saveToMyBooks(book);
  } catch (e) {
    error.value = "Не удалось забронировать книгу";
  } finally {
    reservingId.value = null;
  }
}

onMounted(loadBooks);
</script>
