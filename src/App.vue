<template>
  <NavVar></NavVar>
  <router-view></router-view>
  <Footer></Footer>
</template>

<script>
import NavVar from "./components/NavVar.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    NavVar,
    Footer,
  },

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
