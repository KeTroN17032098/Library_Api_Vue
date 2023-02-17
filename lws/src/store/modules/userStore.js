import { router } from '@/router/index.js'

const userStore = {
    namespace: true,
    state: {
        userEmail: '',
        token: '',
        refresh_token: '',
        login_provider: '',
        verifyurl: 'http://localhost:8000/api/accounts/v1/token/verify/',
        refreshurl: 'http://localhost:8000/api/accounts/v1/token/refresh/',
    },
    getters: {
        USER_ACCESS_TOKEN: state => state.token,
        USER_REFRESH_TOKEN: state => state.refresh_token,
        USER_EMAIL: state => state.userEmail,
        USER_LOGIN_PROVIDER: state => state.login_provider
    },
    mutations: {
        login: function(state, payload) {
            state.userEmail = payload.userEmail
            state.token = payload.token
            state.refresh_token = payload.refresh_token
            state.login_provider = payload.login_provider
            router.push({
                name: 'home'
            }).catch(error => {
                console.log(error)
            })
        },
        logout: function(state) {
            state.userEmail = ''
            state.token = ''
            state.login_provider = ''
            state.refresh_token = ''
            router.push({
                name: 'login'
            })
        },
    }
}

export default userStore