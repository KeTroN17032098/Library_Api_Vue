<template>
    <v-app id="app">
        <v-main>
            <v-parallax src="http://localhost:8000/static/img/bg.webp" jumbotron height="1024">
                <v-container style="position: relative; top: 20%; margin-left: 40%; bottom:20%" class="text-xs-center"
                    color="white">
                    <v-layout row wrap class="text-xs-center">
                        <v-flex>
                            <v-card class="mx-auto" max-width="1000" height="800" color="#385F73" dark elevation="2">
                                <v-row>
                                    <v-col style="margin-top: 50px">
                                        <v-card-title class="text-white text-center">
                                            Login
                                        </v-card-title>
                                    </v-col>
                                </v-row>
                                <v-row style="margin-top: 10px;margin-bottom: 10px;">

                                    <v-col>
                                        <v-form style="width: 400px; height: 300px" ref="form">
                                            <div class="mx-3 text-white">
                                                <v-icon icon="mdi-account" color="#ffffff"></v-icon>
                                                userEmail
                                                <div class="mx-1">
                                                    <v-text-field placeholder="userEmail" v-model="userEmail"
                                                        :rules="[rules.required, rules.email]"></v-text-field>
                                                </div>
                                            </div>
                                            <div class="mx-3 text-white">
                                                <v-icon color="#ffffff" icon="mdi-lock"></v-icon>
                                                userPassword
                                                <div class="mx-1">
                                                    <v-text-field placeholder="userPassword" type="password"
                                                        v-model="userPassword" :rules="[rules.required]"
                                                        v-on:keyup.enter="loginSubmit"></v-text-field>
                                                </div>
                                            </div>

                                            <v-card-actions>
                                                <v-btn color="#ffffff" dark large block variant="outlined"
                                                    @click="loginSubmit">Login</v-btn>
                                            </v-card-actions>
                                            <v-card-actions>
                                                <v-btn color="#ffffff" dark large block variant="outlined"
                                                    @click="linktosignup">SignIn</v-btn>
                                            </v-card-actions>
                                            <v-card-actions>
                                                <v-img src="http://localhost:8000/static/img/nlogin1.png"
                                                :height="100" v-on:click="openPopup" />
                                            </v-card-actions>
                                            <v-card-actions>
                                                <v-img src="http://localhost:8000/static/img/glogin.png"
                                                :height="100"
                                                 v-on:click="loginSubmit" />
                                            </v-card-actions>
                                            <v-card-actions>
                                                <v-img
                                                :height="100"
                                                src="http://localhost:8000/static/img/kakao_login.png" v-on:click="loginSubmit" />
                                            </v-card-actions>
                                        </v-form>
                                    </v-col>
                                </v-row>
                            </v-card>
                        </v-flex>
                    </v-layout>
                </v-container>
            </v-parallax>
        </v-main>
    </v-app>

</template>
  
<script>
import { mapGetters } from 'vuex';
import { toast } from 'vue3-toastify'
export default {
    data() {
        return {
            userEmail: null,
            userPassword: null,
            rules: this.$store.state.ruleStore.rules
        };
    },
    computed: {
        ...mapGetters([
            'USER_ACCESS_TOKEN',
        ])
    },
    methods: {
        loginSubmit() {
            let saveData = {};
            saveData.email = this.userEmail;
            saveData.password = this.userPassword;

            this.$axios
                .post("http://localhost:8000/api/accounts/v1/login/", JSON.stringify(saveData), {
                    headers: {
                        "Content-Type": `application/json`,
                    },
                })
                .then((res) => {
                    console.log(res.status)
                    if (res.status === 200) {
                        // 로그인 성공시 처리해줘야할 부분
                        let payload = {}
                        payload.userEmail = res.data.user.email
                        payload.token = res.data.access_token
                        console.log(res)
                        this.$store.commit("login", payload)
                    }
                })
                .catch(error => {
                    toast.error(error.request.responseText,{
                        autoClose:1000,

                    })
                    console.log(error.request.response)
                })
                .finally(() => {
                    this.userEmail=""
                    this.userPassword=""
                })

        },
        linktosignup() {
            this.$router.push('signin')
        },
        openPopup() {
            window.open("http://localhost:8000/api/accounts/v1/sociallogin/kakao/login/",'popupView')
        }
    },
};
</script>