<template>
    <div class="row">
        <div class="col-md-12 offset bg-dange">
        <textsubmit
        
          :apiurl="api_root+'/mtpinfoshare/ajax/oplayout'"
          caption="Drawing no"
          resulthtml="<p>pl enter and submit to see the result here!</p>"
          @resultmodified="refresh"
        >
        <template  v-slot:resultslot="result">
          <div  v-for="(item,index) in result.result" :key="index">
            <textsubmit
              :key="index+=keyincrement"
              :apiurl="item.apiurl"
              type="label"
              :inputtext="item.inputtext"
            >
            </textsubmit>
          </div>
        </template>
        </textsubmit>

        

        
        </div>
    </div>
</template>
<script>
import textsubmit from '../../../../components/textsubmit.vue'
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
 

export default {
  name: 'oplayout',
  components: {
    textsubmit
    
  },
  data:function(){
    return{api_root:api_root,keyincrement:1}
  },
  methods:{
    refresh:function(){
      this.keyincrement+=1
      //this.result=[]
      //console.log(r)
      //this.result=r
      //this.abc=true
    },
  },
}
</script>