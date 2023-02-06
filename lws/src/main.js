import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import axios from 'axios';
import { router } from './router/index.js'
import store from './store/index.js'


loadFonts()

const app = createApp(App)
app.use(router)
app.use(store)
app.config.globalProperties.$axios = axios
app.use(vuetify)
app.mount('#app')