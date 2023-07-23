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

  <div class="Wireframe1">
    <div class="Frame49">
      <span class="Frame49-Title"> 당신을 위한 추천 커피에요 </span>
      <span class="Frame49-Sub"> 마음에 드시나요? </span>
    </div>
    <div class="Frame50">
      <Card
        v-for="bean in beans"
        @openModal="
          this.modalShow = !this.modalShow;
          this.selectedBean = $event;
        "
        :key="bean"
        :bean="bean"
        style="width: 250px"
      ></Card>
    </div>
  </div>
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
.Wireframe1 {
  display: flex;
  padding: 82px 71px;
  flex-direction: column;
  align-items: center;
  gap: 102px;
  background: #fff;
}
.Frame49 {
  display: flex;
  /* width: 1297.969px; */
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 9px;
}
.Frame49-Title {
  color: var(--system-grey-900, #212121);
  text-align: center;
  font-family: Inter;
  font-size: 64px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
  letter-spacing: 2.2px;
  text-transform: uppercase;
}
.Frame49-Sub {
  color: var(--system-grey-600, #757575);
  text-align: center;
  font-family: Inter;
  font-size: 20px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  letter-spacing: 0.2px;
}
.Frame50 {
  display: flex;
  width: 1111px;
  /* height: 422px; */
  justify-content: center;
  align-items: flex-start;
  gap: 122px;
}
</style>
