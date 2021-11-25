
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
import mi from './components/mi.vue'
import mislips from './components/mislips.vue'
import products from './components/products.vue'
import mainstore from './components/mainstore.vue'
import stledgerview from './components/stledgerview.vue'
const routes = [
  { path: '/', components: {default:mi, }},
  { path: '/mislips', components: {default:mislips, }},
  {path: '/products', components: {default:products,}},

  {path: '/mainstore', components: {default:mainstore,
                                    ledger:stledgerview,
                                    }
                },

  
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
