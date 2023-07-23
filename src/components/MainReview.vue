<template>
  <div>
    <div class="Clients">
      <div class="Frame17">
        <div class="Frame16">
          <span class="Frame16-title">
            "To be or not to bean, <br> that is the coffee." 
          </span>
          <span class="Frame16-sub"> 윌리엄 셰익스피어</span>
        </div>
        <div class="Frame16-2">
          <div class="Frame60">
            <div class="Client-review">
              <div class="Frame62">
                <img v-for="num in 5" :key="num" :src="Star" alt="Star" />
              </div>
              <span class="Client-review-text"
                >"동서남북 어디에서도 나란 얼간이는 없다고 그래도 너 하나만
                사랑한다고 쉽게 녹아 버린 네 마음 상처받은 MC몽 사랑은 아아아아
                아이스크림"</span
              >
              <div class="Frame63">
                <div class="Avatar">
                  <img class="Client-review-img" :src="sample" alt="sample" />
                </div>
                <span class="Client-review-img-text"> Jisu Lim </span>
              </div>
            </div>
            <div class="Client-review">
              <div class="Frame62">
                <img v-for="num in 5" :key="num" :src="Star" alt="Star" />
              </div>
              <span class="Client-review-text"
                >"I'm super shy, super shy But wait a minute while I make you
                mine, make you mine 떨리는 지금도 you're on my mind all the time
                I wanna tell you"</span
              >
              <div class="Frame63">
                <div class="Avatar">
                  <img class="Client-review-img" :src="sample2" alt="sample2" />
                </div>
                <span class="Client-review-img-text"> Dohyun Lim </span>
              </div>
            </div>
            <div class="Client-review">
              <div class="Frame62">
                <img v-for="num in 5" :key="num" :src="Star" alt="Star" />
              </div>
              <span class="Client-review-text"
                >"Lolli lolli lollipop boy 넌 나의 lollipop Lolli lolli lollipop
                oh lolli-pop-pop Lolli lolli lollipop boy 넌 나의 lollipop Lolli
                lolli lollipop oh lolli-pop-pop"</span
              >
              <div class="Frame63">
                <div class="Avatar">
                  <img class="Client-review-img" :src="sample3" alt="sample3" />
                </div>
                <span class="Client-review-img-text"> Yerim Park </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Star from "../assets/mainReview/Feather_Icon.svg";
import sample from "../assets/mainReview/sample.jpg";
import sample2 from "../assets/mainReview/sample2.jpg";
import sample3 from "../assets/mainReview/sample3.jpg";
export default {
  name: "main-review",
  data() {
    return {
      Star: Star,
      sample: sample,
      sample2: sample2,
      sample3: sample3,
    };
  },
};
</script>

<style>
.Clients {
  /* width: 1440px; */
  padding: 80px 120px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 50px;
  display: flex;

  background: #fff;
}

.Frame17 {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;
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
  /* width: 1000px; */
  color: var(--system-grey-900, #212121);
  display: flex;
  text-align: center;
  font-family: Inter;
  font-size: 48px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  letter-spacing: 0.2px;
  text-transform: capitalize;
  word-break: keep-all; /* 단어 단위로 줄바꿈을 방지합니다 */
  background: #fff;
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

.Frame16-2 {
  display: flex;
  padding: 20px;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 50px;
}

.Frame60 {
  display: flex;
  align-items: center;
  gap: 42px;
  align-self: stretch;
}

.Client-review {
  display: flex;
  width: 414px;
  height: 323px;
  padding: 10px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 27px;
}

.Frame62 {
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.Client-review-text {
  align-self: stretch;
  color: var(--system-grey-800, #424242);
  text-align: center;
  font-family: Inter;
  font-size: 20px;
  font-style: normal;
  font-weight: 500;
  line-height: 32px; /* 160% */
  letter-spacing: 0.2px;
  text-transform: capitalize;
}

.Frame63 {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.Avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.Client-review-img {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  border-radius: 40px;
  background: url("../assets/mainReview/sample.jpg"),
    lightgray 50% / cover no-repeat;
}

.Client-review-img-text {
  color: var(--system-grey-600, #757575);
  font-family: Inter;
  font-size: 14px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  letter-spacing: 0.2px;
  text-transform: capitalize;
}
</style>
