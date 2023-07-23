<template>
  <!-- modal -->
  <div class="w-full bg-white">
    <b-modal v-model="this.modalShow" size="lg" hide-footer>
      <template #modal-title>
      </template>
      <ProductDetail style="display:inline-flex" :selectedBean="this.selectedBean" />
    </b-modal>
  </div>

  <!-- Header-->
  <header class="bg-dark py-5">
    <div class="container px-4 px-lg-5 my-5">
      <div class="text-center text-white">
        <h1 class="display-4 fw-bolder">...님 반갑습니다.</h1>
        <p class="lead fw-normal text-white-50 mb-0">
          ... 님과 관련된 원두 상품들을 보여드릴게요.
        </p>
      </div>
    </div>
  </header>
  <!-- Section-->
  <section class="py-5">
      <div>
        <h3 class="fw-bolder"> 테스트 결과 추천 받은 상품들이에요. </h3>
      </div>
    <div class="container px-4 px-lg-5 mt-5">
      <div
        class="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center"
      >
        <div class="col mb-5" v-for="bean in coldStart" :key="bean">
          <Card
          @openModal="
          this.modalShow = !this.modalShow;
          this.selectedBean = $event;
          "
          :bean="bean"
          />
        </div>
      </div>
    </div>
  </section>

  <section class="py-5">
      <div>
        <h3 class="fw-bolder"> 좋아하는 상품과 유사한 상품들이에요. </h3>
      </div>
    <div class="container px-4 px-lg-5 mt-5">
      <div
        class="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center"
      >
        <div class="col mb-5" v-for="bean in notColdStart" :key="bean">
          <Card
          @openModal="
          this.modalShow = !this.modalShow;
          this.selectedBean = $event;
          "
          :bean="bean"
          />
        </div>
      </div>
    </div>
  </section>

  <section class="py-5">
      <div>
        <h3 class="fw-bolder"> 당신이 좋아하는 상품이에요. </h3>
      </div>
    <div class="container px-4 px-lg-5 mt-5">
      <div
        class="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center"
      >
        <div class="col mb-5" v-for="bean in cart" :key="bean">
          <Card
          @openModal="
          this.modalShow = !this.modalShow;
          this.selectedBean = $event;
          "
          :bean="bean"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Card from "./Card.vue";
import ProductDetail from "./ProductDetail.vue";
import { ref, onMounted } from "vue";
import axios from "axios";
import { useStore } from 'vuex';

export default{
  name: "my-page",
  components: {
    ProductDetail,
    Card,
  },
  setup(){
    const store = useStore()
    var modalShow = ref(false);
    var cart = ref([]);
    var coldStart = ref([]);
    var notColdStart = ref([]);

    function getUserData(){
      axios
      .get('http://reconi-backend.kro.kr:30005/api/v1/coffee-beans/mypage/', {
        headers:{
          Authorization: `Bearer ${store.state.token}`
        }
      })
      .then((getted)=>{
        console.log(getted);
        cart.value = getted.data.cart;
        coldStart.value = getted.data.cold_start;
        notColdStart.value = getted.data.not_cold_start;
      })
      .catch(()=>{
        console.log("실패😘");
      })
    }

    onMounted(()=>{
      getUserData();
    });


    return {
      modalShow,
      getUserData,
      cart,
      coldStart,
      notColdStart,

    }
  }
}

</script>

<style scoped>
@import "./css/styles.css";
</style>
