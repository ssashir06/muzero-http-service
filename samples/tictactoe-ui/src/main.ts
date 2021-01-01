import Vue from 'vue'
import App from './App.vue'
import axios from 'axios';

// Initialize axios
axios.defaults.baseURL = "/api/";

// Initialize Vue
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
