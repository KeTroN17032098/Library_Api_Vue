import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'


import userStore from './modules/userStore'

const store = new createStore({
    modules: {
        userStore: userStore
    },
    plugins: [createPersistedState({
        path: ['userStore']
    })]
})

export default store