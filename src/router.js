import { createWebHistory, createRouter } from "vue-router";
import Main from './components/Main.vue';
import TestPage from './components/TestPage.vue';

const routes = [
  {
    path: "/",
    component: Main
  },
  {
    path: "/test",
    component: TestPage
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router; 