<template>
<div>
    <div class="row" >
        <span class="col-md-12  text-center bg-secondary" >
            <h4>View Add Edit POs</h4>
        </span>
    </div>
    <div class="row bg-inf" >
        <div class="col-md-2 offset-5">
           
                <b-form-select id="txtfinyear" v-model="selected" :options="options" size="sm" class="mt-3"></b-form-select>
        </div>
    </div>
    <div class="row bg-inf" >
        
        <div class="col-sm-12 ">
            <modal  ref="myModal" v-show="showModal"  v-on:close="showModal = false"  modalcontainer="modal-container-md">

                <component :key="formkey" v="component" ref="mm1" :is="mm"  v-on:close="showModal = false" @saveMe="authpo"  inputchange="handleinputchange" formmounted="formmountevent" groupdatasubmit="handlegroupdatasubmit"></component>

        <!--<v-runtime-template v-if="component" :template="compiledData.template" v-on:close="showModal = false" @saveMe="saveMe"></v-runtime-template>
        -->
            </modal>  
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
                    @forminputchange="handlepoforminputchange"
                    :useprintbutton="true"
                    :exportto="true"
                    :tablesearchable="false"
                    :softbutton1="true"
                    title_softbutton1="new Amendment"
                    
                    @formmounted="formmounted"
                    modalcontainersize="modal-container-lg"
            
            >
                <template v-slot:authstatus="slotprops" >
                    
                    <input type='checkbox' 
                    :checked="slotprops.item.authstatus==1?true:false" style='pointe-events: none;' 
                    @click.prevent.stop="checkpoauth(slotprops.item)"
                    :disabled="slotprops.item['pono']==0||slotprops.item['pono']==''||slotprops.item['items']==0||(slotprops.item['amemdments']==0 &&slotprops.item['amendno']>0)?true:false"
                    title="click to authorize PO!"
                    >
                </template>
                <template v-slot:addtext>new</template>
                <template v-slot:extraactionbuttons="ab">
                     <button  style="padding-to:20px" class="btn btn-primary btn-sm" @click.stop="addAmend(ab.item)" :disabled="ab.item.authstatus&&!(ab.item.pendingamendment)?false:true"> abc</button>
                </template>
                 <template v-slot:detailrow="slotprops">
                     <div style="border: solid black 2px;">
                         
                    <b-tabs content-class="mt-3">
                        <b-tab title="Items" active>
                            
                            <component :is="c[slotprops.index]"
                                    :key="key_c"
                                    :ref="'c_'+slotprops.index"
                                    :apiurl="urlpoitems"
                                    :groupfields="false"
                                    :use-detail-row="false"
                                    :use-action-button="!slotprops.item.authstatus"
                                    :sortable="false"
                                    @forminputchange="handleforminputchangeinmislipitems($event,slotprops.index)"
                                    rowcolor="lightgreen"
                                    modalcontainersize="modal-container-lg"

                                      >
                           
                       </component>
                        
                        </b-tab>
                        <b-tab title="MPRs">
                            <component :is="c2[slotprops.index]"
                                    :ref="'c2_'+slotprops.index"
                                    :key="key_c2"
                                    :apiurl="urlmprs"
                                    :groupfields="false"
                                    :use-detail-row="false"
                                    :sortable="false"
                                    :use-action-button="!slotprops.item.authstatus"
                                    @datachanged="datachanged(slotprops.index)"
                            >
                                <template v-slot:addtext>add MPR</template>
                            </component>

                        </b-tab>
                        <b-tab v-if="slotprops.item.amendno>0" title="Amendments">
                            <component :is="c1[slotprops.index]"
                                    :ref="'c1_'+slotprops.index"
                                    :key="key_c1"
                                    :apiurl="urlamendments"
                                    :groupfields="false"
                                    :use-detail-row="false"
                                    :sortable="false"
                                    :use-action-button="!slotprops.item.authstatus"
                                    @datachanged="datachanged(slotprops.index)"
                                    :softbutton1="true"
                                    title_softbutton1="Print"
                                    @softbutton1_clicked="softbutton1_clicked(slotprops.item)"
                            >
                                <template v-slot:addtext>add</template>
                            </component>

                        </b-tab>
    
                    </b-tabs>

                  </div>

                         </template>

                        

            </ktable>
           
        </div>
    </div>
     
    
