<template>
  <div class="container d-md-flex align-items-stretch">
    <!-- Page Content -->
    <div id="content" class="p-4 p-md-5 pt-5">
      <h2 class="mb-4">당신이 찾는 모든 커피</h2>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
      </p>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
      </p>
      <b-container class="bv-example-row">
        <b-row class = "pt-5" v-for="num in 10" :key="num">
          <b-col v-for="n in 3" :key="n"> <Card/> </b-col>
        </b-row>
      </b-container>
    </div>

    <nav id="sidebar">
      <div class="p-4 pt-5">
        <h5>Filter</h5>
        <ul class="list-unstyled components mb-5">
          <li>
            <a>
              신맛
            </a>
            <b-form-input id="range-1" v-model="value" type="range" min="1" max="5" class="scroll"></b-form-input>
          </li>
          <li>
            <a>단맛</a>
            <b-form-input id="range-1" v-model="value" type="range" min="1" max="5" class="scroll"></b-form-input>
          </li>
          <li>
            <a>바디감</a>
            <b-form-input id="range-1" v-model="value" type="range" min="1" max="5" class="scroll"></b-form-input>
          </li>
          <li>
            <a>로스팅</a>
            <b-form-input id="range-1" v-model="value" type="range" min="1" max="5" class="scroll"></b-form-input>
          </li>
        </ul>
        <div class="mb-5">
          <h5>원산지</h5>
          <div class="tagcloud">
            <a href="#" class="tag-cloud-link">dish</a>
            <a href="#" class="tag-cloud-link">menu</a>
            <a href="#" class="tag-cloud-link">food</a>
            <a href="#" class="tag-cloud-link">sweet</a>
            <a href="#" class="tag-cloud-link">tasty</a>
            <a href="#" class="tag-cloud-link">delicious</a>
            <a href="#" class="tag-cloud-link">desserts</a>
            <a href="#" class="tag-cloud-link">dish</a>
            <a href="#" class="tag-cloud-link">menu</a>
            <a href="#" class="tag-cloud-link">food</a>
            <a href="#" class="tag-cloud-link">sweet</a>
            <a href="#" class="tag-cloud-link">tasty</a>
            <a href="#" class="tag-cloud-link">delicious</a>
            <a href="#" class="tag-cloud-link">desserts</a>
          </div>
        </div>

      </div>
    </nav>
  </div>
</template>

<script>
import Card from './Card.vue';

export default {
  name: "products-main",
  components:{
    Card,
  }
};
</script>

<style scoped>
@import './style.css';

h5{
  color:black
}
</style>
