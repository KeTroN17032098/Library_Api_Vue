import { router } from '@/router/index.js'
import axios from 'axios'
import store from '..'


const boardStore = {
    namespace: true,
    state: {
        threadurl: "http://localhost:8000/api/board/v1/thread/",
        commenturl: "http://localhost:8000/api/board/v1/comment/",
        count: 0,
        nexturl: "",
        previousurl: "",
        threads: [],

    },
    getters: {
        BOARD_THREAD_URL: state => state.threadurl,
        BOARD_COMMENT_URL: state => state.threadurl,
    },
    mutations: {
        getThreads: function(state, pagenumber) {
            axios.get(state.threadurl, {
                    headers: {
                        "Content-Type": `application/json`,
                        "Authorization": "Bearer " + store.state.userStore.token
                    },
                    params: {
                        page_size: pagenumber || 1
                    }
                })
                .then((res) => {
                    if (res.status == 200) {
                        state.count = res.data.count
                        state.nexturl = res.data.next
                        state.previousurl = res.data.previous
                        state.threads = res.data.results
                        console.log(state.threads)
                    }
                })
                .catch((error) => {
                    console.log(error)
                })
        }

    }
}

export default boardStore