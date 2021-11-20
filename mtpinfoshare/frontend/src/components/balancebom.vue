<template>
    <div >
        
        <textsubmit
        :apiurl="api_root+'/mtpinfoshare/ajax/balancebom'"
        caption="Stock No"
        
        ></textsubmit>
        
    </div>
</template>
<script>
import textsubmit from '../../../../components/textsubmit.vue'
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
 

export default {
  name: 'balancebom',
  components: {
    textsubmit
    
  },
  data:function(){
    return{api_root:api_root}
  },
}
</script>