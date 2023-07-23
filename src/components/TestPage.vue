<template>
  <section class="py-5">
    <div>
      <h1 class="fw-bolder">정확한 추천을 위해 당신에 대해 알려주세요.</h1>
      <p class="lead fw-normal text-white-50 mb-0">
        응답해주신 기록을 바탕으로 당신에게 꼭 맞는 커피를 추천해드릴게요.
      </p>
    </div>
    <div style="padding-left : 500px; padding-right : 500px; text-align: right;" class="justify-content-center">
      <Vueform :force-labels="true" v-model="this.formData" :endpoint="false" @submit="onSubmit">
         <template #empty>
           <FormSteps>
             <FormStep
               name="Step1"
               label="Step1"
               :elements="['gender', 'ageRange']"
             />
             <FormStep
               name="Step2"
               label="Step2"
               :elements="['age']"
             />
             <FormStep
               name="Step3"
               label="Step2"
               :elements="['favorite_scent']"
             />
             <FormStep
               name="Step4"
               label="Step3"
               :elements="['aroma', 'acidity', 'sweetness', 'body_feel', 'roasting_characteristics']"
             />
           </FormSteps>
   
           <FormElements>
             <RadiogroupElement name="gender" placeholder = "gender" view="blocks"
             :items="[ { value:'M', label:'남자' }, { value:'F', label:'여자' }  ]"
             label="당신의 성별을 알려주세요"/>
             <TextElement
                     name="age"
                     placeholder="0"
                     input-type="number"
                     :rules="[
                       'required',
                       'numeric',
                     ]"
                     autocomplete="off"
                     label="당신의 연령을 알려주세요"
                   />
   
             <RadiogroupElement name="favorite_scent" placeholder = "favorite_scent" view="blocks"
             :items="[ { value:'chocolate', label:'초콜릿향' }, { value:'nutty', label:'고소한 견과류향' }, { value:'fruity', label:'상큼한 과일향' }, { value:'floral', label:'은은한 꽃향' }]"
             label="커피를 드실 때 선호하는 향을 알려주세요"/>
   
             <SliderElement name="aroma" placeholder = "aroma" :defalut="5" :max="10" :min="0" :step="1"
             label="커피를 드실 때 선호하는 향미의 정도를 알려주세요"
             info="산미는 원두가 가지고 있는 향의 정도를 나타냅니다." show-tooltip="focus" tooltip-position="bottom"/>
             <SliderElement name="acidity" placeholder = "acidity" :defalut="5" :max="10" :min="0" :step="1"
             label="커피를 드실 때 선호하는 산미의 정도를 알려주세요"
             info="산미는 원두가 가지고 있는 신 맛의 정도를 나타냅니다." show-tooltip="focus" tooltip-position="bottom"/>
             <SliderElement name="sweetness" placeholder = "sweetness" :defalut="5" :max="10" :min="0" :step="1"
             label="커피를 드실 때 선호하는 단 맛의 정도를 알려주세요"
             info="단 맛은 원두가 가지고 있는 단 맛의 정도를 나타냅니다." show-tooltip="focus" tooltip-position="bottom"/>
             <SliderElement name="body_feel" placeholder = "body_feel" :defalut="5" :max="10" :min="0" :step="1"
             label="커피를 드실 때 선호하는 바디감의 정도를 알려주세요"
             info="바디감은 커피가 입 안으로 들어왔을 때 주는 무게감을 나타냅니다." show-tooltip="focus" tooltip-position="bottom"/>
             <SliderElement name="roasting_characteristics" placeholder = "roasting_characteristics" :defalut="5" :max="10" :min="0" :step="1"
             label="커피를 드실 때 선호하는 원두 로스팅의 정도를 알려주세요"
             info="로스팅은 원두를 가열하여 볶은 정도를 의미합니다." show-tooltip="focus" tooltip-position="bottom"/>
           </FormElements>
           <FormStepsControls />
         </template>
       </Vueform>


    </div>
    <div class="container px-4 px-lg-5 mt-5">
      <div
        class="row gx-4 gx-lg-5 row-cols-2 row-cols-md-3 row-cols-xl-4 justify-content-center"
      >
        <div class="col mb-5" v-for="bean in coldStart" :key="bean">
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
  <TestResult :beans="this.beans" v-if="this.test_done"></TestResult>
</template>

<script>
import TestResult from "./TestResult.vue";
import axios from "axios";
export default {
  data() {
    return {
      test_done: false,
      formData: {},
      beans: {},
    };
  },
  methods: {
    onSubmit() {
      console.log(this.formData);
      axios
        .post(
          "http://reconi-backend.kro.kr:30005/api/v1/coffee-beans/cold_start_recommended/",
          this.formData,
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.token}`,
            },
          }
        )
        .then((getted) => {
          this.test_done = !this.test_done;
          this.beans = getted.data;
          console.log(getted);
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
  components: {
    TestResult,
  },
};
</script>

<style scoped>
@import "./css/styles.css";

/* .Frame {
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

.Form-area {
  background-color: #f7f7f7;
  border-radius: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.b-form-group {
  margin-bottom: 20px;
}

/* 레인지 인풋 스타일 */
/*
b-form-input[type="range"] {
  width: 100%;
  -webkit-appearance: none;
  background-color: #f7f7f7;
  height: 10px;
  border-radius: 5px;
  outline: none;
  margin-top: 8px;
}

b-form-input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: #007bff;
  cursor: pointer;
}

/* Submit 버튼 스타일 */
/*
b-button {
  width: 100%;
} */
</style>
