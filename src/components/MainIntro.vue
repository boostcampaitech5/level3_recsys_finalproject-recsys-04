<template>
  <div class="baseBG" id="9:4606">
    <div class="Frame10">
      <div class="Frame9">
        <p class="Frame9-title">
          당신에게 어울리는 커피를
          <br />
          찾아드릴게요
        </p>
        <p class="Frame9-sub">
          누구에게나 똑같은 커피가 아닌, 오직 당신을 위한 커피를 AI가
          추천드립니다.
        </p>
      </div>
      <div class="Frame12">
        <b-button pill variant="outline-danger" class="Frame12-button">테스트 하기</b-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "main-intro",
};
</script>

<style>
.baseBG {
  display: flex;
  /* width: 1440px; */
  height: 735px;
  padding: 80px 120px;
  justify-content: center;
  align-items: center;
  gap: 20px;
  background: var(--light-primary-origin, #3563E9);
}
.Frame10{
  display: flex;
  width: 1081px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 50px;
  flex-shrink: 0;
}
.Frame9{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;
  align-self: stretch;
}
.Frame9-title{
  /* width: 923px; */
  color: var(--white, #FFF);
  text-align: center;
  font-family: Inter;
  font-size: 64px;
  font-style: normal;
  font-weight: 700;
  line-height: 80px; /* 125% */
  letter-spacing: 3.2px;
  text-transform: uppercase;
}
.Frame9-sub{
  /* width: 755px; */
  color: var(--system-grey-50, #FAFAFA);
  text-align: center;
  font-family: Inter;
  font-size: 20px;
  font-style: normal;
  font-weight: 500;
  line-height: 30px; /* 150% */
  letter-spacing: 0.2px;
}
.Frame12{
  display: flex;
  align-items: flex-start;
  gap: 20px;
}
.Frame12-button{
  display: flex;
  padding: 15px 20px;
  align-items: center;
  gap: 10px;
}

</style>


