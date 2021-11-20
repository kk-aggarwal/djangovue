import Vue from 'vue/dist/vue.js';
import 'bootstrap/dist/css/bootstrap.min.css'
import  'jquery/src/jquery.js'
import 'bootstrap/dist/js/bootstrap.min.js'
import axios from "axios"
Vue.use(axios)
//axios.defaults.baseURL='http://localhost:8080/api/'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

import VueRouter from 'vue-router'

Vue.use(VueRouter)
import monitororderlists from './components/monitororderlists.vue'
import monitorshortagelists from './components/monitorshortagelists.vue'

const routes = [
  { path: '/', components: {default:monitororderlists, }},
  { path: '/monitorshortagelists', components: {default:monitorshortagelists, }},
  
]
const router = new VueRouter({
  routes // short for `routes: routes`
})

import App from './App.vue'
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