</div>
</template>
<script>
import ktable from '../../../../components/ktable-cmp.vue'
import modal from '../../../../components/modal-cmp.vue'
//import VueDatePick from '../../../../components/vuedatepick-cmp.vue'
import axios from "axios"
//import $ from 'jquery'
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
  
export default {
    name: 'poview',
    components: {
    ktable,modal
    },
    mounted:function(){
      this.getstartinfo();
    },
    
    data:function(){
      return {
          showModal:false,
          mm:null,
          formkey:0,
          modal_content:'',
          mprno:null,
          apiurl_mpritems:'',
          mpritemskey:0,
            apiurl:'',  
            
            selected:null,

            options:[
            { value: null, text: 'Select Fin year' },
            { value: '2020-2021', text: '2020-2021' },
            { value: '2021-2022', text: '2021-2022' },
            ],
            api_root:api_root,
            urlamendments:'',
            urlpoitems:'',
            urlmprs:'',
            c:[],
            c1:[],
            c2:[],
            key_index_ktable:0,
            key_index_c:0,
            key_index_c1:0,
             key_index_c2:0,
            currentindex:'',
            suppcode:'asdfrtt'
            }
    },
    computed:{
                key_ktable:{
                    get:function(){return 'ktable'+this.key_index_ktable},
                    //set:function(newvalue){this.key_index_ktable=newvalue},
                },
                key_c:{
                    get:function(){return 'c'+this.key_index_c},
                    //set:function(newvalue){this.key_index_c1=newvalue},
                },
                key_c1:{
                    get:function(){return 'c1'+this.key_index_c1},
                   // set:function(newvalue){this.key_index_c=newvalue},
                },
                key_c2:{
                    get:function(){return 'c2'+this.key_index_c2},
                   // set:function(newvalue){this.key_index_c=newvalue},
                },
                compiledData:function(){return {template:`<div>${this.modal_content}</div>`,mounted:function(){console.log('sddfff');this.$emit('formmounted');}}
                },
      
                
    },
    methods:{
        authpo:function(){
                console.log('authpo');
                var action=this.$refs.mm1.$refs['myform'].action;
                var formdata=new FormData(document.getElementById('__form'));
                //formdata.forEach((key,value)=> console.log(value,key));
                var csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value;
            
                axios({method:'post',url:action, data:formdata,
                        headers: {
                            "X-CSRFToken": csrftoken,
                            'content-type': 'application/x-www-form-urlencoded'
                            
                        }

                        }).then(response=>{
                            //console.log(response.data);
                            this.modal_content = response.data.html_form;
                            this.mm='';
                            this.mm=this.compiledData;

                            //console.log(response.data.success);
                            if (response.data.success=='True'){
                                    this.$refs.ktable.refreshData();
                                    //this.$emit('datachanged');
                                    //this.component=false;
                                    this.showModal=false;
                                        }
                        })
                                .catch(response=>{console.log(response);});
        },
        checkpoauth:function(item){
            console.log(item)
            var msg='';
            `
            If Item.SubItems(1)pono = "" Or Item.SubItems(1) = 0 Or Item.SubItems(6) items = 0 Or (Item.SubItems(7)amendments = 0 And Item.SubItems(2) amendment > 0) Then
CheckPOData = False
`
            if(item['pono']==0||item['pono']==''||item['items']==0||(item['amemdments']==0 &&item['amendno']>0)){
                    console.log('false')
            }

            if (item.authstatus){
                msg="'PO will be de-authorized. Are you sure!"
            }else{
                 msg="'PO will be authorized. Are you sure!"
            }
            if (confirm(msg)) {
                console.log("You pressed OK!") ;
                axios.get(this.api_root+"/purchase/ajax/poauth/"+item['poid'])
                .then((response) => {
                                //console.log(response);
                                this.modal_content = response.data.html_form;
                                this.mm=this.compiledData;
                                //this.component=true;
                                this.showModal=true;

                    },function (error) {alert(error);}
                    );
            } else {
               console.log("You pressed cancel!") ;
            } 
        },
        mpritems_rowclicked:function(item,index){
            console.log('mpritems')
            console.log(item)
            console.log(index)
            this.$refs['c_'+this.currentindex].$refs.mm1.$refs.ref_stockno.value=item.stockno;
            this.$refs['c_'+this.currentindex].$refs.mm1.$refs.ref_des.value=item.itemdesig;
            this.$refs['c_'+this.currentindex].$refs.mm1.$refs.ref_mprno.value=item.mprno;
            this.$refs['c_'+this.currentindex].$refs.mm1.$refs.ref_unit.value=item.unit;
            this.$refs['c_'+this.currentindex].$refs.mm1.$refs.ref_drwgno.value=item.drwgno;
            this.$refs['c_'+this.currentindex].$refs.mm1.$refs.ref_qty.value=item.qty;
        },
        softbutton1_clicked:function(item){
            console.log('button1')
            var urlprint=this.api_root+"/purchase/ajax/poamendmentprint?poid="+item.poid;
            window.location.href=urlprint
        },
        addAmend:function(item){
            console.log(item);
            var url=this.api_root+"/purchase/ajax/amendpo?poid="+item.poid;
                    axios.get(url)
                            .then((response) => {
                                console.log(response);
                                if(response.data.success=='success'){
                                    this.$refs.ktable.refreshData()
                                }
                                },function (error) {console.log(error);}
                        );

        },
        getstartinfo:function(){
                    console.log('start');
                    var url=this.api_root+"/purchase/ajax/getcurrentyear";
                    axios.get(url)
                            .then((response) => {
                                console.log(response);
                                this.selected = response.data.stcurrentyear;
                                },function (error) {console.log(error);}
                        );
        },
        rowclicked:function(item,index){
                    //console.log(item);
                    this.urlpoitems='';
                    this.urlamendments='';
                    this.mprno=null;
                    this.c[this.currentindex]='';
                    this.c1[this.currentindex]='';
                    this.c2[this.currentindex]='';
                    this.key_index_c+=1;
                    this.key_index_c1+=1;
                    this.key_index_c2+=1;
                    this.mpritemskey+=1;
                    
                    this.currentindex=index;
                     this.urlpoitems=this.api_root+ '/purchase/ajax/poitems?poid='+item.poid;
                    //console.log(this.urlmislipitems);
                    this.c[index]=ktable;

                    this.urlamendments=this.api_root+ '/purchase/ajax/poamendments?poid='+item.poid;
                    this.c1[index]=ktable;

                    this.urlmprs=this.api_root+ '/purchase/ajax/pomprs?poid='+item.poid;
                    this.c2[index]=ktable;
                    

                    //this.keyktable+=1;
                    this.key_index_c+=1;
                    this.key_index_c1+=1;
                     this.key_index_c2+=1;
        },
        formmounted:function(){
                    console.log('form');
                    this.status_update();
        },
        status_update:function(){
            console.log('statusupdated');
            var el=this.$refs.ktable.$refs.mm1.$refs.suppcode_id;
            //var e = document.createElement('div'); e.innerHTML = 'abc'; 
            el.innerHTML='asssssssss  hhhhh hhhh    kkkkkk   kkkkkkk uuuuuuuuu';
            var amendno=document.getElementById('id_amendno')
            var divamend=document.getElementById('amend')
            if(amendno.value>0){
                    divamend.hidden=false
            }else{divamend.hidden=true}

            var potype=document.getElementById('id_potype')
            var divimport=document.getElementById('import')
            var divimporta=document.getElementById('importa')
            if(potype.value==2){
                    divimport.hidden=false;
                    divimporta.hidden=false;
            }else{
                divimport.hidden=true;
                divimporta.hidden=true;
            }
            
        },
        handlepoforminputchange:function(e){
                    console.log(e.target.name);
                    this.status_update()
        },
    },
    
    watch:{
        selected:function(val){
            this.apiurl=this.api_root+"/purchase/ajax/pos?finyear="+val
            this.key_index_ktable+=1
        },
        mprno:function(val){
            console.log(val);
            
            this.apiurl_mpritems=this.api_root+"/purchase/ajax/mpritems?mprno="+val
            this.mpritemskey+=1;
             console.log(this.apiurl_mpritems);
            this.$refs["c_"+this.currentindex].$refs.mm1.$refs.mpritems.refreshData()
            
        },
    },
    
}
</script>
