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
            :rules="[rules.required, rules.email]"></v-text-field>
          </v-form>
          <span class="text-caption text-grey-darken-1">
            This is the email you will use to login to your Vuetify account
          </span>
        </v-card-text>
      </v-window-item>

      <v-window-item :value="2">
        <v-card-text>
          <v-text-field label="Password" type="password" :rules="[rules.required, rules.counter,rules.minvalue]"></v-text-field>
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
      <v-btn v-if="(step > 1)&&(step < 3)" variant="text" @click="step--">
        Back
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn v-if="step ==1" color="primary" variant="flat" @click=page1>
        Next
      </v-btn>
      <v-btn v-if="(step == 2)" color="primary" variant="flat" @click="step++">
        Sign-Up
      </v-btn>
      <v-btn v-if="(step == 4)" color="primary" variant="flat">
        Resend
      </v-btn>
    </v-card-actions>
  </v-card>
  <v-alert
  v-if="emb==true"
        type="error"
        >Something is wrong</v-alert>
</template>

<script>
export default {
  data() {
    return {
      step: 1,
      writtenEmail: '',
      writtenPassword: '',
      rules: this.$store.state.userStore.rules,
      emb:false,
      errormessage: ''
    }
  },

  computed: {
    currentTitle() {
      switch (this.step) {
        case 1: return 'Email'
        case 2: return 'Create a password'
        case 3: return 'Processing'
        default: return 'Final Check'
      }
    },
  },
  methods: {
    page1(){
      console.log("dsa")
      const validate=this.$refs.form.validate()
      if(validate){
        this.emb=false
        this.errormessage=""
        this.step++
      }
      else{
        this.emb=true
        this.errormessage="Need to complete the validation"
      }
    },
    signup() {
      let payload = {}
      payload.Username = ''
      payload.Email = this.writtenEmail
      payload.Password1 = this.writtenPassword
      payload.Password2 = this.writtenPassword
      try {
        this.$axios
          .post("http://localhost:8000/api/accounts/v1/registration/", JSON.stringify(payload), {
            headers: {
              "Content-Type": `application/json`,
            },
          })
          .then((res) => {
            if (res.status === 200) {
              // 로그인 성공시 처리해줘야할 부분
              let payload2 = {}
              payload2.userEmail = res.data.user.email
              payload2.token = res.data.access_token
              console.log(res)
              this.$store.commit("signup", payload2)
            }
          });
      } catch (error) {
        console.error(error);
      }
    }
  }
}
</script>