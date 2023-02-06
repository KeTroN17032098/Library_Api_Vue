import store from '@/store/index.js'

let requireAuth = function requireAuth(to, from, next) {
    console.log("Hi")
    if (store.state.userStore.token != '') {
        return next()
    }
    next('/login')
}


const functions = {
    requireAuth
}

export default functions