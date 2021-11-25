<template>
     <div>
        <div class="row" >
            <span class="col-md-12  text-center bg-secondary" >
                <h4>Main store ledger</h4>
            </span>
        <!--
            <span class="col-md-1">
                <a class="nav-link" href="#"  >{% if request.username  %} {{ request.username }} {% else %} [['Log_in']] {% endif %}</a>
            </span>
        -->
        </div>

        <div class="row bg-inf" >
            <div class="col-md-3 ">
                       <label for="txtfinyear">Fin Year:</label>
                    <input type="text" class="input-sm form-control" :value=" finyear" id="txtfinyear" disabled>
                    </div>
                    <div class="col-md-3 ">
                        <b-form-group label="Pick Mat type" v-slot="{ ariaDescribedby }">
                      <b-form-radio-group
                        id="radio-group-1"
                        v-model="selected"
                        :options="options"
                        :aria-describedby="ariaDescribedby"
                        name="radio-options"
                      ></b-form-radio-group>
                   </b-form-group>
                    </div>
                        <div class="col-md-2 ">
                       <label for="txtstockno">Stock no:</label>
                    <input type="text" class="input-sm form-control" v-model="stockno" id="txtstockno">
                    </div>
                    <div class="col-md-1" style="padding-top:30px">
                        <button type="submit" class= "btn btn-info" @click="getledgerinfo" >Submit</button>

                    </div>
        </div>
    <!--
        <div class="row">
            <div class="col-md-3 ">
                <label for="txtdrwgno">Drawing No:</label>
                <input type="text" class="input-sm form-control" :value="drwgno" id="txtdrwgno" disabled>
            </div>
            <div class="col-md-6 ">
                <label for="txrdes">Description:</label>
                <input type="textarea" class="input-sm form-control" :value="des" id="txtdes" disabled>
            </div>
            <div class="col-md-1 ">
                <label for="txrdes">Group:</label>
                <input type="texta" class="input-sm form-control" :value="group" id="txtgroup" disabled>
            </div>
            <div class="col-md-1 ">
                <label for="txtunit">Unit:</label>
                <input type="texta" class="input-sm form-control" :value="unit" id="txtunit" disabled>
            </div>

        </div>
        <div class="row">
            <div class="col-md-3 ">
                <label for="txtbalance">Stock Bal:</label>
                <input type="text" class="input-sm form-control" :value="st_balance" id="txtbalance" disabled>
            </div>
        </div>
-->

<hr>
        <div class="row bg-inf offset-" >

            <ktable
                    ref="ktable"
                    :key="key_ktable"
                    :apiurl="apiurl"

                    :groupfields="false"
                    :use-detail-row="false"
                    rowclicked="rowclicked"
                    rowcolor=""
                    :sortable="false"
                    :use-action-button="true"
                    @forminputchange="handleledgerforminputchange"
                    :useprintbutton="false"
                    @tableparticularschanged="tableparticularsmodify"
                    @formmounted="formmounted"
                    @add_clicked="addclicked"
                    :displaytableparticulars="true"
                    >
                    <template v-slot:addtext>new</template>
                     <template v-slot:edittext>&nbsp;</template>
                 <template v-slot:deletetext>&nbsp;</template>
                    </ktable>
        </div>

    </div>

</template>

<script>
import ktable from '../../../../components/ktable-cmp.vue'
//import ktable from './ktable-cmp.vue'
import axios from "axios"
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
    
