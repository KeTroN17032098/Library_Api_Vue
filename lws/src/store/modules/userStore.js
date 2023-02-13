import { router } from '@/router/index.js'

const userStore = {
    namespace: true,
    state: {
        userEmail: '',
        token: '',
    },
    getters: {
        USER_ACCESS_TOKEN: state => state.token,
        USER_EMAIL: state => state.userEmail,
    },
    mutations: {
        login: function(state, payload) {
            state.userEmail = payload.userEmail
            state.token = payload.token
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
        },
        signup: function(state, payload) {

        }
    }
}

export default userStore