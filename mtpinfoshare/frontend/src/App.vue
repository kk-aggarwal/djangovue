<template>
  <div id="app">
    
     <router-view></router-view>
    
  </div>
</template>

<script>
//const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
 
//import textsubmit from '../../../components/textsubmit.vue'
export default {
  name: 'App',
  components: {
    //textsubmit
    
  },
  //data:function(){
   // return{api_root:api_root}
 // },
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: '';
  color: #2c3e50;
  margin-top: 10px;
}
</style>