export default {
    name:"stledgerview",
    components:{ktable},
    mounted:function(){
      this.getstartinfo();
  },
    data:function(){
                  return {
                      api_root:api_root,
                      finyear:'',
                      apiurl:'',key_ktable:1,stockno:'',
                      selected: 'stock',
                      options: [
                      { text: 'Stock', value: 'stock' },
                      { text: 'Raw mat', value: 'raw' },
                            ],
                      des:'',drwgno:'',unit:'',group:'',st_balance:'',
                      doctype_choices:'',rec_issue:'',
                  }
            },
            watch:{
                rec_issue:function(){
                    this.status_update()
                },
                doctype_choices:function(){
                    this.status_update()
                },
                selected:function(){
                    this.apiurl='';
                    this.key_ktable+=1;
                    this.stockno='';

                },
                stockno:function(){
                    this.apiurl='';
                    this.key_ktable+=1;

                },

            },
            computed:{


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
                addclicked:function(){
                    //console.log('addclicked');
                    this.rec_issue='';
                    this.doctype_choices=''
                },
                formmounted:function(){
                    //console.log('form');
                    this.status_update();
                },
                status_update:function(){
                    //console.log('status update')
                    var s='';
                    if (this.rec_issue=='recpt'){
                        s=`<option value="3">MI</option> <option value="2">RN</option>
                                <option value="5">VA</option> <option value="4">RV</option>
                                <option value="6">SAV</option>
                                `;
                        this.doctype_choices=s;
                        this.$refs.ktable.$refs.mm1.$refs.ref_qtyout.disabled=true;
                       this.$refs.ktable.$refs.mm1.$refs.ref_qtyin.disabled=false;
                    }
                    if (this.rec_issue=='issue'){
                         s=`<option value="1">DN</option> <option value="5">VA</option><option value="6">SAV</option>`;
                        this.doctype_choices=s;
                        this.$refs.ktable.$refs.mm1.$refs.ref_qtyin.disabled=true;
                       this.$refs.ktable.$refs.mm1.$refs.ref_qtyout.disabled=false;
                    }
                    if (this.doctype_choices){
                        this.$refs.ktable.$refs.mm1.$refs.ref_doctype.disabled=false;
                    }else{
                        this.$refs.ktable.$refs.mm1.$refs.ref_doctype.disabled=true;
                    }
                    if(this.$refs.ktable.$refs.mm1.$refs.ref_doctype.value==5){
                         this.$refs.ktable.$refs.mm1.$refs.ref_qtyin.disabled=true;
                       this.$refs.ktable.$refs.mm1.$refs.ref_qtyout.disabled=true;

                    }

                },
                tableparticularsmodify:function(val){
                    //console.log('tttttbbgt');
                    if(val){
                    this.des=val.des;
                    this.group=val.matgroup;
                    this.st_balance=val.st_balance;}
                    else{
                      this.des='';
                      this.group='';
                      this.st_balance='';
                    }
                    },
                getledgerinfo:function(){
                    console.log('myself');
                    this.apiurl=this.api_root+"/mi/ledger?finyear="+ this.finyear +"&stockno="+this.stockno+"&mattype="+this.selected;
                    this.key_ktable+=1;
                    //console.log(this.$refs.ktable.tableparticulars['des'])
                    //this.des=this.$refs.ktable.tableparticulars.des
                },
                handleledgerforminputchange:function(e){
                    //console.log(e.target.name);
                    this.status_update()
                    var s='';
                    if(e.target.name=='rec_issu') {
                        //console.log(this.$refs.ktable.$refs.mm1.$refs.ref_qtyin.disabled);
                        if (document.getElementById('id_rec_issue_1').checked) {
                            s = `<option value="1">DN</option> <option value="2">RN</option>`;
                            this.doctype_choices = s;
                            this.$refs.ktable.$refs.mm1.$refs.ref_qtyout.disabled = true;
                        }
                        else if (document.getElementById('id_rec_issue_2').checked) {
                             s = `<option value="3">MI</option> <option value="5">VA</option>`;
                            this.doctype_choices = s

                        }
                    }
                        if (e.target.name == 'docno') {
                            //console.log(this.$refs.ktable.$refs.mm1.$refs.ref_docno.value);
                            var formdata=new FormData(document.getElementById('__form'));
                            //console.log(formdata.get('yearid'));

                             axios.get(this.api_root+"/mi/ajax/updatewon",
                                 {params:{'rec_issue':formdata.get('rec_issue'),'stockno':formdata.get('stockno'),'finyear':formdata.get('yearid'),'matgroup':formdata.get('groupid'),'doctype':formdata.get('doctype'),'docno':formdata.get('docno'),}})
                                    .then((response)=> {
                                 //console.log(response);
                                    if (formdata.get('doctype') === 5) {
                                        this.$refs.ktable.$refs.mm1.$refs.ref_docref.value = response.data.docref
                                        this.$refs.ktable.$refs.mm1.$refs.ref_qtyin.value = response.data.qtyin
                                        this.$refs.ktable.$refs.mm1.$refs.ref_qtyout.value = response.data.qtyout
                                        } else {

                                        this.$refs.ktable.$refs.mm1.$refs.ref_won.value = response.data.won;
                                        this.$refs.ktable.$refs.mm1.$refs.ref_warrant.value = response.data.warrant;
                                        this.$refs.ktable.$refs.mm1.$refs.ref_docref.value = response.data.docref
                                        }
                            },
                                 function(error){console.log(error);});

                        }
                        if (e.target.name == 'doctype'){
                            this.$refs.ktable.$refs.mm1.$refs.ref_docno.value="";
                             this.$refs.ktable.$refs.mm1.$refs.ref_won.value="";
                              this.$refs.ktable.$refs.mm1.$refs.ref_warrant.value="";
                               this.$refs.ktable.$refs.mm1.$refs.ref_docref.value="";
                        }
                },
            },
    
}
</script>