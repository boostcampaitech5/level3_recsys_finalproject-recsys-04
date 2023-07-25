<template>
  <div>
    <b-card
      :subtitle="bean?.roastery"
      :img-src="getImgUrl(bean?.thumbnail)"
      img-alt="Image"
      img-top
      tag="article"
      style="max-width: 20rem"
      class="mb-2"
      :style="styleObject"
    >
      <b-card-title>{{ bean?.title }}</b-card-title>
      <b-card-text>
        {{ bean?.description }}
      </b-card-text>

      <b-container>
        <b-row class="text-center">
          <b-col cols="8">
            <b-button
              variant="primary"
              @click="$emit('openModal', bean)"
              >보러가기</b-button
            >
          </b-col>
          <b-col>
            <img
              v-if="!this.$store.getters.isInCart(bean?.id)" 
              @click="addCart(bean?.id)"
              src="../assets/card/unlike.png"
              alt="Like"
              style="width: 40px; height: 40px; cursor:pointer;"
            />
            <img
              v-else
              @click="removeFromCart(bean?.id)"
              src="../assets/card/like.png"
              alt="Like"
              style="width: 40px; height: 40px; cursor:pointer;"
            />
          </b-col>
        </b-row>
      </b-container>
    </b-card>

        <!-- <b-button v-if="!this.$store.getters.isInCart(bean?.id)" @click="addCart(bean?.id)" variant="primary">담기</b-button> -->

  </div>
</template>

<script>
import axios from "axios";
import Like from "../assets/card/like.png";
import Unlike from "../assets/card/unlike.png";

export default {
  name: "main-product-sample-card",
  props: {
    bean: Object,
  },
  data() {
    return {
      styleObject: {
        fontSize: "10px",
        modalShow: false,
        new_url: null,
        Like: Like,
        Unlike: Unlike,
      },
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
    },
    removeFromCart(beanId){
      axios.
        post(
          "http://reconi-backend.kro.kr:30005/api/v1/coffee-cart/remove_from_cart/",
          { coffee_bean_id : beanId},
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.token}`,
            },
          }
        )
        .then(() => {
          this.$store.commit("removeFromCart", beanId);
        })
        .catch((e) => {
          console.log(e)
        })
    }
  },
  components: {},
};
</script>

<style></style>
