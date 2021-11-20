<template>
    <div class="row">
        <div class="col-md-12 offset bg-dange">
        <textsubmit
          :apiurl="api_root+'/mtpinfoshare/ajax/systems'"
          caption="Drawing no"
          type="label"
          inputtext='CNC Packages'
          resulthtml="<p>pl enter and submit to see the result here!</p>"
          @resultmodified="refresh1"
          :loadonstart="true"
        
        >
        
            <template  v-slot:resultslot="result">
                
                <div  v-for="(item,index) in result.result" :key="index">
                    <textsubmit
                        :key="index+=keyincrement1"
                        :apiurl="item.apiurl"
                        type="label"
                        :inputtext="item.inputtext"
                        @resultmodified="refresh2"
                    >
                        <template  v-slot:resultslot="result">
                            <div  v-for="(item,index) in result.result" :key="index">
                                <textsubmit
                                    :key="index+=keyincrement2"
                                    :apiurl="item.apiurl"
                                    type="label"
                                    :inputtext="item.inputtext"
                                >
                                </textsubmit>
                            </div>
                        </template>
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
  name: 'cncpackages',
  components: {
    textsubmit
    
  },
  data:function(){
    return{api_root:api_root,keyincrement1:1,keyincrement2:1}
  },

  methods:{
    refresh1:function(){
      this.keyincrement1+=1
      //this.result=[]
      //console.log(r)
      //this.result=r
      //this.abc=true
    },
    refresh2:function(){
      this.keyincrement2+=1
      //this.result=[]
      //console.log(r)
      //this.result=r
      //this.abc=true
    },
  },
}
</script>