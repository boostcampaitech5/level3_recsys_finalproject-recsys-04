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

      <div>
        <b-button variant="outline-primary" @click="$emit('openModal', bean)"
          >원두 보러가기</b-button
        >
        <b-button variant="primary">담기</b-button>
      </div>
    </b-card>
  </div>
</template>

<script>
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
  },
};
</script>

<style></style>
