import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'

// vue form setting
import "./assets/main.scss";
import Vueform from "@vueform/vueform/plugin";
import vueformConfig from "./../vueform.config";


// bootstrap setting
import BootstrapVue3 from "bootstrap-vue-3";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-3/dist/bootstrap-vue-3.css";


const app = createApp(App)
app.use(BootstrapVue3)
app.use(router)
app.use(Vueform, vueformConfig);
app.mount("#app");
