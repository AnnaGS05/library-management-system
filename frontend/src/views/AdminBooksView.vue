<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h1 class="text-2xl md:text-3xl font-semibold">
          Управление книгами
        </h1>
        <p class="text-sm opacity-70 mt-1">
          Добавляйте, редактируйте и удаляйте книги каталога.
        </p>
      </div>

      <div class="flex flex-col md:flex-row gap-3 md:items-center">
        <input
          v-model="search"
          type="text"
          placeholder="Поиск по названию или автору"
          class="input input-bordered w-64"
        />
      </div>
    </div>

    <!-- Форма добавления -->
    <div class="card bg-base-100 shadow-sm">
      <div class="card-body gap-3">
        <h2 class="card-title text-lg">Добавить книгу</h2>
        <div class="grid md:grid-cols-4 gap-3">
          <input
            v-model="newBook.title"
            type="text"
            placeholder="Название"
            class="input input-bordered w-full"
          />
          <input
            v-model="newBook.author"
            type="text"
            placeholder="Автор"
            class="input input-bordered w-full"
          />
          <input
            v-model.number="newBook.year"
            type="number"
            placeholder="Год"
            class="input input-bordered w-full"
          />
          <label class="label cursor-pointer justify-start gap-3">
            <span class="label-text">Доступна</span>
            <input type="checkbox" class="toggle" v-model="newBook.available" />
          </label>
        </div>
        <div class="card-actions justify-end">
          <button
            class="btn btn-primary"
            :disabled="createLoading"
            @click="createBook"
          >
            <span v-if="createLoading" class="loading loading-spinner loading-xs"></span>
            <span v-else>Добавить</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Таблица книг -->
    <div class="card bg-base-100 shadow-sm">
      <div class="card-body p-0">
        <div class="overflow-x-auto">
          <table class="table table-zebra w-full">
            <thead>
              <tr>
                <th class="w-12">ID</th>
                <th>Название</th>
                <th>Автор</th>
                <th class="w-24">Год</th>
                <th class="w-32">Доступна</th>
                <th class="w-40 text-right pr-6">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="book in filteredBooks" :key="book.id">
                <td>{{ book.id }}</td>
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.year }}</td>
                <td>
                  <span
                    class="badge"
                    :class="book.available ? 'badge-success' : 'badge-neutral'"
                  >
                    {{ book.available ? "Да" : "Нет" }}
                  </span>
                </td>
                <td class="text-right space-x-2">
                  <button
                    class="btn btn-xs"
                    @click="openEdit(book)"
                  >
                    Редактировать
                  </button>
                  <button
                    class="btn btn-xs btn-error"
                    :disabled="deleteLoadingId === book.id"
                    @click="removeBook(book)"
                  >
                    <span
                      v-if="deleteLoadingId === book.id"
                      class="loading loading-spinner loading-xs"
                    ></span>
                    <span v-else>Удалить</span>
                  </button>
                </td>
              </tr>
              <tr v-if="!loading && filteredBooks.length === 0">
                <td colspan="6" class="text-center py-4 text-sm opacity-70">
                  Книги не найдены.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-if="loading" class="flex justify-center py-4">
          <span class="loading loading-spinner loading-md"></span>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert alert-error mt-4">
      <span>{{ error }}</span>
    </div>

    <!-- Модальное окно редактирования -->
    <dialog ref="editDialog" class="modal">
      <div class="modal-box">
        <h3 class="font-bold text-lg mb-3">Редактировать книгу</h3>
        <div v-if="editBook" class="space-y-3">
          <input
            v-model="editBook.title"
            type="text"
            class="input input-bordered w-full"
            placeholder="Название"
          />
          <input
            v-model="editBook.author"
            type="text"
            class="input input-bordered w-full"
            placeholder="Автор"
          />
          <input
            v-model.number="editBook.year"
            type="number"
            class="input input-bordered w-full"
            placeholder="Год"
          />
          <label class="label cursor-pointer justify-start gap-3">
            <span class="label-text">Доступна</span>
            <input type="checkbox" class="toggle" v-model="editBook.available" />
          </label>
        </div>
        <div class="modal-action">
          <form method="dialog" class="space-x-2">
            <button type="button" class="btn" @click="closeEdit">
              Отмена
            </button>
            <button
              type="button"
              class="btn btn-primary"
              :disabled="editLoading"
              @click="saveEdit"
            >
              <span v-if="editLoading" class="loading loading-spinner loading-xs"></span>
              <span v-else>Сохранить</span>
            </button>
          </form>
        </div>
      </div>
    </dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "@/services/api";

const books = ref([]);
const loading = ref(false);
const error = ref("");

const search = ref("");

const newBook = ref({
  title: "",
  author: "",
  year: new Date().getFullYear(),
  available: true,
});

const createLoading = ref(false);
const deleteLoadingId = ref(null);
const editLoading = ref(false);

const editBook = ref(null);
const editDialog = ref(null);

const loadBooks = async () => {
  loading.value = true;
  error.value = "";
  try {
    const res = await api.get("/books");
    books.value = res.data;
  } catch (e) {
    error.value = "Не удалось загрузить список книг";
  } finally {
    loading.value = false;
  }
};

const filteredBooks = computed(() => {
  let list = books.value;
  if (search.value.trim()) {
    const q = search.value.toLowerCase();
    list = list.filter(
      (b) =>
        b.title.toLowerCase().includes(q) ||
        (b.author && b.author.toLowerCase().includes(q))
    );
  }
  return list;
});

const createBook = async () => {
  if (!newBook.value.title || !newBook.value.author || !newBook.value.year) {
    error.value = "Заполните название, автора и год";
    return;
  }
  createLoading.value = true;
  error.value = "";
  try {
    await api.post("/books", newBook.value);
    newBook.value = {
      title: "",
      author: "",
      year: new Date().getFullYear(),
      available: true,
    };
    await loadBooks();
  } catch (e) {
    error.value = "Не удалось добавить книгу";
  } finally {
    createLoading.value = false;
  }
};

const removeBook = async (book) => {
  if (!confirm(`Удалить книгу "${book.title}"?`)) return;

  deleteLoadingId.value = book.id;
  error.value = "";
  try {
    await api.delete(`/books/${book.id}`);
    await loadBooks();
  } catch (e) {
    error.value = "Не удалось удалить книгу";
  } finally {
    deleteLoadingId.value = null;
  }
};

const openEdit = (book) => {
  editBook.value = { ...book };
  if (editDialog.value?.showModal) {
    editDialog.value.showModal();
  }
};

const closeEdit = () => {
  editBook.value = null;
  if (editDialog.value?.close) {
    editDialog.value.close();
  }
};

const saveEdit = async () => {
  if (!editBook.value) return;
  editLoading.value = true;
  error.value = "";
  try {
    await api.put(`/books/${editBook.value.id}`, editBook.value);
    await loadBooks();
    closeEdit();
  } catch (e) {
    error.value = "Не удалось сохранить изменения";
  } finally {
    editLoading.value = false;
  }
};

onMounted(() => {
  loadBooks();
});
</script>
