<template>
  <div>
    <div class="row">
        <div class="col-md-12 offset bg-dange">
          <textsubmit
            :apiurl="api_root+'/mtpinfoshare/ajax/homiteminfo'"
            caption="Drawing No"
            
           >
           </textsubmit>
        </div>
        
       
    </div>
    <hr/>
        
         <hr/>
    <div class="row"></div>
    <div class="row">
       <div id="mydiv" class="bg-info"></div>
    </div>

  </div>
</template>
<script>
import textsubmit from '../../../../components/textsubmit.vue'
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
 

export default {
  name: 'homiteminfo',
  components: {
    textsubmit
    
  },
  data:function(){
    return{api_root:api_root}
  },
}
</script>