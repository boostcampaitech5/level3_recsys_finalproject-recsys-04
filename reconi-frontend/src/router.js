import { createWebHistory, createRouter } from "vue-router";
import Main from './components/Main.vue';
import TestPage from './components/TestPage.vue';
import Products from './components/Products.vue';
import MyPage from './components/MyPage.vue';

const routes = [
  {
    path: "/",
    component: Main
  },
  {
    path: "/test",
    component: TestPage
  },
  {
    path: "/products",
    component: Products
  },
  {
    path: "/mypage/",
    component: MyPage
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router; 