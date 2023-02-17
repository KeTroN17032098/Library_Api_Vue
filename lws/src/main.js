import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import axios from 'axios';
import { router } from './router/index.js'
import store from './store/index.js'
import Vue3Toasity from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';
import filters from './filter/customfilter';

loadFonts()

const app = createApp(App)
app.use(router)
app.use(Vue3Toasity)
app.use(store)
app.config.globalProperties.$axios = axios
app.config.globalProperties.$filters = filters
app.use(vuetify)
app.mount('#app')