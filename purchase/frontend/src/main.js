//npm install bootstrap@4.6.0 bootstrap-vue@2.21.2
//npm install vue-router

import Vue from 'vue';


import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import VueRouter from 'vue-router'


import App from './App.vue'
// Import Bootstrap an BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.config.productionTip = false

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(VueRouter)
import ktable from '../../../components/ktable-cmp.vue'
Vue.component('ktable', ktable)

import poview from './components/poview.vue'
const routes = [
  { path: '/po', components: {default:poview, }},
]
const router = new VueRouter({
  routes // short for `routes: routes`
})
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
