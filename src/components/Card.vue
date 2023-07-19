<template>
  <div>
    <b-card
      :subtitle="bean?.roastery"
      img-src="https://picsum.photos/600/300/?image=25"
      img-alt="Image"
      img-top
      tag="article"
      style="max-width: 20rem;"
      class="mb-2"
      :style="styleObject"
    >
      <b-card-title>{{ bean?.title }}</b-card-title>
      <b-card-text>
        {{ bean?.description }}
      </b-card-text>

      <b-button variant="outline-primary">원두 보러가기</b-button>
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
      styleObject:{
        fontSize:'10px'
      }
    };
  },

};
</script>

<style>

</style>
