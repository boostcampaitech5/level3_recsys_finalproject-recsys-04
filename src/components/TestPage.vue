<template>
  <div class="Frame">
    <div class="Frame10">
      <div class="Frame9">
        <span class="Frame9-title">
          정확한 추천을 위해 <br />
          당신에 대해 알려주세요.
        </span>
        <span class="Frame9-sub">
          응답해주신 기록을 바탕으로 당신에게 꼭 맞는 커피를 추천해드릴게요.
        </span>
      </div>
    </div>
    <div> 
      <!-- 성별 -->
      <b-form-group label="당신의 성별을 알려주세요" v-slot="{ ariaDescribedby }">
        <b-form-radio
          v-model="selected"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="남자"
          >남자</b-form-radio
        >
        <b-form-radio
          v-model="selected"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="여자"
          >여자</b-form-radio
        >
      </b-form-group>
      <!-- 연령대 -->
      <b-form-group label="당신의 연령대를 알려주세요" v-slot="{ ariaDescribedby }">
        <b-form-radio
          v-model="ageRange"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="10대"
          >10대</b-form-radio
        >
        <b-form-radio
          v-model="ageRange"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="20대"
          >20대</b-form-radio
        >
        <b-form-radio
          v-model="ageRange"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="30대"
          >30대</b-form-radio
        >
        <b-form-radio
          v-model="ageRange"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="40대"
          >40대</b-form-radio
        >
        <b-form-radio
          v-model="ageRange"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="50대"
          >50대</b-form-radio
        >
        <b-form-radio
          v-model="ageRange"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="60대 이상"
          >60대 이상</b-form-radio
        >
      </b-form-group>
      <!-- 선호하는 향 -->
      <b-form-group label="커피를 드실 때 선호하는 향을 선택해주세요" v-slot="{ ariaDescribedby }">
      <b-form-radio
          v-model="flavor"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="초콜릿향"
          >초콜릿향</b-form-radio
        >
      <b-form-radio
          v-model="flavor"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="고소한 견과류향"
          >고소한 견과류향</b-form-radio
        >
      <b-form-radio
          v-model="flavor"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="상큼한 과일향"
          >상큼한 과일향</b-form-radio
        >
      <b-form-radio
          v-model="flavor"
          :aria-describedby="ariaDescribedby"
          name="some-radios"
          value="상큼한 과일향"
          >상큼한 과일향</b-form-radio
        >
      </b-form-group>
      <!-- 산미 -->
      <div>
        <label for="range-2">커피를 드실 때 선호하는 산미의 정도를 선택해주세요</label>
        <b-form-input id="range-2" v-model="acid" type="range" min="0" max="10" step="1"></b-form-input>
        <div class="mt-2">{{ acid }} / 10</div>
      </div>
      <!-- 단맛 -->
      <div>
        <label for="range-2">커피를 드실 때 선호하는 단맛의 정도를 선택해주세요</label>
        <b-form-input id="range-2" v-model="sweet" type="range" min="0" max="10" step="1"></b-form-input>
        <div class="mt-2">{{ sweet }} / 10</div>
      </div>
      <!-- 바디감 -->
      <div>
        <label for="range-2">커피를 드실 때 선호하는 바디감의 정도를 선택해주세요</label>
        <b-form-input id="range-2" v-model="bodyRate" type="range" min="0" max="10" step="1"></b-form-input>
        <div class="mt-2">{{ bodyRate }} / 10</div>
      </div>
      <!-- 로스팅 -->
      <div>
        <label for="range-2">커피를 드실 때 선호하는 단맛의 정도를 선택해주세요</label>
        <b-form-input id="range-2" v-model="roast" type="range" min="0" max="10" step="1"></b-form-input>
        <div class="mt-2">{{ roast }} / 10</div>
      </div>
      <b-button variant="outline-primary">Submit</b-button>

    </div>
  </div>
  <TestResult></TestResult>
</template>

<script>
import TestResult from "./TestResult.vue";
export default {
  data(){
    return{
      gender : '',
      ageRange : '',
      flavor : '',
      acid : 0,
      sweet : 0,
      bodyRate : 0,
      roast : 0,
    }
  },
  components: {
    TestResult,
  },
};
</script>

<style>
.Frame {
  display: inline-flex;
  padding: 50px 180px;
  flex-direction: column;
  align-items: center;
  gap: 102px;
  background: #fff;
}
.Frame10 {
  display: flex;
  width: 1080px;
  flex-direction: column;
  align-items: center;
  gap: 50px;
}
.Frame9 {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  align-self: stretch;
}
.Frame9-title {
  width: 923px;
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
.Frame9-sub {
  width: 755px;
  color: var(--system-grey-600, #757575);
  text-align: center;
  font-family: Inter;
  font-size: 20px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  letter-spacing: 0.2px;
}
</style>
