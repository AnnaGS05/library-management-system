import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import BooksView from "../views/BooksView.vue";
import AdminBooksView from "../views/AdminBooksView.vue";
import MyBooksView from "../views/MyBooksView.vue";

const routes = [
  { path: "/", component: BooksView },
  { path: "/login", component: LoginView },
  { path: "/admin/books", component: AdminBooksView },
  { path: "/my-books", component: MyBooksView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
