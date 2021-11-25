//npm install bootstrap@4.6.0 bootstrap-vue@2.21.2
//npm install vue-router

import Vue from 'vue'
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

import home from './components/home.vue'
import balancehom from './components/balancehom.vue'
import balancebom from './components/balancebom.vue'
import searchdatabase from './components/searchdatabase.vue'
import dailymislipitems from './components/dailymislipitems.vue'
import oplayout from './components/oplayout.vue'
import prodprogram from './components/prodprogram.vue'
import manpowerutilization from './components/manpowerutilization.vue'
import machineutilization from './components/machineutilization.vue'
import homiteminfo from './components/homiteminfo.vue'
import stocknodetail from './components/stocknodetail.vue'
import dailymrr from './components/dailymrr.vue'
import cncpackages from './components/cncpackages.vue'
import finddrwgno from './components/finddrwgno.vue'
const routes = [
  { path: '/', components: {default:home, }},
  { path: '/balancehom', components: {default:balancehom, }},
  { path: '/balancebom', components: {default:balancebom, }},
  { path: '/searchdatabase', components: {default:searchdatabase, }},
  { path: '/dailymislipitems', components: {default:dailymislipitems, }},
  { path: '/oplayout', components: {default:oplayout, }},
  { path: '/prodprogram', components: {default:prodprogram, }},
  { path: '/manpowerutilization', components: {default:manpowerutilization, }},
  { path: '/machineutilization', components: {default:machineutilization, }},
  { path: '/homiteminfo', components: {default:homiteminfo, }},
  { path: '/stocknodetail', components: {default:stocknodetail, }},
  { path: '/dailymrr', components: {default:dailymrr, }},
  { path: '/cncpackages', components: {default:cncpackages, }},
  { path: '/finddrwgno', components: {default:finddrwgno, }},

]
const router = new VueRouter({
 routes // short for `routes: routes`
})
new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
