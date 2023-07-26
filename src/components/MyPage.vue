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
        <h1 class="display-4 fw-bolder">{{nickname}}님 반갑습니다.</h1>
        <p class="lead fw-normal text-white mb-0">
          커피 플레이리스트가 여러분의 커피 경험을 업그레이드시켜줄게요
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
        class="row gx-4 gx-lg-5 row-cols-1 row-cols-md-2 row-cols-xl-3 justify-content-center"
      >
        <div class="col mb-5" style="display: flex; justify-content: center; align-content: center" v-for="bean in coldStart" :key="bean">
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
        <div class="p-4">
          <b-button @click="getNotColdStart" variant="outline-warning"> 다른 상품 추천 받기 </b-button>
        </div>
      </div>
    <div class="container px-4 px-lg-5 mt-5">
      <div
        class="row gx-4 gx-lg-5 row-cols-1 row-cols-md-2 row-cols-xl-3 justify-content-center"
      >
        <div class="col mb-5" style="display: flex; justify-content: center; align-content: center" v-for="bean in notColdStart" :key="bean">
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
        class="row gx-4 gx-lg-5 row-cols-1 row-cols-md-2 row-cols-xl-3 justify-content-center"
      >
        <div class="col mb-5" style="display: flex; justify-content: center; align-content: center" v-for="bean in cart" :key="bean">
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
    var nickname = ref([]);

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
        nickname.value = getted.data.nickname;
      })
      .catch(()=>{
        console.log("실패😘");
      })
    }

    function getNotColdStart(){
      axios.get('http://reconi-backend.kro.kr:30005/api/v1/coffee-beans/not_cold_start_recommended/', {
        headers:{
          Authorization: `Bearer ${store.state.token}`
        }
      })
      .then((getted)=>{
        console.log(getted)
        notColdStart.value=getted.data;
        alert('현재 담기된 데이터를 기반으로 추천된 아이템들이 업데이트 됐어요!')
      })
      .catch((e)=>{
        console.log(e);
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
      nickname,
      getNotColdStart,
    }
  }
}

</script>

<style scoped>
@import "./css/styles.css";
</style>
