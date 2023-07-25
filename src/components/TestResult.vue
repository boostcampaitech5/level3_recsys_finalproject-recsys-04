<template>
  <div class="w-full bg-white">
    <b-modal v-model="this.modalShow" size="lg" hide-footer>
      <template #modal-title> </template>
      <ProductDetail
        style="display: inline-flex"
        :selectedBean="this.selectedBean"
      />
    </b-modal>
  </div>

  <section class="py-5">
    <div>
      <h3 class="fw-bolder">당신을 위한 추천 커피에요.</h3>
      <h5> 추천 결과는 언제든지 마이페이지에서 확인할 수 있어요.</h5>
    </div>
    <div class="container px-4 px-lg-5 mt-5">
      <div
        class="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-3 justify-content-center"
      >
        <div class="col mb-5" v-for="bean in beans" :key="bean">
          <Card
            @openModal="
              this.modalShow = !this.modalShow;
              this.selectedBean = $event;
            "
            :bean="bean"
            style="width: 300px"
          ></Card>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Card from "./Card.vue";
import ProductDetail from "./ProductDetail.vue";
export default {
  name: "test-result",
  data() {
    return {
      modalShow: false,
      selectedBean: null,
    };
  },
  components: {
    Card,
    ProductDetail,
  },
  props: {
    beans: Object,
  },
};
</script>

<style scoped>
@import "./css/styles.css";
</style>
