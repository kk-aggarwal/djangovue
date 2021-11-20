<template>
    <div class="row">
        <div class="col-md-12 offset bg-dange">
        <textsubmit
          :apiurl="api_root+'/mtpinfoshare/ajax/prodprogram'"
          caption="Drawing no"
          type="label"
          inputtext='prod program'
          resulthtml="<p>pl enter and submit to see the result here!</p>"
        
        >
        
        </textsubmit>

        

        
        </div>
    </div>
</template>
<script>
import textsubmit from '../../../../components/textsubmit.vue'
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
 

export default {
  name: 'prodprogram',
  components: {
    textsubmit
    
  },
  data:function(){
    return{api_root:api_root}
  },
}
</script>