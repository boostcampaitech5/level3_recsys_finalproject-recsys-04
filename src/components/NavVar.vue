<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="light" class="bg-white">
      <b-navbar-brand router-link to="/">COFFEE PLAYLIST</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item class="mr-3" @click="mvPage('/')">Home</b-nav-item>
          <b-nav-item class="mr-3" @click="mvPage('/products')"
            >Products</b-nav-item
          >
          <b-nav-item
            v-if="!$store.getters.isLogin"
            href="#"
            @click="$emit('openLoginModal')"
            class="mr-3"
            >Login</b-nav-item
          >
          <b-nav-item v-else @click="onLogOut" class="mr-3">Logout</b-nav-item>
          <b-nav-item
            @click="
              if (!$store.getters.isLogin) this.$emit('openLoginModal');
              else this.$router.push(`/mypage/`);
            "
            class="mr-3"
            >MyPage</b-nav-item
          >
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "nav-var",
  data() {
    return {};
  },
  methods: {
    onLogOut() {
      this.$store.dispatch("LOGOUT"); // logout action
      this.$router.push("/");
    },
    mvPage(url) {
      axios
        .post("http://reconi-backend.kro.kr:30005/user/token/verify/", {
          token: this.$store.state.token,
        })
        .then(() => {
          this.$router.push(url);
        })
        .catch(() => {
          alert("다시 로그인 해주세요!");
          this.$store.commit("expireToken");  // logout
          localStorage.removeItem("accTkn");
          localStorage.removeItem("pk");
          localStorage.removeItem("cart");
        });
    },
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
