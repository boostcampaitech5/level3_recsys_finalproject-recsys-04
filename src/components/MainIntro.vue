<template>
  <header class="bg-dark py-5">
    <div class="container px-4 px-lg-5 my-5">
      <div class="text-center text-white">
        <h1 class="display-4 fw-bolder">
          당신에게 어울리는 커피를 <br />
          찾아드릴게요
        </h1>
        <p class="lead fw-normal text-white mb-0 p-4">
          누구에게나 똑같은 커피가 아닌, 오직 당신을 위한 커피를 AI가
          추천드립니다.
        </p>
        <b-button
          class="p-3"
          pill
          variant="danger"
          @click="loginCheck"
          >테스트 하기</b-button
        >
      </div>
    </div>
  </header>

  <!-- <div class="baseBG" id="9:4606">
    <div class="Frame10">
      <div class="Frame99">
        <p class="Frame99-title">
          당신에게 어울리는 커피를
          <br />
          찾아드릴게요
        </p>
        <p class="Frame99-sub">
          누구에게나 똑같은 커피가 아닌, 오직 당신을 위한 커피를 AI가
          추천드립니다.
        </p>
      </div>
      <div class="Frame12">
        <b-button
          pill
          variant="danger"
          class="Frame12-button"
          @click="loginCheck"
          >테스트 하기</b-button
        >
      </div>
    </div>
  </div> -->
</template>

<script>
export default {
  name: "main-intro",
  methods: {
    loginCheck() {
      if (!this.$store.getters.isLogin) {
        alert("로그인을 먼저 진행해주세요!");
      } else {
        this.$router.push("/test");
      }
    },
  },
};
</script>

<style scoped>
@import "./css/main_intro/styles.css";

.baseBG {
  display: flex;
  /* width: 1440px; */
  height: 735px;
  padding: 80px 120px;
  justify-content: center;
  align-items: center;
  gap: 20px;
  background-image: url("../../public/test.jpg");
  /* background-size : contain; */
  /* background-size : 100% 100%; */
  /* background: var(--light-primary-origin, #3563e9); */
  /* width: 100px; */
  /* height: 100px; */
  background-position: center center;
  background-repeat: no-repeat;
}
.Frame10 {
  display: flex;
  width: 1081px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 50px;
  flex-shrink: 0;
}
.Frame99 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;
  align-self: stretch;
}
.Frame99-title {
  /* width: 923px; */
  color: var(--white, #fff);
  text-align: center;
  font-family: Inter;
  font-size: 64px;
  font-style: normal;
  font-weight: 700;
  line-height: 80px; /* 125% */
  letter-spacing: 3.2px;
  text-transform: uppercase;
}
.Frame99-sub {
  /* width: 755px; */
  color: var(--system-grey-50, #fafafa);
  text-align: center;
  font-family: Inter;
  font-size: 20px;
  font-style: normal;
  font-weight: 500;
  line-height: 30px; /* 150% */
  letter-spacing: 0.2px;
}
.Frame12 {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}
.Frame12-button {
  display: flex;
  padding: 15px 20px;
  align-items: center;
  gap: 10px;
}
</style>
