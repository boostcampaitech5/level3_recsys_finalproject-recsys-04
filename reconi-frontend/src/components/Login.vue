<template>
  <div class="w-full bg-white">
    <b-modal v-model="this.modalShow" size="lg" hide-footer title="JOIN Coffee Playlist">
      <JoinComponent 
      @closeModal="this.modalShow=!this.modalShow"/>
    </b-modal>
  </div>
  <div>
    <H1> Login </H1>
  </div>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Email address:"
        label-for="input-1"
        description="Input must be email form"
      >
        <b-form-input
          id="input-1"
          v-model="form.email"
          type="email"
          placeholder="Enter email"
          required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="input-group-2"
        label="Your Password:"
        label-for="input-2"
      >
        <b-form-input
          id="input-2"
          v-model="form.password"
          placeholder="Enter password"
          type="password"
          required
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">LOGIN</b-button>
      <b-button @click="this.modalShow= !this.modalShow" variant="outline-danger">JOIN</b-button>
    </b-form>
    <!-- 테스트임 -->
    <!-- <b-card class="mt-3" header="Form Data Result">
      <pre class="m-0">{{ form }}</pre>
    </b-card> -->
  </div>
</template>

<script>
import JoinComponent from './Join.vue';

export default {
  name: "login-component",
  data() {
    return {
      modalShow:false,
      form: {
        email: "",
        password: "",
      },
      show: true,
    };
  },
  components:{
    JoinComponent,
  },
  methods: {
    onSubmit(event) {
      event.preventDefault();
      // alert(JSON.stringify(this.form));
      this.$store.dispatch("LOGIN", this.form); // login action
      // this.$store.dispatch("GETCART");
    },
    onReset(event) {
      event.preventDefault();
      // Reset our form values
      this.form.email = "";
      this.form.name = "";
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    },
  },
};
</script>

<style></style>
