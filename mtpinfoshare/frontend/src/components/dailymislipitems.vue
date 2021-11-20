<template>
    <div>
        <textsubmit
        :apiurl="api_root+'/mtpinfoshare/ajax/dailymislipitems'"
        caption="Stock No"
        type='date'
        ></textsubmit>
     </div>
</template>
<script>
import textsubmit from '../../../../components/textsubmit.vue'
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
 

export default {
  name: 'dailymislipitems',
  components: {
    textsubmit
    
  },
  data:function(){
    return{api_root:api_root}
  },
}
</script>