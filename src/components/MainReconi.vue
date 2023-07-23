<template>
  <div class="reconi">
    <div class="Frame17">
      <div class="Frame16">
        <span class="Frame16-title"> 저희는 RecoRecoNi 입니다.</span>
      </div>
      <span class="Frame16-sub">김수민 박예림 임도현 임우열 임지수</span>
    </div>
    <div class="Frame58">
      <img class ="Frame58-img">
      <div class="Frame58-Frame16">
        <div class="Frame34">
          <span class="Frame34-Title"> 더 이상 커피 선택에 <br> 망설임이 없도록</span>
        </div>
        <span class="Frame34-sub">BoostCamp AI Tech 5기 - Recsys Track 4팀</span>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: "main-reconi",
};
</script>

<style>
.reconi{
  /* display: inline-flex; */
  display: flex;
  padding: 80px 120px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 70px;
  background: #FFF;
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
  justify-content: center;
  text-align: center;
  font-family: Inter;
  font-size: 48px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  letter-spacing: 0.2px;
  text-transform: capitalize;
}
.Frame16-sub{
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
.Frame58{
  display: flex;
  align-items: center;
  gap: 55px;
}
.Frame58-img{
  display: flex;
  width: 652px;
  height: 472px;
  /* padding: 256px 674px; */
  /* justify-content: center; */
  /* align-items: center; */
  gap: 10px;
  background: url("/opt/repo/reconi-frontend/public/images/sample-reconicat.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  /* background: var(--light-primary-a-8, #EFF3FD); */
}
.Frame58-Frame16{
  display: flex;
  width: 510px;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 32px;
}
.Frame34{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
  align-self: stretch;
}
.Frame34-Title{
  align-self: stretch;
  color: var(--system-grey-900, #212121);
  font-family: Inter;
  font-size: 32px;
  font-style: normal;
  font-weight: 500;
  line-height: 48px; /* 150% */
  letter-spacing: 0.2px;
  text-transform: capitalize;
  text-align: left;
}
.Frame34-sub{
  color: var(--system-grey-600, #757575);
  font-family: Inter;
  font-size: 20px;
  font-style: normal;
  font-weight: 400;
  line-height: 28px;
  letter-spacing: 0.2px;
  text-transform: capitalize;
  text-align: center;
}
</style>
