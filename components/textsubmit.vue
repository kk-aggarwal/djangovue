<template>
    <div>
        <div class="row bg-inf">
                <div class="col-md-4" v-if="(type=='text')">
                    <label for="txtText" >Enter {{textlabel}}:</label>
                    <div  >
                        <input type="text" class="form-control"  id="txtText" v-model="text" placeholder="Enter">
                    </div>

                </div>
                    <div class="col-md-4" v-if="type=='date'">
                        <label for="txtText" >Enter {{textlabel}}:</label>
                        <vue-date-pick
                        id="txtText"
                        input_class="form-control"
                        v-model="text"
                        :format="'DD-MM-YYYY'"
                        :inputAttributes="{readonly: true}"

                    >

                    </vue-date-pick>
                    
                    </div>
                     <div class="col-md-12" v-if="type=='label'">
                            <a href="" id="label" @click.prevent="submitText($event)"  v-html="text"></a>
                     </div>
            
              
           <div class="col-md-2">
               
                <button v-if="!('label'==type)" style="margin-top:30px" type="submit" class= "btn btn-info" @click="submitText($event)" >Submit</button>

           </div> 
          
        </div>
        <div style="padding-left:30px;" class="col-md-12" v-if="display=='self'">
            
            
            <slot name='resultslot' :result="result">
                <template  v-for="(item, index) in result">
                    <div :key="index" v-html="item"> </div>
                    
                </template>
            </slot>
        </div>
        
    </div>

</template>

<script>
import axios from "axios"
import VueDatePick from '../components/vuedatepick-cmp.vue'

export default {
    name:'textsubmit',
    components:{VueDatePick},
    mounted:function(){
        this.el= document.getElementById(this.display);
        this.display="off"
        if(this.loadonstart){this.submitText()}

        
        

    },
    created:function(){
        if (this.type=='date'){
        var today = new Date();
        var date = String(today.getDate()).padStart(2, '0')+'-'+String(today.getMonth()+1).padStart(2, '0')+'-'+today.getFullYear();
        this.text=date
        this.textlabel="date"
        
        }
        this.result.push(this.resulthtml)
    },
    data:function(){
        return{
            el:'',
            text:this.inputtext,
            result:[],
            textlabel:this.caption,
            
            }
    },
    props:{
        loadonstart:{
            type:Boolean,
            default:false
        },
        display:{
            type: String,
            default:'self'
        },
        resulthtml:{
            type: String,
            default:'<p>pl enter and submit to see the result here!</p>'
        },
        inputtext:{
            type: String,
            default:''
        },
        caption:{
            type: String,
            default:''
        },
        apiurl:{
            type: String,
            default:''
        },

    type:{
            type: String,
            default:'text'  //or 'date' or 'label'
        },
    },
    watch:{
        text:function(){
            if (this.type=='date'){
                this.display="self";
            this.submitText();
            }
        },
    },
    computed:{
        
    },
    
    methods:{
        displayResult:function(){
            var r='';
            for( var i of this.result){
                r=r+'<div>'+i+'</div>'
            }
            this.el.innerHTML= r
        },
        submitText:function(){
            if (this.display=='self'){
                this.display="off";
                return;
            }else{this.display="self";}
           this.result=[]
            if (this.text!=''){
                //this.result="<a href=''>fgggg</a>"

                var url=''
                if (this.type=='label'){
                 url=this.apiurl

            }else{
                url=this.apiurl+"?text=" + this.text
            }

            axios.get(url)
                .then((response) => {
                                //console.log(response.data.result)
                                this.result=[];
                                for (var item of response.data.result){
                                   // console.log(item)
                              this.result.push(item)}
                              this.$emit('resultmodified',this.result)
                              if(this.display!='self'){
                                        this.displayResult();
                              }
                               
                   },function (error) {alert(error);}
                    );
            }
            
        },

    },
}
</script>