<template>
  <b-form @submit="onSend">
    <b-form-group
      label="Nickname"
      label-for="input-nickname"
      description="등록할 닉네임을 입력해주세요 (2자~8자)"
    >
      <div class="row">
        <div class="col-md-10">
          <b-form-input
            id="input-nickname"
            v-model="this.form.nickname"
            type="text"
            :state="nickNameState"
            placeholder="Enter nickname"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback">
            닉네임 중복 확인을 진행해주세요!
          </b-form-invalid-feedback>
        </div>
        <div class="col-md-2">
          <b-button variant="primary" class="pb-2" @click="checkNickName">
            중복 확인
          </b-button>
        </div>
      </div>
    </b-form-group>

    <b-form-group
      label="Email"
      label-for="input-email"
      description="등록할 이메일을 입력해주세요"
    >
      <div class="row">
        <div class="col-md-10">
          <b-form-input
            id="input-email"
            v-model="this.form.email"
            type="email"
            :state="this.emailState"
            placeholder="Enter email"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback">
            이메일 중복 확인을 진행해주세요!
          </b-form-invalid-feedback>
        </div>
        <div class="col-md-2">
          <b-button variant="primary" class="pb-2" @click="checkEmail">
            중복 확인
          </b-button>
        </div>
      </div>
    </b-form-group>

    <b-form-group
      label="Password"
      label-for="input-password"
      description="등록할 비밀번호을 입력해주세요"
    >
      <div class="row">
        <div class="col-md-8">
          <b-form-input
            id="input-email"
            v-model="this.form.password1"
            type="password"
            :state="passwordState"
            placeholder="Enter Password"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback">
            문자 1개와 숫자 1개를 포함하여 8자리 이상의 비밀번호를 입력해주세요.
          </b-form-invalid-feedback>
        </div>
      </div>
    </b-form-group>

    <b-form-group
      label="Password Confirm"
      label-for="input-password2"
      description="비밀번호를 다시 한 번 입력해주세요"
    >
      <div class="row">
        <div class="col-md-8">
          <b-form-input
            id="input-password2"
            v-model="this.form.password2"
            type="password"
            :state="passwordConfirmState"
            placeholder="Enter Password again"
            required
          ></b-form-input>
          <b-form-invalid-feedback id="input-live-feedback">
            위에서 입력한 Password를 한 번 더 입력해주세요
          </b-form-invalid-feedback>
        </div>
      </div>
    </b-form-group>
    <b-button type="submit" variant="outline-success"> Register </b-button>
  </b-form>

  <!-- 테스트임 -->
  <!-- <div>
    {{ this.form }}
    {{ nickname_validation }}
    {{ passwordConfirmState }}
  </div> -->
</template>

<script>
import axios from "axios";

export default {
  name: "main-join",
  data() {
    return {
      form: {
        nickname: "",
        email: "",
        password1: "",
        password2: "",
      },
      nickname_validation: false,
      email_validation: false,
    };
  },
  computed: {
    nickNameState() {
      return this.nickname_validation;
    },
    emailState() {
      return this.email_validation;
    },
    passwordConfirmState() {
      return this.form.password1 === this.form.password2;
    },
    passwordState(){
      const regex = /^(?=.*[a-zA-Z])(?=.*\d).{8,}$/;     // 문자열이 최소 1개의 문자와 1개의 숫자를 포함하고, 8자리 이상인지 확인
      return regex.test(this.form.password1);
    }
  },
  methods: {
    checkNickName() {
      axios
        .post(
          "http://reconi-backend.kro.kr:30005/user/registration/nickname-check/",
          {
            nickname: this.form.nickname,
          }
        )
        .then((getted) => {
          alert(getted.data.detail);
          this.nickname_validation = true;
        })
        .catch((getted) => {
          alert(getted.response.data.detail);
          this.form.nickname = "";
        });
    },
    checkEmail() {
      axios
        .post(
          "http://reconi-backend.kro.kr:30005/user/registration/email-check/",
          {
            email: this.form.email,
          }
        )
        .then((getted) => {
          alert(getted.data.detail);
          this.email_validation = true;
        })
        .catch((getted) => {
          alert(getted.response.data.detail);
          // alert("해당 이메일은 사용할 수 없습니다.");
          this.form.email = "";
        });
    },
    onSend() {
      axios
        .post(
          "http://reconi-backend.kro.kr:30005/user/registration/",
          this.form
        )
        .then(() => {
          location.reload();
        })
        .catch((getted) => {
          console.log(getted);
          alert("중복 검사를 진행해주세요.");
        });
    },
  },
};
</script>

<style></style>
