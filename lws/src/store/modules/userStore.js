import { router } from '@/router/index.js'

const userStore = {
    namespace: true,
    state: {
        userEmail: '',
        token: '',
        login_provider: '',
    },
    getters: {
        USER_ACCESS_TOKEN: state => state.token,
        USER_EMAIL: state => state.userEmail,
        USER_LOGIN_PROVIDER: state => state.login_provider
    },
    mutations: {
        login: function(state, payload) {
            state.userEmail = payload.userEmail
            state.token = payload.token
            state.login_provider = payload.login_provider
            router.push({
                name: 'home'
            }).catch(error => {
                console.log(error)
            })
        },
        loginCheck: function(state) {
            if (!state.token) {
                router.push({
                    name: 'login'
                }).catch(error => {
                    console.log(error)
                })
            }
        },
        logout: function(state) {
            state.userEmail = ''
            state.token = ''
            state.login_provider = ''
        },
        signup: function(state, payload) {

        }
    }
}

export default userStore