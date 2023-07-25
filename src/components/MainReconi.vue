<template>
  <div class="reconi">
    <div class="Frame17">
      <div class="Frame16">
        <span class="Frame16-title"> 저희는 RecoRecoNi 입니다.</span>
      </div>
      <span class="Frame16-sub">김수민 박예림 임도현 임우열 임지수</span>
    </div>
    <div class="Frame58">
      <img class="Frame58-img" />
      <div class="Frame58-Frame16">
        <div class="Frame34">
          <span class="Frame34-Title">
            더 이상 커피 선택에 <br />
            망설임이 없도록</span
          >
          <p style="text-align: justify">
            우리가 '커피 플레이리스트'를 시작한 이유는, 커피 시장의 성장과
            고급화, 그리고 개인 취향의 중요성에 주목했기 때문입니다. 스페셜티
            커피의 인기와 다양성으로 커피 시장이 더욱 세분화되고, 원두 선택이
            복잡해지고 있습니다. 예전에는 믹스커피를 마시던 사람들조차 이제는
            특별한 맛과 원산지에 관심을 갖게 되었습니다.
          </p>
          <p style="text-align: justify">
            더욱이 코로나로 인해 홈카페 문화가 확산되면서 집에서 커피를 즐기는
            사람들이 늘어났지만, 맞춤형 커피 원두를 찾는 것은 여전히 어렵습니다.
            수많은 원두 중에서 자신에게 맞는 것을 찾는 것은 시간과
            노력이 필요합니다.
          </p>
          <p style="text-align: justify">
            그래서 우리는 '커피 플레이리스트'를 통해 개인 취향에 맞는 최적의
            커피 원두를 제공하고자 합니다. 신선도, 원산지, 맛, 가격, 로스팅 방식
            등 다양한 요소를 고려하여 사용자들에게 맞춤형 추천을 제공하고, 더
            특별하고 만족스러운 커피 경험을 선사하고자 합니다. 
          </p>
          <p style="text-align: justify">
            '커피 플레이리스트'와 함께 여러분의 커피 탐험을 더욱 풍요롭게
            만들어보세요.
          </p>
        </div>
        <span class="Frame34-sub"
          >BoostCamp AI Tech 5기 - Recsys Track 4팀</span
        >
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
.reconi {
  /* display: inline-flex; */
  display: flex;
  padding: 80px 120px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 70px;
  background: #fff;
}
.Frame17 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 32px;
  align-self: stretch;
}
.Frame16 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 24px;
}
.Frame16-title {
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
.Frame16-sub {
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
.Frame58 {
  display: flex;
  align-items: center;
  gap: 55px;
}
.Frame58-img {
  display: flex;
  width: 652px;
  height: 652px;
  /* padding: 256px 674px; */
  /* justify-content: center; */
  /* align-items: center; */
  gap: 10px;
  /* background-image: url("../assets/reconi/sample-reconicat.jpg"); */
  background-image: url("../../public/sample-reconicat.jpg");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  /* background: var(--light-primary-a-8, #EFF3FD); */
}
.Frame58-Frame16 {
  display: flex;
  width: 510px;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 32px;
}
.Frame34 {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
  align-self: stretch;
}
.Frame34-Title {
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
.Frame34-sub {
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
