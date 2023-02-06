import { router } from '@/router/index.js'
const userStore = {
    namespace: true,
    state: {
        userEmail: '',
        token: '',
        rules: {
            required: value => !!value || 'Required.',
            counter: value => value.length <= 20 || 'Max 20 characters',
            minvalue: value => value.length >= 8 || 'At least 8 characters',
            email: value => {
                const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                return pattern.test(value) || 'Invalid e-mail.'
            },
        }
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