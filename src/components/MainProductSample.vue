<template>
  <div class="Feature">
    <div class="Frame17">
      <div class="Frame16">
        <span class="Frame16-title">
          어떤 로스터리, 어떤 상품이 있는지는 걱정하지 마세요.
        </span>
      <span class="Frame17-sub">N개의 로스터리 M개의 상품 중에서 알아서 추천해드릴게요.</span>
      </div>

    </div>
    <div class="Frame53">
      <div class="Frame54">
        <Card class = "Feature-Card" v-for="num in 3" :key="num"/>
      </div>
      <div class="Frame55">
        <Card class = "Feature-Card" v-for="num in 3" :key="num"/>
      </div>

    </div>

  </div>
</template>

<script>
import Card from "./Card.vue";

export default {
  name: "main-product-sample",
  data() {
    return {};
  },
  components:{
    Card,
  }
};
</script>

<style>
.Feature{
  display: inline-flex;
  padding: 80px 120px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 60px;
  background: var(--white, #FFF);
  display: flex;

}
.Frame17{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 32px;
  align-self: stretch;
}
.Frame16{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 24px;
}
.Frame16-title{
  width: 952px;
  color: var(--system-grey-900, #212121);
  text-align: center;
  font-family: Inter;
  font-size: 48px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  letter-spacing: 0.2px;
  text-transform: capitalize;
  display: flex;
  word-break: keep-all; /* 단어 단위로 줄바꿈을 방지합니다 */
  background: #fff;
}
.Frame17-sub{
  color: var(--system-grey-600, #757575);
  text-align: center;
  font-family: Inter;
  font-size: 20px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  letter-spacing: 0.2px;
  text-transform: capitalize;
}
.Frame53{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 32px;
}
.Frame54{
  display: flex;
  align-items: flex-start;
  gap: 24px;
}
.Feature-Card{
  display: flex;
  padding: 25px;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 22px;
}
.Feature-Card-img{
  display: flex;
  width: 60px;
  height: 60px;
  padding: 15px;
  justify-content: center;
  align-items: center;
  border: 1px solid #ddd; /* 회색 테두리 스타일을 설정합니다 */
  border-radius: 50px;
  background: var(--light-primary-a-8, #EFF3FD);
  
}
.Frame47{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 16px;
}
.Frame47-title{
  color: var(--system-grey-900, #212121);
  font-family: Inter;
  font-size: 22px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  letter-spacing: 0.2px;
  text-transform: capitalize;
}
.Frame47-sub{
  width: 334px;
  color: var(--system-grey-700, #616161);
  font-family: Inter;
  font-size: 16px;
  font-style: normal;
  font-weight: 400;
  line-height: 24px; /* 150% */
  letter-spacing: 0.2px;
  text-transform: capitalize;
}
.Frame55{
  display: flex;
  align-items: flex-start;
  gap: 24px;
}
</style>
