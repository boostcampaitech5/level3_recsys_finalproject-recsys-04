<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="light" class="bg-white">
      <b-navbar-brand router-link to="/">Ducong</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item class="mr-3" router-link to="/">Home</b-nav-item>
          <b-nav-item class="mr-3" router-link to="/products">Products</b-nav-item>
          <b-nav-item href="#">About Us</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "nav-var",
  data() {
    return {};
  },

};
</script>

<style>

.navbar_control {
  height: 80px; /* Nav bar의 높이를 조정합니다 */
}
.font_size_control {
  font-family: Inter, "Source Sans Pro";
  font-size: 50px; /* Nav bar의 글씨 크기를 조정합니다 */
  padding-top: 30px; /* Nav bar의 글씨 위쪽 패딩을 추가합니다 */
  padding-bottom: 30px; /* Nav bar의 글씨 아래쪽 패딩을 추가합니다 */
}

</style>
