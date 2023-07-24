<template>
  <div class="w-full bg-white">
    <b-modal v-model="this.modalShow" size="lg" hide-footer>
      <LoginComponent />
    </b-modal>
  </div>

  <NavVar @openLoginModal="
  this.modalShow = !this.modalShow;"></NavVar>
  <router-view></router-view>
  <!-- <Footer></Footer> -->
</template>

<script>
import NavVar from "./components/NavVar.vue";
// import Footer from "./components/Footer.vue";
import LoginComponent from "./components/Login.vue";
import { ref } from "vue"

export default {
  name: "App",
  components: {
    NavVar,
    // Footer,
    LoginComponent,
  },
  setup(){
    var modalShow = ref(false);

    return {
      modalShow
    }
  }

};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
