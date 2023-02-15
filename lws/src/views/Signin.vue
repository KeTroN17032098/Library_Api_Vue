<template>
  <v-card class="mx-auto" max-width="500">
    <v-card-title class="text-h6 font-weight-regular justify-space-between">
      <span>{{ currentTitle }}</span>
      <v-divider></v-divider>
      <v-avatar color="primary" size="24" v-text="step"></v-avatar>
    </v-card-title>

    <v-window v-model="step">
      <v-window-item :value="1">
        <v-card-text>
          <v-form ref="form" lazy-validation>
            <v-text-field label="Email" placeholder="john@google.com" v-model="writtenEmail"
            onSubmit="return false;"
              :rules="[rules.required, rules.email]" v-on:keydown.enter.prevent="page1"></v-text-field>
          </v-form>
          <span class="text-caption text-grey-darken-1">
            This is the email you will use to login to your Vuetify account
          </span>
        </v-card-text>
      </v-window-item>

      <v-window-item :value="2">
        <v-card-text>
          <v-text-field label="Password" type="password" v-model="writtenPassword"
            :rules="[rules.required, rules.counter, rules.minvalue]"
            v-on:keydown.enter.prevent="signup"></v-text-field>
          <v-text-field label="Repeat Password" type="password" v-model="writtenRPassword"
            :rules="[rules.required, rules.counter, rules.minvalue]"
            v-on:keydown.enter.prevent="signup"></v-text-field>
          <span class="text-caption text-grey-darken-1">
            Please enter a password for your account
          </span>
        </v-card-text>
      </v-window-item>

      <v-window-item :value="4">
        <div class="pa-4 text-center">
          <v-img class="mb-4" contain height="128" src="https://cdn.vuetifyjs.com/images/logos/v.svg"></v-img>
          <h3 class="text-h6 font-weight-light mb-2">
            Welcome to Library Service
            <br>{{ writtenEmail }}
          </h3>
          <span class="text-caption text-grey">Thanks for signing up!
            <br>Email Verification my be needed.</span>
        </div>
      </v-window-item>

      <v-window-item :value="3">
        <div class="pa-4 text-center">
          <v-img class="mb-4" contain height="128" src="https://cdn.vuetifyjs.com/images/logos/v.svg"></v-img>
        </div>
      </v-window-item>
    </v-window>

    <v-divider></v-divider>

    <v-card-actions>
      <v-btn v-if="step == 2" variant="text" @click="step--">
        Back
      </v-btn>
      <v-btn v-if="step == 4" variant="text" @click="emailresend">
        Resend
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn v-if="step == 1" color="primary" variant="flat" @click="page1">
        Next
      </v-btn>
      <v-btn v-if="(step == 2)" color="primary" variant="flat" @click="signup">
        Sign-Up
      </v-btn>
      <v-btn v-if="(step == 4)" color="primary" variant="flat">
        To Login Page
      </v-btn>
    </v-card-actions>
  </v-card>
  <v-alert v-if="emb == true" type="error">Something is wrong</v-alert>
</template>

<script>
import { toast } from 'vue3-toastify'
export default {
  data() {
    return {
      step: 1,
      writtenEmail: '',
      writtenPassword: '',
      writtenRPassword: '',
      rules: this.$store.state.ruleStore.rules,
      emb: false,
      errormessage: ''
    }
  },

  computed: {
    currentTitle() {
      switch (this.step) {
        case 1: return 'Email'
        case 2: return 'Create a password'
        case 3: return 'Processing'
        default: return 'Welcome!'
      }
    },
  },
  methods: {
    page1() {
      console.log()
      if (typeof (this.rules.required(this.writtenEmail)) == 'string') {
        toast.error(this.rules.required(this.writtenEmail), {
          autoClose: 1000,
        })
      } else if (typeof (this.rules.email(this.writtenEmail)) == 'string') {
        toast.error(this.rules.email(this.writtenEmail), {
          autoClose: 1000,
        })
      } else {
        this.step++
      }
    },
    emailresend() {
      this.step--;
      let payload={}
      payload.email = this.writtenEmail
      this.$axios
          .post("http://localhost:8000/api/accounts/v1/registration/resend-email/", JSON.stringify(payload), {
            headers: {
              "Content-Type": `application/json`,
            },
          })
          .then((res) => {
            if (res.status === 200) {
              // 로그인 성공시 처리해줘야할 부분
              console.log(res)
              this.step++
            }
          })
          .catch(error => {
            this.step = 4
            toast.error(error.request.responseText, {
              autoClose: 1000,
            })
          })
    },
    signup() {
      let payload = {}
      payload.email = this.writtenEmail
      payload.password1 = this.writtenPassword
      payload.password2 = this.writtenRPassword
      if (this.writtenRPassword != this.writtenRPassword) {
        toast.error(this.rules.email(this.writtenEmail), {
          autoClose: 1000,
        })
      }
      else {
        this.step++
        this.$axios
          .post("http://localhost:8000/api/accounts/v1/registration/", JSON.stringify(payload), {
            headers: {
              "Content-Type": `application/json`,
            },
          })
          .then((res) => {
            if (res.status === 201) {
              // 로그인 성공시 처리해줘야할 부분
              console.log(res)
              this.step++
            }
          })
          .catch(error => {
            this.step = 1
            toast.error(error.request.responseText, {
              autoClose: 1000,
            })
          })
      }
    }
  }
}
</script>