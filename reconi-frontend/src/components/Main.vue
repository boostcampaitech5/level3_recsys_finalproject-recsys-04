<template>
  <MainIntro></MainIntro>
  <MainReview></MainReview>
  <MainProductSample></MainProductSample>
  <MainReconi></MainReconi>
</template>

<script>
import MainIntro from "./MainIntro.vue";
import MainReview from "./MainReview.vue";
import MainProductSample from "./MainProductSample.vue";
import MainReconi from "./MainReconi.vue";

export default {
  name: "main-home",
  components: {
    MainIntro,
    MainReview,
    MainProductSample,
    MainReconi,
  },
};
</script>

<style>

</style>
