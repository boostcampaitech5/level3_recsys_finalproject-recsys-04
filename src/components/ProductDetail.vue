<template>
  <div class="container d-md-flex  align-items-stretch">
    <div id="content" class="p-4 p-md-5 pt-5" style="padding-bottom:0px">
      <h2 style="word-break: keep-all; text-align: center">
        {{ selectedBean?.title }}
      </h2>
      <h5
        class="mb-4"
        style="word-break: keep-all; text-align: center; color: gray"
      >
        {{ selectedBean?.roastery }}
      </h5>
      <p style="word-break: keep-all; text-align: center">
        {{ selectedBean?.description }}
      </p>
      <img
        :src="getImgUrl(selectedBean?.thumbnail)"
        alt="img"
        style="max-width: 100%; height: auto; display:block"
      />
    </div>
    <div>
      <nav id="sidebar">
        <div class="p-4 pt-5">
          <h4
            class="pb-4"
            style="color: black; word-break: keep-all; text-align: center"
          >
            원산지
          </h4>
          <h5
            class="pb-4"
            style="color: black; word-break: keep-all; text-align: center"
          >
            {{ selectedBean?.origins.join(", ") }}
          </h5>
          <ul class="list-unstyled components mb-5">
            <li class="pt-4">
              <h5 style="color: black">산미</h5>
              <p style="color: black">
                원두가 가지고 있는 신 맛의 정도를 나타냅니다.
              </p>
              <b-progress
                :value="selectedBean?.acidity"
                :max="10"
                variant="warning"
                show-value
                animated
              ></b-progress>
            </li>
            <li class="pt-4">
              <h5 style="color: black">단맛</h5>
              <p style="color: black">
                원두가 가지고 있는 단 맛의 정도를 나타냅니다.
              </p>
              <b-progress
                :value="selectedBean?.sweetness"
                :max="10"
                variant="primary"
                show-value
                animated
              ></b-progress>
            </li>
            <li class="pt-4">
              <h5 style="color: black">바디감</h5>
              <p style="color: black">
                커피가 입 안으로 들어왔을 때 주는 무게감을 나타냅니다.
              </p>
              <b-progress
                :value="selectedBean?.body"
                :max="10"
                variant="secondary"
                show-value
                animated
              ></b-progress>
            </li>
            <li class="pt-4">
              <h5 style="color: black">로스팅 포인트</h5>
              <p style="color: black">원두가 로스팅 된 정도를 나타냅니다.</p>
              <b-progress
                :value="selectedBean?.roasting_point"
                :max="10"
                variant="danger"
                show-value
                animated
              ></b-progress>
            </li>
            <ui> </ui>
          </ul>
        </div>
      </nav>
    </div>
  </div>

  <div class="pb-4">
    <div>
      <b-button
        block
        variant="primary"
        style="margin: 0 auto; display: flex; justify-content: center"
        v-if="!this.$store.getters.isInCart(selectedBean?.id)"
        @click="addCart(selectedBean?.id)"
      >
        내 취향 원두 리스트에 담기
      </b-button>
    </div>
    <div class="pt-4">
      <b-button
        :href="selectedBean?.purchase"
        target="_blank"
        block
        variant="outline-primary"
        style="margin: 0 auto; display: flex; justify-content: center"
      >
        {{ selectedBean?.roastery }} 로스터리로 구매하러 가기
      </b-button>
    </div>
  </div>
</template>

<script>
import beanImg from "../assets/product/sample-product.jpg";
import axios from "axios";

export default {
  name: "product-detail",
  props: {
    selectedBean: Object,
  },
  data() {
    return {
      beanImg: beanImg,
    };
  },
  methods: {
    getImgUrl(url) {
      if (typeof url == "string") {
        if (url.startsWith("/media")) {
          return "http://reconi-backend.kro.kr:30005/" + url;
        }
        if (!url.startsWith("http://reconi-backend.kro.kr:30005/")) {
          this.new_url = url.replace(
            "http://reconi-backend.kro.kr",
            "http://reconi-backend.kro.kr:30005"
          );
          return this.new_url;
        }
      } else {
        return "http://reconi-backend.kro.kr:30005/" + url;
      }
    },
    addCart(beanId) {
      if (this.$store.getters.isLogin) {
        axios
          .post(
            "http://reconi-backend.kro.kr:30005/api/v1/coffee-cart/add_to_cart/",
            { coffee_bean_id: beanId },
            {
              headers: {
                Authorization: `Bearer ${this.$store.state.token}`,
              },
            }
          )
          .then(() => {
            this.$store.commit("addUserCart", beanId);
          })
          .catch((e) => {
            console.log(e);
          });
      } else {
        alert("로그인을 먼저 진행해주세요!");
      }
    },
  },
};
</script>

<style scoped>
@import "./style.css";

</style>
