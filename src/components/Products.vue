<template>
  <div class="w-full bg-white">
    <b-modal v-model="this.modalShow" size="lg" hide-footer>
      <template #modal-title>
      </template>
      <ProductDetail style="display:inline-flex" :selectedBean="this.selectedBean" />
      <!-- {{ this.selectedBean }} -->
    </b-modal>
  </div>
  <div class="container d-md-flex align-items-stretch">
    <!-- Page Content -->
    <div
      id="content"
      class="p-4 p-md-5 pt-5"
      @scroll="handleNotificationListScroll"
    >
      <h2 class="mb-4">당신이 찾는 모든 커피</h2>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </p>
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat. Duis aute irure dolor in reprehenderit in voluptate
        velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
        occaecat cupidatat non proident, sunt in culpa qui officia deserunt
        mollit anim id est laborum.
      </p>

      <b-container
        class="bv-example-row mr-4"
        style="display: flex; flex-wrap: wrap; justify-content: space-around"
      >
        <Card
          v-for="bean in bean_data"
          @openModal="
            this.modalShow = !this.modalShow;
            this.selectedBean = $event;
          "
          :key="bean"
          :bean="bean"
          style="width: 250px"
          class="mt-4"
        />
      </b-container>

      <b-button
        block
        variant="primary"
        @click="handleNotificationListScroll"
        class="mt-4"
        >더 많은 원두 보기</b-button
      >
    </div>

    <nav id="sidebar">
      <div class="p-4 pt-5">
        <h5>Filter</h5>
        <ul class="list-unstyled components mb-5">
          <li>
            <a> 신맛 </a>
            <VueSlider v-model="acidRange" :max="10" :min="0" :enable-cross="false" :interval="1"  sync>
            </VueSlider>
          </li>
          <li>
            <a>단맛</a>
            <VueSlider v-model="sweetyRange" :max="10" :min="0" :enable-cross="false" :interval="1"  sync>
            </VueSlider>
          </li>
          <li>
            <a>바디감</a>
            <VueSlider v-model="bodyRange" :max="10" :min="0" :enable-cross="false" :interval="1"  sync>
            </VueSlider>
          </li>
          <li>
            <a>로스팅</a>
            <VueSlider v-model="roastRange" :max="10" :min="0" :enable-cross="false" :interval="1"  sync>
            </VueSlider>
          </li>
        </ul>
        <div class="mb-5">
          <h5>카페인 여부</h5>
          <div class="tagcloud mt-4">
            <a
              href="#"
              class="tag-cloud-link"
              v-for="decaf in ['디카페인']"
              :key="decaf"
              >{{ decaf }}</a
            >
          </div>
        </div>
        <div class="mb-5">
          <h5>원산지</h5>
          <div class="tagcloud mt-4">
            <a
              href="#"
              class="tag-cloud-link"
              v-for="origin in this.origins"
              :key="origin"
              >{{ origin }}</a
            >
          </div>
        </div>
        <div class="mb-5">
          <h5>로스터리</h5>
          <div class="tagcloud mt-4">
            <a
              href="#"
              class="tag-cloud-link"
              v-for="roastery in this.roasteries"
              :key="roastery"
              >{{ roastery }}</a
            >
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import Card from "./Card.vue";
import ProductDetail from "./ProductDetail.vue";
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  name: "products-main",
  components: {
    Card,
    ProductDetail,
  },
  data() {
    return {
      // filter info
      acidRange:[0, 10],
      sweetyRange:[0,10],
      bodyRange:[0,10],
      roastRange:[0,10],
    };
  },
  // composition API
  setup() {
    // 원두 정보
    var page = ref(0);
    var prev = ref("");
    var next = ref("");
    var bean_data = ref([]);

    var origins = ref([]);
    var roasteries = ref([]);

    // modal 정보
    var modalShow = ref(false);
    var selectedBean = ref(null);

    function getOrigins() {
      axios
        .get("http://reconi-backend.kro.kr:30005/api/v1/coffee-beans/unique_categories/")
        .then((getted) => {
          origins.value = getted.data.origin;
          roasteries.value = getted.data.roastery;
        })
        .catch(() => {
          console.log("실패😘");
        });
    }

    function getinitpage() {
      axios
        .get("http://reconi-backend.kro.kr:30005/api/v1/coffee-beans/?page=1&page_size=30")
        .then((getted) => {
          console.log(getted);
          prev.value = getted.data.previous;
          next.value = getted.data.next;

          // port number insert
          if (!next.value.startsWith('http://reconi-backend.kro.kr:30005')){
            next.value = next.value.replace('http://reconi-backend.kro.kr', 'http://reconi-backend.kro.kr:30005')
          }

          bean_data.value = bean_data.value.concat(getted.data.results);
        })
        .catch(() => {
          console.log("실패😘");
        });
    }
    function getNextPage() {
      axios
        .get(next.value)
        .then((getted) => {
          console.log(getted);
          prev.value = getted.data.previous;
          next.value = getted.data.next;

          // port number insert
          if (!next.value.startsWith('http://reconi-backend.kro.kr:30005')){
            next.value = next.value.replace('http://reconi-backend.kro.kr', 'http://reconi-backend.kro.kr:30005')
          }
          
          bean_data.value = bean_data.value.concat(getted.data.results);
          console.log("실행됨");
        })
        .catch((e) => {
          console.log("실패😘");
          console.log(e);
        });
    }

    function handleNotificationListScroll(e) {
      const { scrollHeight, scrollTop, clientHeight } = e.target;
      console.log(scrollHeight, scrollTop, clientHeight);
      const isAtTheBottom = scrollHeight === scrollTop + clientHeight;
      if (isAtTheBottom) {
        // setTimeout(() => getNextPage(), 1000);
        getNextPage();
      }
    }

    onMounted(() => {
      getOrigins();
      getinitpage();
    });

    return {
      origins,
      roasteries,
      page,
      bean_data,
      prev,
      next,
      modalShow,
      selectedBean,
      getNextPage,
      handleNotificationListScroll,
    };
  },
};
</script>

<style scoped>
@import "./style.css";

h5 {
  color: black;
}
</style>
