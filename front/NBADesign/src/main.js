// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import echarts from 'echarts'
import 'lib-flexible/flexible.js'
import { JSEncrypt } from 'jsencrypt'
Vue.use(ElementUI);
Vue.config.productionTip = false
import axios from 'axios'
axios.defaults.baseURL = "http://localhost:8082"


Vue.prototype.$ajax = axios
Vue.prototype.$echarts = echarts
Vue.use(ElementUI)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
