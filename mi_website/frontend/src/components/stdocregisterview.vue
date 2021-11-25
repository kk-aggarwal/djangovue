<template>
    <div>
        <div class="row bg-inf" >
            <span class="col-md-12  text-center bg-secondary" >
                <h4>Register documents</h4>
            </span>
        </div>
        <div class="row bg-inf" >
            <div class="col-md-3 ">
                <label for="txtfinyear">Fin Year:</label>
                <input type="text" class="input-sm form-control" v-model="finyear" id="txtfinyear" disabled>
            </div>
             <div class="col-md-2 ">
                 <label for="bselected">Mat Group:</label>
                 <b-form-select v-model="selected" :options="matgroups" id="bselected"/>
             </div>
        </div>
        <hr>
        <div class="row bg-inf" >
            <ktable
                        ref="ktabledocs"
                        :key="key_ktabledocs"
                        :apiurl="apiurldocs"
                        apiurl8='http://192.100.200.23:8033/mi/ajax/stdocregister/?yearid=2020-2021&groupid=2&docno=0&doctype=0'
                        :use-action-button="true"
                        :useprintbutton="false"
                        @formmounted="formmounted"
                        @add_clicked="addclicked"
                        :use-detail-row="true"
                        @rowclicked="rowclicked"
            >
                <template v-slot:edittext>&nbsp;</template>
                <template v-slot:deletetext>&nbsp;</template>
                <template v-slot:detailrow="slotprops">
                       <component :is="c[slotprops.index]"
                                  :key="key_c"
                                  :ref="'c_'+slotprops.index"
                                  :apiurl="apiurldocledger"
                                  :groupfields="false"
                                  :use-detail-row="false"
                                  :use-action-button="false"
                                  :sortable="false"
                                  rowcolor="lightgreen"
                        >             
                       </component>
                </template>
            </ktable>
        </div>
    </div>
</template>

<script>
import ktable from '../../../../components/ktable-cmp.vue'
//import ktable from './ktable-cmp.vue'
import axios from 'axios'

const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
  
export default {
            name:'stdocregisterview',
            components:{ktable},
            mounted:function(){
                    this.getstartinfo();
            },
            data:function(){
                return{
                     api_root:api_root,
                    finyear:'',matgroups:[],selected:'',key_ktabledocs:1,apiurldocs:'',key_ktabledocledger:1,apiurldocledger:'',doctype_choices:-1,c:[],key_c:1,currentindex:'',
                    options1: [
                            { value: 0, text: '0' },{ value: 1, text: '1' },{ value: 2, text: '2' },
                            { value: 3, text: '3' },{ value: 4, text: '4' },{ value: 5, text: '5' },
                            { value: 6, text: '6' },{ value:7, text: '7' },{ value: 8, text: '8' },
                            { value: 9, text: '9' },{ value: 10, text: '10' },{ value: 11, text: '11' },
                            { value: 12, text: '12' },{ value: 13, text: '13' },{ value: 14, text: '14' },
                            { value: 15, text: '15' },{ value: 16, text: '17' },{ value: 14, text: '18' },
                        { value: 15, text: '15' },{ value: 16, text: '17' },{ value: 14, text: '18' },
                            ],
                    
                    
                    
                }
        },
            watch:{

                selected:function(){
                   this.getstdocregisterinfo();
                },
                 doctype_choices:function(){
                    this.status_update()
                },
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
                    var url1=this.api_root+"/mi/ajax/getmatgroups";
                    axios.get(url1)
                            .then((response) => {
                                //console.log(response);
                                this.matgroups = response.data.matgroups;
                               // for(var c of matgroups){
                                //            this.matgroups.push({value:c.value,text:c.text});
                               // }
                                console.log(this.matgroups);
                                },function (error) {console.log(error);}
                        );
                },
                 addclicked:function(){
                    console.log('addclicked');
                    this.doctype_choices=-1;

                },
                formmounted:function(){
                    console.log('form');
                    this.status_update();
                },
                getstdocregisterinfo:function(){
                    this.apiurldocs=this.api_root+ "/mi/ajax/stdocregister?yearid="+ this.finyear +"&groupid="+this.selected+"&docno=0&doctype=0";
                    this.key_ktabledocs+=1;
                },
                status_update:function(){
                    console.log(this.doctype_choices);


                    if (this.doctype_choices=='6'){
                        this.$refs.ktabledocs.$refs.mm1.$refs.ref_warrant.readOnly=true;
                    }else{
                        this.$refs.ktabledocs.$refs.mm1.$refs.ref_warrant.readOnly=false;
                    }
                    if(this.doctype_choices!=-1) {
                        var a = this.$refs.ktabledocs.tableparticulars.maxdocs[this.finyear][this.selected][this.doctype_choices];
                        this.$refs.ktabledocs.$refs.mm1.$refs.ref_docno.value = a ? a : 1;
                    }

                },
                rowclicked:function(item,index){
                    //console.log(item);
                    this.apiurldocledger='';
                    this.c[this.currentindex]='';
                    this.key_c+=1;
                    this.currentindex=index;

                     this.apiurldocledger=this.api_root+ "/mi/ajax/stdocledger?yearid="+item.yearid+"&docno="+item.docno+"&groupid="+item.groupid+"&doctype="+item.doctype;
                    //console.log(this.urlmislipitems);
                    this.c[index]=ktable;
                    this.key_c+=1;
                },
        },
                

}
</script>