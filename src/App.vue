<template>
  <div class="w-full bg-white">
    <b-modal v-model="this.modalShow" size="lg" hide-footer>
      <LoginComponent />
    </b-modal>
  </div>

  <NavVar @openLoginModal="
  this.modalShow = !this.modalShow;"></NavVar>
  <router-view></router-view>
  <Footer></Footer>
</template>

<script>
import NavVar from "./components/NavVar.vue";
import Footer from "./components/Footer.vue";
import LoginComponent from "./components/Login.vue";
import { ref, onMounted } from "vue"
import axios from 'axios';
import { useStore } from 'vuex';

export default {
  name: "App",
  components: {
    NavVar,
    Footer,
    LoginComponent,
  },
  setup(){
    const store = useStore()
    var modalShow = ref(false);

    onMounted(()=>{
      console.log('------------------')
      console.log(store.state.token)
      if (store.getters.isLogin){
        axios.get('http://reconi-backend.kro.kr:30005/api/v1/coffee-beans/user_cart_ids/', {
          headers: {
            Authorization: `Bearer ${store.state.token}`
          }
        }).then((getted)=>{
          store.commit('setUserCart', getted.data.user_item_ids);
          localStorage.setItem("cart", getted.data.user_item_ids);
        }).catch((e)=>{
          console.log(e);
        })
      }
    })

    return {
      modalShow
    }
  }

};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
