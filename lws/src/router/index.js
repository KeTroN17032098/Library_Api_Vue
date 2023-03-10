import { createRouter, createWebHistory } from 'vue-router'

// 연결할 각 컴포넌트 import (src/views폴더 아래 컴포넌트들 생성해둠)
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import functions from './beFunctions.js'
import Signin from '../views/Signin.vue'
import SCallback from '../views/callback.vue'
import Board from '../views/board.vue'
// 라우터 설계
const routes = [
    { path: '/', component: Home, beforeEnter: functions.requireAuth, name: 'home' },
    { path: '/login', component: Login, name: 'login' },
    { path: '/signin', component: Signin, name: 'signin' },
    { path: '/callback/naver', component: SCallback, name: 'scallback_naver' },
    { path: '/callback/kakao', component: SCallback, name: 'scallback_kakao' },
    { path: '/callback/google', component: SCallback, name: 'scallback_google' },
    { path: '/board', component: Board, name: 'board', beforeEnter: functions.requireAuth },
]

// 라우터 생성
const router = createRouter({
    history: createWebHistory(),
    routes
});

// 라우터 추출 (main.js에서 import)
export { router }