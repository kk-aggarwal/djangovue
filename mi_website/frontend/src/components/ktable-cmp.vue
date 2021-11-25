<template>
<div v-cloak>
<div class="col-sm-12 bg-primar">

    <div v-if="(caption=='')?false:true" class="row bg-secondar">
        <span  class="col-md-11 " style="float:left;background-colo:lightblue;text-align:center">[[caption]]</span>
     </div>

        <div  v-if="tableparticulars&&displaytableparticulars" class="row bg-dange">
            <div class="form-inline">
                <div class="col-sm-12 form-group ">
                    <template v-for="field,index in Object.keys(tableparticulars)">

                        <label class="col-sm-2 col-form-label" :for="field" :key="'l'+index" v-text="field+':'">:</label>
                        <input  type="text" rows="rows(field)" class="col-sm-2 form-control bg-in" :id="field" :value="tableparticulars[field]" disabled :key="'i'+index">

                    </template>
                </div>
            </div>
            <hr>
        </div>

    <!--
        <div  v-if="tableparticulars&&displaytableparticulars" >

                    <div class="card-columns">
                    <template v-for="field,index in Object.keys(tableparticulars)">
                        <div class="card ">
                            <div class="card-body">
                            <div class="card-title">
                                <label >[[field]]:</label>
                            </div>
                                <p class="card-text" v-text="tableparticulars[field]" ></p>
                            </div>
                        </div>
                    </template>
                    </div>

            </div>

        </div>
        -->
        <div class="row bg-warnin" >
            <div v-if="useActionButton&&urlcreate"  class=" col-md-1 d-inline-block">
                <button  style="padding-to:20px" class="btn btn-primary btn-sm" @click="addItem"> <slot name="addtext">add </slot></button>
            </div>
             <div v-if="tablesearchable&&tableData.length>0" class="offset-7  d-inline-block" >
                <span class="  input-group">
                    <label  class="  col-form-label" for="field">Field</label>
                    <select   class="col-md-3 form-control" id="searchfield" v-model="searchfield">
                        <template v-for="field,index in formFields" >
                            <option :key="index" v-text="field"></option>
                        </template>
                    </select>
                    <label  class=" col-form-label" for="search">search</label>
                    <input  type="text" class="col-md-3 form-control" id="searchtext" @input="searchtext($event)">
                </span>
             </div>

        </div>

    <!--<div class="col-md-4 offset-md-4">[[caption]]</div>-->
