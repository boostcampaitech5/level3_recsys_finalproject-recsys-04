<template>
  <NavVar></NavVar>
  <MainIntro></MainIntro>
  <MainReview></MainReview>
  <MainProductSample></MainProductSample>
  <MainReconi></MainReconi>
  <Footer></Footer>
</template>

<script>
import NavVar from "./components/NavVar.vue";
import MainIntro from "./components/MainIntro.vue";
import MainReview from "./components/MainReview.vue";
import MainProductSample from "./components/MainProductSample.vue";
import MainReconi from "./components/MainReconi.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    NavVar,
    MainIntro,
    MainReview,
    MainProductSample,
    MainReconi,
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
