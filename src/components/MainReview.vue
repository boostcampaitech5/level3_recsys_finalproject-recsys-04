<template>
  <div>
    <div class="Clients">
      <div class="Frame17">
        <div class="Frame16">
          <span class="Frame16-title">
            "To be or not to bean, <br />
            that is the coffee."
          </span>
          <span class="Frame16-sub"> 윌리엄 셰익스피어</span>
        </div>
        <div class="Frame16-2">
          <div class="Frame60">
            <div class="Client-review">
              <div class="Frame62">
                <img v-for="num in 5" :key="num" :src="Star" alt="Star" />
              </div>
              <span class="Client-review-text" style="text-align: center"
                >"원두 커피 입문자로써 어떤 상품을 선택해야 할지 막막했어요.
                커피 플레이리스트에서는 원두 입문자에게도 적절하게 추천해줘서
                진입 장벽이 낮아진 느낌이에요. 커피에 대한 지식이 없더라도 쉽고
                빠르게 내 취향에 맞는 원두를 찾을 수 있어서 좋아요!"</span
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
                >"개인화 추천이 정말 대단해요! 제 취향과 원하는 스타일을 정확히
                파악해서, 맞춤형으로 원두를 추천해주는 게 너무 감동이에요. 이런
                서비스를 통해 처음으로 마셔본 커피도 내 취향에 꼭 맞았어요. 정말
                잘 선택한 것 같아요."</span
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
                >"국내 유명 로스터리들의 원두도 커피 플레이리스트에서 만날
                수 있어서 너무 좋아요! 이제 집에서도 내가 좋아하는
                유명 로스터리의 커피를 즐길 수 있으니까, 커피 시간이 더욱
                특별해진 느낌이 들어요! 커피 플레이리스트 애용합니다!"</span
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
import Star from "../../public/star.svg";
import sample from "../../public/jisu.jpg";
import sample2 from "../../public/dohyun.jpg";
import sample3 from "../../public/yerim.jpg";
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