<div class="row bg-inf">
    <table class="   table   table-striped table-sm " style="margin-bottom:5px;margin-top:5px">
        <thead v-if="headervisible">
        <tr>
            <th v-if="useDetailRow"></th>
            <th v-if="useserialnos&&(tableData.length==0?false:true)">#</th>
            <template v-for="field,index in formFields">

                    <th @click.stop="onColumnHeaderClicked(field, $event)"

                    :key="index"
                        :id="'_' + field"

                    style="text-align:center;"
                    v-html="renderTitle(field)">

                    </th>

            </template>
            <th v-if="useActionButton&&(tableData.length==0?false:true)" :style="{width:useActionButton?'120px':'0px'}">Action</th>
        </tr>
        </thead>
 <tbody >


            <template  v-for="(item, itemindex) in tableData">
              <tr item-index="itemIndex"

                :key="'r'+itemindex"


                  :style="{'background-color':(item['rowcolor']=='default'?rowcolor:item['rowcolor'])}"
                  :class="{'active':isActive}"

                @click.stop="rowitemclicked(item,itemindex,$event)"
                dblclick="onRowDoubleClicked(item, itemindex, $event)"
                mouseover="onMouseOver(item, itemIndex, $event)"

              >
                        <td  v-if="tableexpandable"></td>
                      <td  v-if="useDetailRow&&!tableexpandable" class="ktable-expand" clas="{'highlight': (itemindex == selectedRow)}"  @click.stop="useDetailRow ?onRowClicked(item,itemindex,$event):''">
                          <a  href="javascript:void(0);"><chevronright width="20" v-if="d[itemindex]==''?false:true"></chevronright><chevrondown width="20" v-else></chevrondown></a>
                      </td>

                  <td v-if="useserialnos" :class="{'highlight': (itemindex == selectedRow)}">{{itemindex+1}} </td>
                <template v-for="(field, index) in formFields">
                    <td

                        :key="'r'+itemindex+'c'+index"
                        :class="{'highlight': (itemindex == selectedRow)}"
                        :style="{'text-align':align[field],'color':(item['fieldcolor'][field]=='default'?'black':item['fieldcolor'][field]),'width':width[field]}"
                        html="renderNormalField(field, item)"
                        click="onCellClicked(item, itemIndex, field, $event)"
                        dblclick="onCellDoubleClicked(item, itemIndex, field, $event)"
                        contextmenu="onCellRightClicked(item, itemIndex, field, $event)"
                    >


                        <slot :name="field" :item="item" :itemindex="itemindex" >
                            <div :style="groupfields?(ifprevioussame(field,item,itemindex)&&!(typeof item[field]=='boolean')?{'visibility': 'hidden'}:{'visibility':'visible'}):{'visibility':'visible'}">
                                <div v-html="renderNormalField(field, item,itemindex)"></div>
                            </div>
                        </slot>

                    </td>
                </template>
                  <td v-if="useActionButton" style="background-color:lightblue;" :style="{width:useActionButton?'120px':'0px'}">
                  <span class="align-self-center" v-if="useActionButton" >
                       <button class="btn bg-transparent  btn-sm" @click.stop="editItem(item,index,$event)"><slot name="edittext">E</slot></button>
                      <button class="btn bg-transparent  btn-sm" @click.stop="delItem(item,index,$event)"><slot name="deletetext">D</slot></button>

                    </span>
                      <span>
                          <slot name="printaction" :item="item" v-if="useprintbutton">
                              <button class="btn bg-transparent btn-default btn-sm" @click.stop="printItem(item,index,$event)"><slot name="printtext">P</slot></button>

                      </slot>
                      </span>
                  </td>
              </tr>



            <template v-if="useDetailRow">
                <transition name="detailRowTransition" :key="'t'+itemindex">
                    <tr class="detailrow"

                        :ref="'dr'+itemindex"
                        click="onDetailRowClick(item, itemIndex, $event)"

                        :style="{display:d[itemindex]}"
                        style="backgroun-color:yellow"
                    >
                        <td class="tddetailrow" ></td>
                        <td id="detailrow" class="tddetailrow" :colspan="countVisibleFields()+3" style="background-colo:yellow">
                            <slot name="detailrow" :item="item" :index="itemindex">

                            </slot>
                        </td>
                    </tr>
                </transition>
            </template>
        </template>
        <template v-if="summaryrow&&tableData.length>0" class="summaryrow">
            <tr class="bg-secondary">
                <td  v-if="useDetailRow&&tableData.length>0"></td>
                <td v-if="useserialnos&&tableData.length>0"></td>
                <template  v-for="(field, index) in formFields">
                    <td v-text="summary[field]" :style="{'text-align':align[field]}" :key="index"></td>
                </template>
            </tr>
             <tr class="bg-secondary">
                <td  v-if="useDetailRow&&tableData.length>0"></td>
                <td v-if="useserialnos&&tableData.length>0"></td>
                <template  v-for="(field, index) in formFields">
                    <td v-text="summaryinfo[field]" :style="{'text-align':align[field]}" :key="index"></td>
                </template>
            </tr>
        </template>
        </tbody>



    </table>

</div>
    <div v-if="!tableData.length==0&&exportto" class="row bg-inf">
        <div  class="col-md-1 offset-10" style="align:left;">
            <button  style="padding-to:20px" class="btn btn-secondary btn-sm" @click="ExportData">To Excel</button>
        </div>
    </div>
    <hr v-if="exportto" >
    <!--<button id="show-modal" @click="showModal = true">Show Modal</button> -->
      <!-- use the modal component, pass in the prop -->


      <modal  ref="myModal" v-show="showModal"  v-on:close="showModal = false" >

 <component :key="formkey" v-if="component" ref="mm1" :is="mm"  v-on:close="showModal = false" @saveMe_add="saveMe_add" @saveMe_edit="saveMe_edit" @inputchange="handleinputchange" @formmounted="formmountevent"></component>

