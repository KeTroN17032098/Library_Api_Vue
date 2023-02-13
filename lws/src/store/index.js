import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'


import userStore from './modules/userStore'
import ruleStore from './modules/ruleStore'

const store = new createStore({
    modules: {
        userStore: userStore,
        ruleStore: ruleStore,
    },
    plugins: [createPersistedState({
        path: ['userStore']
    })]
})

export default store