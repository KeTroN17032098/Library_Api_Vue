import store from '@/store/index.js'
import axios from 'axios'

let requireAuth = function requireAuth(to, from, next) {
    let isverified = false
    console.log("Token Check")
    if (store.state.userStore.token != '') {
        let pd = {}
        pd.token = store.state.userStore.token
        axios.post(store.state.userStore.verifyurl, JSON.stringify(pd), {
                headers: {
                    "Content-Type": `application/json`,
                }
            })
            .then(res => {
                console.log("token verified")
                isverified = true
            })
            .catch(err => {
                console.log("token failed")
                if (store.state.userStore.refresh_token != '') {
                    let pd1 = {}
                    pd1.refresh = store.state.userStore.refresh_token
                    axios.post(store.state.userStore.refreshurl, JSON.stringify(pd1), {
                            headers: {
                                "Content-Type": `application/json`,
                            }
                        })
                        .then(res => {
                            store.state.userStore.token = res.data.access
                            isverified = true
                            console.log("refresh token verified")
                        })
                        .catch(err1 => {
                            console.log("refresh token failed")
                            isverified = false
                        })
                }
            })
    } else {
        isverified = false
    }
    console.log(isverified)
    if (isverified) {
        return next()
    } else {
        return next('/login')
    }
}


const functions = {
    requireAuth
}

export default functions