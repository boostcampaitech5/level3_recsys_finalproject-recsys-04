<template>
  <section class="py-5" v-if="this.step != 5">
    <div>
      <h1 class="fw-bolder">정확한 추천을 위해 당신에 대해 알려주세요.</h1>
      <h2 class="lead fw-normal mb-0" style="color: black">
        여러분의 취향을 파악하여 꼭 맞는 원두를 찾아드릴게요.
      </h2>
    </div>
    <div
      style="
        padding-top: 50px;
        margin-left: 500px;
        margin-right: 500px;
        /* border: 1.5px solid gray; */
        /* border-radius: 1rem; */
        /* text-align: right; */
      "
      class="justify-content-center"
    >
      <div v-if="this.step == 1">
        <h5>Step1</h5>
        <b-form-group
          id="fileset-1"
          label="당신은 남자인가요 여자인가요?"
          label-for="input-1"
          style="padding: 20px"
        >
          <b-form-radio-group
            id="input-1"
            v-model="this.formData.gender"
            :options="[
              { text: '남자', value: 'M' },
              { text: '여자', value: 'F' },
            ]"
            buttons
            button-variant="outline-primary"
            size="lg"
            style="padding-top: 30px"
          ></b-form-radio-group>
        </b-form-group>
        <b-button @click="this.step = 2"> next </b-button>
      </div>
      <div v-if="this.step == 2">
        <h5>Step2</h5>
        <b-form-group
          id="fileset-2"
          label="당신의 연령을 알려주세요"
          label-for="input-2"
          style="padding: 30px"
        >
          <b-form-input
            id="input-2"
            :type="number"
            v-model="this.formData.age"
            size="lg"
            :state="ageState"
          ></b-form-input>
          <b-form-invalid-feedback id="input-2">
            input must be number
          </b-form-invalid-feedback>
        </b-form-group>
        <b-container>
          <b-row>
            <b-col>
              <b-button @click="this.step = 1"> before </b-button>
            </b-col>
            <b-col>
              <b-button @click="this.step = 3"> next </b-button>
            </b-col>
          </b-row>
        </b-container>
      </div>
      <div v-if="this.step == 3">
        <h5>Step3</h5>
        <b-form-group
          id="fileset-3"
          label="커피를 드실 때 선호하는 향을 알려주세요"
          label-for="input-3"
          style="padding: 30px"
        >
          <b-form-radio-group
            id="input-3"
            v-model="this.formData.favorite_scent"
            :options="[
              { value: 'chocolate', text: '초콜릿향' },
              { value: 'nutty', text: '고소한 견과류향' },
              { value: 'fruity', text: '상큼한 과일향' },
              { value: 'floral', text: '은은한 꽃향' },
            ]"
            buttons
            button-variant="outline-primary"
            size="lg"
            style="padding-top: 30px"
          ></b-form-radio-group>
        </b-form-group>
        <b-container>
          <b-row>
            <b-col>
              <b-button @click="this.step = 2"> before </b-button>
            </b-col>
            <b-col>
              <b-button @click="this.step = 4"> next </b-button>
            </b-col>
          </b-row>
        </b-container>
      </div>
      <div v-if="this.step == 4">
        <h5 style="padding-bottom: 50px">Step4</h5>
        <h5>커피를 드실 때 선호하는 향미의 정도를 알려주세요</h5>
        <p>향미는 원두가 가지고 있는 향의 정도를 나타냅니다.</p>
        <VueSlider
          v-model="this.formData.aroma"
          :marks="true"
          :min="0"
          :max="10"
          :interval="1"
          style="padding-top: 50px; padding-bottom: 80px"
        >
        </VueSlider>
        <h5>커피를 드실 때 선호하는 산미의 정도를 알려주세요</h5>
        <p>산미는 원두가 가지고 있는 신 맛의 정도를 나타냅니다.</p>
        <VueSlider
          v-model="this.formData.acidity"
          :marks="true"
          :min="0"
          :max="10"
          :interval="1"
          style="padding-top: 50px; padding-bottom: 80px"
        >
        </VueSlider>
        <h5>커피를 드실 때 선호하는 단 맛의 정도를 알려주세요</h5>
        <p>단 맛은 원두가 가지고 있는 단 맛의 정도를 나타냅니다.</p>
        <VueSlider
          v-model="this.formData.sweetness"
          :marks="true"
          :min="0"
          :max="10"
          :interval="1"
          style="padding-top: 50px; padding-bottom: 80px"
        >
        </VueSlider>
        <h5>커피를 드실 때 선호하는 바디감의 정도를 알려주세요</h5>
        <p>바디감은 커피가 입 안으로 들어왔을 때 주는 무게감을 나타냅니다.</p>
        <VueSlider
          v-model="this.formData.body_feel"
          :marks="true"
          :min="0"
          :max="10"
          :interval="1"
          style="padding-top: 50px; padding-bottom: 80px"
        >
        </VueSlider>
        <h5>커피를 드실 때 선호하는 원두 로스팅의 정도를 알려주세요</h5>
        <p>로스팅정도는 원두를 가열하여 볶은 정도를 의미합니다.</p>
        <VueSlider
          v-model="this.formData.roasting_characteristics"
          :marks="true"
          :min="0"
          :max="10"
          :interval="1"
          style="padding-top: 50px; padding-bottom: 80px"
        >
        </VueSlider>
        <b-container>
          <b-row>
            <b-col>
              <b-button @click="this.step = 3"> before </b-button>
            </b-col>
            <b-col>
              <b-button variant="danger" @click="onSubmit"> submit </b-button>
            </b-col>
          </b-row>
        </b-container>
      </div>
    </div>
  </section>

  <TestResult
    :beans="this.beans"
    v-if="this.test_done && this.step == 5"
  ></TestResult>
</template>

<script>
import TestResult from "./TestResult.vue";
import axios from "axios";
export default {
  data() {
    return {
      test_done: false,
      step: 1,
      formData: {
        gender: "",
        age: "",
        favorite_scent: "",
        aroma: "0",
        acidity: "0",
        sweetness: "0",
        body_feel: "0",
        roasting_characteristics: "0",
      },
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
          this.step = 5;
          this.test_done = true;
          this.beans = getted.data;
          window.scrollTo(0, 0); // 페이지 최상단 이동
        })
        .catch((e) => {
          console.log(e);
        });
    },
  },
  components: {
    TestResult,
  },
  computed: {
    ageState() {
      var numberPattern = /^[0-9]+$/;
      return numberPattern.test(this.formData.age);
    },
  },
};
</script>

<style scoped>
@import "./css/styles.css";
</style>
