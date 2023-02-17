import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'


import userStore from './modules/userStore'
import ruleStore from './modules/ruleStore'
import boardStore from './modules/boardStore'

const store = new createStore({
    modules: {
        userStore: userStore,
        ruleStore: ruleStore,
        boardStore: boardStore,
    },
    plugins: [createPersistedState({
        path: ['userStore']
    })]
})

export default store