<!--<v-runtime-template v-if="component" :template="compiledData.template" v-on:close="showModal = false" @saveMe="saveMe"></v-runtime-template>
-->
      </modal>

    <!-- <div> <button class="btn btn-info" type="button" v-on:click="refreshData()">Refresh</button></div> -->
</div>
</div>
</template>


<script>
import axios from "axios"
import XLSX from 'xlsx';
import chevrondown from './chevrondown.vue'
import chevronright from './chevronright.vue'
import modal from './modal-cmp.vue'

export default {
  name: 'ktable',
    delimiters: ['[[', ']]'],
    components:{chevrondown,chevronright,modal},

    props: {
        
        summaryrow:{
            type: Boolean,
            default: false
        },
        exportto:{
            type: Boolean,
            default: false
        },
        tablesearchable:{
            type: Boolean,
            default: false
        },
        apiurl:{
            type: String,
            default: ''
        },
        displaytableparticulars:{
            type: Boolean,
            default: false
        },
        loadOnStart: {
            type: Boolean,
            default: true
        },
        useDetailRow:{
            type: Boolean,
            default: false
        },
        useActionButton:{
            type: Boolean,
            default: false
        },
         useprintbutton:{
            type: Boolean,
            default: false
        },
        groupfields:{
            type: Boolean,
            default: false
        },
        tableexpandable:{
            type: Boolean,
            default: false
        },
        rowcolor:{
            type: String,
            default: 'lightgrey'
        },
        headervisible:{
            type: Boolean,
            default: true
        },
        sortable:{
            type: Boolean,
            default: false
        },
        hidedetailrowatindex:{
            type: Number,
            default: -1
        },
        useserialnos:{
            type:  Boolean,
            default: true
        },
        caption:{
            type: String,
            default: ''
        },


    },
    watch: {

        hidedetailrowatindex: function (val) {
            //console.log('watchmoddet')
            this.modifydetailrowstyle(val);
        },
        tableparticulars: function (val) {
            this.$emit('tableparticularschanged', val);
        },

    },
    computed:{compiledData:function(){return {template:`<div>${this.modal_content}</div>`,mounted:function(){console.log('sddfff');this.$emit('formmounted');}}},
        hasDetailRowSlot:function(){return !!this.$scopedSlots['detailrow'];},
    },
    data:function() {
            return {
                summary:{},
                summaryinfo:{},
                dataloaded:false,
                datastatus:'',
                searchfield:'',

                mydetailrowdataready:true,
                tableparticulars:{},
                isActive:false,
                //rowcolor:[],
                align:{},
                width:{},
                p1:'',
                index:0,
                tableFields: [],
                tableFields_verbose:[],
                formFields:[],
                tableData: [],
                originaltableData:[],
                my:12345,
                console:console,
                d:[],
                fields:{},
                apiurldetail:'',
                contentdetailrow:'',
                detailrowcomponent:[],
                showModal:false,
                modal_content:'<div></div>',
                mm:null,
                component:false,
                hasTableData:false,
                detailrowhascontent:[],
                urlcreate:'',
                formkey:1,
                currentindex:-1,
                selectedRow:-1,
                }},

    mounted:function () {

    if (this.loadOnStart) {
      this.loadData()}
        this.$emit('ktablemounted');
    },
    destroyed:function() {
    //console.log(`At this point, watchers, child components, and event listeners have been torn down.`)
    //console.log(this)

  },
    methods: {
        ExportData:function()
                    {
                  
                  //var data=this.tableData;
                  var fields=this.formFields;
                  var newdata=[];
                  for(var x of this.tableData){
                      var newObj=Object.assign({},x);
                      Object.keys(newObj).forEach(function(key){if(!fields.includes(key))delete newObj[key];});
                      newdata.push(newObj);

                  }

                var ws = XLSX.utils.json_to_sheet(newdata);
                var wb = XLSX.utils.book_new();
                 XLSX.utils.book_append_sheet(wb, ws, "data");
                XLSX.writeFile(wb, "sheet1.xlsx");
                },

        rows:function(field){
            console.log(field)
            console.log(this.tableparticulars[field].length)
            if (String(this.tableparticulars[field]).length>50){
                return '3'
            }else if(String(this.tableparticulars[field]).length>20){
                 return '2'
            }else{
                return '1'
            }
        },

        searchtext:function(e){
            //console.log(e.target.value);
            var filter=e.target.value.toLowerCase();

                //console.log(this.searchfield)

            if (this.searchfield.length>=1){
                    this.tableData = this.originaltableData.filter(word => word[this.searchfield].toLowerCase().search(filter)!= -1);
            }

        },
        rowitemclicked:function(item,itemindex,e){
            console.log(e);
            if (this.selectedRow==itemindex){
                this.selectedRow=-1
            }else
            this.selectedRow=itemindex;
            this.$emit('rowselected',item,itemindex)
        },
        formmountevent:function(){
            console.log('form mounted');
            this.$emit('formmounted');
        },
        handleinputchange:function(e){this.$emit("forminputchange",e)},
        modifydetailrowstyle:function(v){this.d[v]='none';},
        calcPos:function(){
                //var abc= this.$refs.myModal.$children[0].$refs.abc;
                //console.log(abc);
                return {"background":"red"};
                },
        loadData: function () {
                axios.get(this.apiurl)
                .then((response) => {
                this.hasTableData = (response.data.success == 'true') ? true : false;

                //this.$emit('tablehasdata', this.hasTableData);

                
                //console.log(this.hasTableData);

                    if(response.data.success=='true'){
                    this.tableFields = response.data.tableFields;
                    this.tableData=response.data.tableData;
                    this.originaltableData=response.data.tableData;


                    this.tableFields_verbose=response.data.tableFields_verbose;
                    this.formFields=response.data.formFields;
                    //console.log(this.formFields);
                    //eslint-disable-next-line
                    this.urlcreate=response.data.hasOwnProperty('urls')?(response.data.urls.hasOwnProperty('urlcreate')?response.data.urls.urlcreate:''):'';
                    this.tableparticulars=response.data.tableparticulars;
                    //console.log(this.tableparticulars);
                    this.DetailRowStyle();
                    //this.defaultrowcolor();
                     var tableFields_align=!('tableFields_align' in response.data)?{}:response.data.tableFields_align;
                    this.width=!('tableFields_width' in response.data)?{}:response.data.tableFields_width;
                    console.log(this.width);
                     this.summary=!('tableFields_summary' in response.data)?{}:response.data.tableFields_summary;
                     this.summaryinfo=!('tableFields_summaryinfo' in response.data)?{}:response.data.tableFields_summaryinfo;
                    //console.log(this.summary);
                        //console.log(Object.keys(tableFields_align).length == 0);
                    var item=this.tableData[0]

                        for (var field of this.formFields) {
                            var type = typeof item[field];
                            if (type == 'string') {
                                if (Object.keys(tableFields_align).length >0) {
                                    this.align[field] = tableFields_align[field]
                                } else {
                                    this.align[field] = 'center';
                                }
                            }
                            
                            if (type == 'number') {
                                if (Object.keys(tableFields_align).length >0) {
                                    this.align[field] = tableFields_align[field]
                                } else {
                                    this.align[field] = 'center';
                                }
                            }
                            
                            if (type == 'boolean') {
                                if (Object.keys(tableFields_align).length >0) {
                                    this.align[field] = tableFields_align[field]
                                } else {
                                    this.align[field] = 'center';
                                }
                            }
                        }


                    //console.log(this.align);
                    this.$emit('dataloaded');
                    this.dataloaded=true;

                    }},function (error) {console.log(error);}
                    )
        },

        renderNormalField:function(field, item){
                            //console.log(itemindex);
                            if(typeof item[field]=='boolean'){

                                return "<input type='checkbox' " +(item[field]?'checked':'') +" style='pointer-events: none;' >";
                            }
                            else{

                                return item[field];
                            }

        },
        ifprevioussame:function(field, item,itemindex){
                        if(itemindex>0){
                                //console.log(this.groupFields);
                                if(this.tableData[itemindex-1][field]==this.tableData[itemindex][field]){
                                    return true;
                                }else{
                                return false;}
                                }
                             else{
                            return false
                             }
        },
        renderTitle:function(field){return "<a href='javascript:void(0);'>"+this.tableFields_verbose[field]+"</a>"+ (this.sortable?"<span><i class='fas fa-sort'></i></span>":"");},
        refreshData:function(){this.loadData()},
        countVisibleFields:function(){return this.formFields.length;},
        onRowClicked:function(item,index){
            //console.log(e);
            //console.log('detial select')
            this.$emit('rowclicked',item,index);
            this.isActive=!this.isActive;
            //console.log(this.currentindex)
            //console.log(index)
            if (this.currentindex===-1){
                this.d.splice(index,1,'');
            } else if(this.currentindex===index)
                {
                //console.log('ccindex1');
                if (this.d[index]==='none'){
                this.d.splice(this.currentindex,1,'')}else{this.d.splice(this.currentindex,1,'none');}
            }else{
               // console.log('ccindex2');
                this.d.splice(this.currentindex,1,'none');
                 this.d.splice(index,1,'');
            }
            this.currentindex=index;


            },
        onRowClicked1:function(item,index){
            //console.log(e);
            this.isActive=!this.isActive;
            //console.log(this.isActive);
            this.$emit('rowclicked',item,index);
            //console.log(this.$scopedSlots);
            if (this.d[index]==''){
                this.d.splice(index,1,'none');
            //this.detailrowcomponent.splice(index,1,'');
                        }
            else{
                for(var i=0;i<this.tableData.length;i++){this.d[i]==''?this.d.splice(i,1,'none'):'';
                    //this.detailrowcomponent.splice(i,1,'');
                }
                //console.log(this.d);
                this.d.splice(index,1,'');


                //this.apiurldetail='http://192.100.200.23:8033/epfo/ajax/epfloanview/';
                //this.detailrowcomponent.splice(index,1,ktable);
                }

            },
        DetailRowStyle:function(){for(var i=0;i<this.tableData.length;i++){this.tableexpandable?this.d.push(''):this.d.push('none');}},
        defaultrowcolor:function(){for(var i=0;i<this.tableData.length;i++){this.rowcolor.push('lightgrey');}},
        modifyrowcolor:function(index,color){this.rowcolor.splice(index,1,color);},
        editItem:function(item,index,e){
            console.log(e);
            this.$emit('edit_clicked');

            this.modal_content='';
            //console.log(this.compiledData);
            this.formkey+=1;
            this.component=false;
                    for (var f in item){this.fields[f]=item[f]}

                //axios.get("{%  url 'epfloanedit' 0 %}".slice(0,-1)+item.id)
                axios.get(item.urledit)
                .then((response) => {
                                //console.log(response);
                                this.modal_content = response.data.html_form;
                                this.mm=this.compiledData;
                                this.component=true;
                                this.showModal=true;

                    },function (error) {alert(error);}
                    );
                    //this.component=true;
                    //this.showModal=true;
        },

        addItem:function(){
            this.$emit('add_clicked');
            this.modal_content='';
            this.formkey+=1;
            this.fields={};
                    //axios.get("{%  url 'epfloancreate' %}")
                axios.get(this.urlcreate)
                .then((response) => {
                    //console.log(response);
                    this.modal_content = response.data.html_form;
                    this.mm=this.compiledData;
                    this.component=true;
                    this.showModal=true;
                    },function (error) {alert(error);}
                    );
                    //this.component=true;
                    //this.showModal=true;
        },
        saveMe_add:function(){
                //save logic
            //console.log('insude save me add');
                var action=this.$refs.mm1.$refs['myform'].action;
                    //const formData=new FormData(this.$refs.mm1.$refs['myform']);
                    //const data={};
                    var formdata=new FormData(document.getElementById('__form'));
                    //formdata.append('addedit','add');
                    //console.log(formdata);
                    //formdata.forEach((key,value)=> console.log(value,key));
                    var csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value;
                    var rdata=this.fields;
                    rdata['addedit']='add';

                    //console.log(action);
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
                                    this.refreshData();
                                    this.$emit('datachanged');
                                    this.component=false;
                                    this.showModal=false;
                                        }
                        })
                                .catch(response=>{console.log(response);});

              },
        saveMe_edit:function(){
                    var action=this.$refs.mm1.$refs['myform'].action;
                    //console.log(action);
                    var formdata=new FormData(document.getElementById('__form'));
                    var csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value;
                     axios({method:'post',url:action, data:formdata,
                        headers: {
                            "X-CSRFToken": csrftoken,
                            'content-type': 'application/x-www-form-urlencoded'
                        }

                        }).then(response=>{
                            //console.log(response);

                            this.modal_content = response.data.html_form;
                            this.mm='';
                            this.mm=this.compiledData;
                            //console.log(response.data.success);
                            if (response.data.success=='True'){
                                    this.refreshData();
                                    this.$emit('datachanged');
                                    this.component=false;
                                    this.showModal=false;
                                        }
                                })
                                .catch(response=>{console.log(response);});
        },
        delItem:function(item,index,e){
            console.log(e);
            if (confirm('Are you sure you want to delete this item ?')) {


                    //console.log(item);
                    //url="{%  url 'epfloandel' 0 %}".slice(0,-1)+item.id
                    var url=item.urldel;
                    axios({method:'get',url:url,

                        }).then(response=>{
                            if (response.data.success=='True'){
                                    this.refreshData();
                                        }
                                })
                                .catch(response=>{console.log(response);});
            }
        },
        onColumnHeaderClicked1:function(field, e){
            console.log(e);
            var url="";
            if (this.sortable) {
                if ((this.apiurl).indexOf("?")==-1){
                     url=this.apiurl + "?field=" + field;}
                else{ url=this.apiurl + "&field=" + field;}

                this.apiurl=url;
                this.loadData();
                //axios.get(url)
                  //  .then((response) => {this.tableFields = response.data.tableFields;
                //this.tableData = response.data.tableData;
               // this.DetailRowStyle();

            //},

               // function (error) {
              //      console.log(error);
              //  }
          //  )

            }
        },
        onColumnHeaderClicked:function(field, e){
            console.log(e);
            if (this.sortable) {
                this.d.splice(this.currentindex,1,'none');
                this.tableData.sort((a,b) => (a['sortkey_'+field] > b['sortkey_'+field]) ? 1 : ((b['sortkey_'+field] > a['sortkey_'+field]) ? -1 : 0));

            }
        },
         spanSize: function(values, valueIndex, fieldIndex) {
              // If left value === current value
              // and top value === 0 (= still in the same top bracket)
              // The left td will take care of the display
              if (valueIndex > 0 &&
                values[valueIndex - 1][fieldIndex] === values[valueIndex][fieldIndex] &&
                (fieldIndex === 0 || (this.spanSize(values, valueIndex, fieldIndex - 1) === 0))) {
                return 0;
              }
              // Otherwise, count entries on the right with the same value
              // But stop if the top value !== 0 (= the top bracket has changed)
              let size = 1;
              let i = valueIndex;
              while (i + 1 < values.length &&
                values[i + 1][fieldIndex] === values[i][fieldIndex] &&
                (fieldIndex === 0 || (i + 1 < values.length && this.spanSize(values, i + 1, fieldIndex - 1) === 0))) {
                i++;
                size++;
              }
              return size;
            },
    },

    }


</script>

<style>
    t:hover{
        background:red;
    }
    .ktable-expand{
         background-color:darkgray;
        width:30px;
    }
    .ktable-expand:hover{
        background-color:#ff0000

    }
    #detailrow {
        ;
    }
    .activeG{
        background-color:#ff0000
    }
    .detailrow .tddetailrow:empty{
        display:none;

    }
    #detailrow{
        padding-left: 40px;
    }
    .table tbody tr td.highlight {
  background-color: #117a8b;
}
[v-cloak]{
    display:none;
}



</style>