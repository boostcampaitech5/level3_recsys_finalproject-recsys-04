<template>
  <!-- sample Product Detail Page -->
  <div class="w-full bg-white">
    <b-modal v-model="this.modalShow" size="lg" hide-footer>
      <ProductDetail
        style="display: inline-flex"
        :selectedBean="this.selectedBean"
      />
    </b-modal>
  </div>

  <section class="py-5">
    <div>
      <h1 style="font-size: 40px" class="fw-bolder">
        어떤 로스터리, 어떤 상품이 있는지는 걱정하지 마세요.
      </h1>
      <p class="lead fw-normal text-black mb-0 p-4">
        79개의 로스터리, 424개의 상품 중에서 알아서 추천해드릴게요.
      </p>
    </div>
    <div class="container px-4 px-lg-4 mt-5">
      <div
        class="row gx-4 gx-lg-5 row-cols-1 row-cols-md-2 row-cols-xl-3"
        style="display: flex; justify-content: center; align-content: center"
      >
        <div
          class="col mb-5"
          v-for="idx in 6"
          :key="idx"
          style="display: flex; justify-content: center; align-content: center"
        >
          <Card
            style="
            "
            @openModal="
              this.modalShow = !this.modalShow;
              this.selectedBean = $event;
            "
            :bean="sampleProducts[idx]"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Card from "./Card.vue";
import axios from "axios";
import { ref, onMounted } from "vue";
import ProductDetail from "./ProductDetail.vue";

export default {
  name: "main-product-sample",
  components: {
    Card,
    ProductDetail,
  },
  setup() {
    // sample Products 저장
    var sampleProducts = ref([]);

    // sample Products Detail 정보
    var modalShow = ref(false);
    var selectedBean = ref(null);

    function getSampleProducts() {
      axios
        .get(
          "http://reconi-backend.kro.kr:30005/api/v1/coffee-beans/random_items/?page=0&page_size=0"
        )
        .then((getted) => {
          sampleProducts.value = getted.data;
        })
        .catch(() => {
          console.log("실패😘");
        });
    }

    onMounted(() => {
      getSampleProducts();
    });

    return {
      sampleProducts,
      getSampleProducts,
      modalShow,
      selectedBean,
    };
  },
};
</script>

<style></style>
