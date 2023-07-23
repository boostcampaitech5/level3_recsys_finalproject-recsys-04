<template>
  <Vueform
    v-model="this.form"
    :endpoint="false"
  >
    <GroupElement name="personal_information" label="Your information">
      <TextElement
        name="nickname"
        placeholder="Nickname"
        rules="required|max:255"
        :columns="6"
        :debounce="300"
      />
      <!-- <b-button variant="danger" :columns="4">중복 확인</b-button> -->
      <ButtonElement name="checkNickName" :columns="3" @click="checkNickName">
        중복 확인
      </ButtonElement>
    </GroupElement>

    <GroupElement name="account_information" label="Account information">
      <TextElement
        name="email"
        placeholder="Email address"
        rules="required|email|max:255"
        :debounce="300"
        :columns="8"
      />
      <ButtonElement name="checkEmail" :columns="3" @click="checkEmail">
        중복 확인
      </ButtonElement>
      <TextElement
        name="password1"
        input-type="password"
        placeholder="Password"
        :debounce="300"
        :rules="['required', 'regex:/^(?=.*[a-z])(?=.*[0-9])(?=.{8,})/']"
        :messages="{
          regex:
            'The Password must at least 8 characters long and contain at least one number, one uppercase and one lowercase character.',
        }"
      />
      <TextElement
        name="password2"
        input-type="password"
        placeholder="Password again"
        rules="required"
      />
    </GroupElement>
    <ButtonElement
      name="register"
      add-class="mt-2"
      submits
      @click="if (onSend()) $emit('closeModal');"
    >
      Register
    </ButtonElement>
  </Vueform>

  <!-- 테스트임 -->
  <!-- <div>
    {{ this.form }}
    {{ nickname_validation }}
    {{ email_validation }}
  </div> -->
</template>

<script>
import axios from "axios";

export default {
  name: "main-join",
  data() {
    return {
      form: {},
      nickname_validation: false,
      email_validation: false,
    };
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
        .catch(() => {
          // alert(getted.response.data.detail);
          alert("해당 닉네임은 사용할 수 없습니다.");
          // this.nickname_validation = false;
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
        .catch(() => {
          alert("해당 이메일은 사용할 수 없습니다.");
          // alert(getted.response.data.detail);
          // this.email_validation = false;
          this.form.email = "";
        });
    },
    onSend() {
      if (!this.nickname_validation) {
        alert("닉네임 중복확인을 해주세요!");
        return false;
      }
      if (!this.email_validation) {
        alert("이메일 중복확인을 해주세요!");
        return false;
      }
      axios
        .post(
          "http://reconi-backend.kro.kr:30005/user/registration/",
          this.form
        )
        .then(() => {
          location.reload();
        })
        .catch((getted) => {
          console.log(getted)
          alert('중복 검사를 진행해주세요.');
        });
      return true;
    },
  },
};
</script>

<style></style>
