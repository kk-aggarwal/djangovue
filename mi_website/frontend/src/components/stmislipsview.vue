<template>
    <div id="app2">
        <div class="row" >
            <span class="col-md-12  text-center bg-secondar" >
                <h4>Stock charge MI Slips</h4>
            </span>

        </div>

        <div class="row bg-inf" >
            <div class="input-group">
                <div class="col-md-3 offset-2">
                    <label for="txtfinyear">Fin Year:</label>
                    <input type="text" class="form-control" :value="finyear" id="txtfinyear" disabled>
                </div>
                <div class="col-md-3">
                    <label for="mrrdate">Select MI Slip date:</label>
                    <vue-date-pick
                        id="mislipdate"
                        input_class="form-control"
                        v-model="dated"
                        :format="'MM-DD-YYYY'"

                    >

                    </vue-date-pick>
                </div>
                <!--<span class="input-group-btn" style="padding-top:30px"><button type="submit" class= "btn btn-info" @click="dateclicked">Submit</button></span>-->
            </div>

        </div>
        <div class="row bg-inf" >
            <div class="col-md-12   bg-secondar" >
            <ktable
                    ref="ktable"
                    :key="key_ktable"
                    :apiurl="apiurl"

                    :groupfields="false"
                    :use-detail-row="true"
                    @rowclicked="rowclicked"
                    rowcolor=""
                    :sortable="false"
                    :use-action-button="true"
                    forminputchange="handlemrrforminputchange"
                    :useprintbutton="false"
                    >

                 <template v-slot:detailrow="slotprops">


                <!-- Tab panes -->

                       <component :is="c[slotprops.index]"
                                  :key="key_c"
                                  :ref="'c_'+slotprops.index"
                                                 :apiurl="urlmislipitems"
                                                 :groupfields="false"
                                                 :use-detail-row="false"
                                                    :use-action-button="true"
                                                :sortable="false"

                                  rowcolor="lightgreen"

                                      >

                       </component>



                         </template>
                    </ktable>
        </div>
        </div>
    </div>
</template>

<script>
import ktable from '../../../../components/ktable-cmp.vue'
//import ktable from './ktable-cmp.vue'
import VueDatePick from '../../../../components/vuedatepick-cmp.vue'
import axios from 'axios'
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
  
export default {
    name:'stmislipsview',
    components:{ktable,VueDatePick},
    mounted:function(){
                    this.getstartinfo();
    },
    data:function(){return{api_root:api_root,finyear:'',c:[],key:[],dated:"",apiurl:'',key_ktable:1,key_c:1,urlmislipitems:'',currentindex:'',}},
    watch:{
        dated:function(){this.dateclicked();},
    },
    methods:{
        getstartinfo:function(){
                    console.log('start');
                    var url=this.api_root+"/mi/ajax/getcurrentyear";
                    axios.get(url)
                            .then((response) => {
                                //console.log(response);
                                this.finyear = response.data.stcurrentyear;
                                },function (error) {console.log(error);}
                        );
                },
        dateclicked:function(){
                    console.log('date clicked');
                    //this.key_index_ktable=1;
                    this.key_index_c=1;

                    this.apiurl=this.api_root+"/mi/ajax/stmislips?finyear="+this.finyear +"&dated="+this.dated;
                    this.key_ktable+=1;
        },
        rowclicked:function(item,index){
                    //console.log(item);
                    this.urlmislipitems='';
                    this.c[this.currentindex]='';
                    this.key_index_c+=1;
                    this.currentindex=index;

                     this.urlmislipitems=this.api_root+"/mi/ajax/stmislipitems?finyear="+item.finyear+"&mislipno="+item.mislipno+"&matgrp="+item.matgrp+"&docref="+item.misref;
                    //console.log(this.urlmislipitems);
                    this.c[index]=ktable;
                    this.key_index_c+=1;
        },
    },
    
}
</script>