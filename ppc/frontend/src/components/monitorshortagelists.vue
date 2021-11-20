<template>
  <div>

        <ktable
            :apiurl="api_root+'/ppc/ajax/shortagelists/'"
            :groupfields="false"
            :use-detail-row="true"
            @rowclicked="rowclicked"
            rowcolor="lightyellow"
            :sortable="false"
            :useserialnos="false"
            caption="Shortage Lists"
            :tablesearchable="false"
        >
         <template v-slot:detailrow="workordernos">
                      <component
                                :key="'ps'+workordernos.index"
                                
                              :is="ktable_ps[workordernos.index]"
                                 :apiurl="api_root+'/ppc/ajax/parentsec?dno='+workordernos.item.dno"
                                    :groupfields="false"
                                 :use-detail-row="true"
                                 rowclicke_d="(item,index) => rowclicked1(item,index,workordernos.index)"
                                 @rowclicked=" rowclicked1"
                                 :useserialnos="false"


                      >
            

                        <template   v-slot:detailrow="ps" >


                            <component
                                    :key="'ol'+workordernos.index+'ps'+ps.index"
                                    
                                    :is="ktable_sld[workordernos.index][ps.index]"
                                    vbind="defineapiorderlist(slotprops.item,slotprops.index)"

                                 :apiurl="api_root+'/ppc/ajax/shortagelist?dno='+ps.item.dno+'&parentsec='+ps.item.parentsec"
                                 :groupfields="false"
                                 :use-detail-row="true"
                                       :tableexpandable="false"
                                 @rowclicked="rowclicked2"
                                dataloaded="orderlistdataready(slotprops.index)"
                                @tableparticularschanged="orderlisttableparticularsmodify"
                                :tablesearchable="true"
                                    :displaytableparticulars="true"
                                    :sortable="true"
                                    :exportto="true"
                            >

                               <template v-slot:detailrow="sld">
                               <table>
                               <tr>
                               <td colspan="2" width="100%">
                               <component
                                        :ref="'ktable'+sld.item.dno+sld.item.drwgnoa"
                                       :key="'op'+'sl'+workordernos.index+'ps'+ps.index+'sld'+sld.index"
                                       :is="ktable_op[workordernos.index][ps.index][sld.index]"
                                       
                                        :apiurl="api_root+'/ppc/ajax/operations?dno='+sld.item.dno+'&drwgno='+sld.item.drwgnoa+'&parentsec='+sld.item.parentsec"
                                        rowcolor="white"
                                        :headervisible="false"
                                        :useserialnos="false"


                                        >
                                        <template v-slot:oplist="oplist" >
                                    
                                        

                                        <span :style="{'background-color':oplist.item.opstatus[index]==1?'green':''}" 
                                        v-for="item,index in ((oplist.item.oplist).split(','))" :key="index"
                                        :title="oplist.item.datestatus[index]"
                                        >
                                        
                                        <input type="checkbox" 
                                        model="checkedOperations" 
                                        :value="item"

                                        :checked="oplist.item.opstatus[index]==1?true:false"

                                        @click.prevent="check($event,oplist.item,oplist.index)"
                                        >
                                        <label>{{item}}</label>
                                        
                                        </span>
                                       
                                        
                                        
                                    
                                        </template>
                                   <template v-slot:remarks="remarks" >
                                       <textarea :style="{'background-color':textareabgcolor[remarks.index]}" :value="remarks.item.remarks" cols="20" @change="updateremarks($event,remarks.item,remarks.index)"></textarea>
                                   </template>

                                   <template v-slot:pdc="pdc" >

                                       <b-form-datepicker
                                                placeholder="Select date"
                                               :value="pdc.item.PDC"
                                               @input="updatepdc($event,pdc.item,pdc.index)"
                                               :date-format-options="{ year: 'numeric', month: 'short', day: 'numeric' }"
                                       >

                                       </b-form-datepicker>
                                   </template>



                                        </component>
                               
                               </td>
                               </tr>
                        
                                   <tr>
                                   <td class="tddetailrow" width="50%">
                                        <component
                                          :key="'running'+'ol'+workordernos.index+'ps'+ps.index+'old'+sld.index"
                                          :is="ktable_run[workordernos.index][ps.index][sld.index]"
                                        :apiurl="api_root+'/ppc/ajax/smallpartsrunning?workorderno='+sld.item.workorderno+'&drwgno='+sld.item.drwgnoa"
                                        rowcolor="lightgreen"
                                        :headervisible="false"
                                        :useserialnos="false"




                                        >

                                        </component>

                                   </td>
                                   <td class="tddetailrow" width="50%">
                                       <component
                                          :key="'stdparts'+'ol'+workordernos.index+'ps'+ps.index+'old'+sld.index"
                                          :is="ktable_fps[workordernos.index][ps.index][sld.index]"
                                        :apiurl="api_root+'/ppc/ajax/homtransac?won='+sld.item.workorderno+'&drwgno='+sld.item.drwgnoa"
                                        rowcolor="lightblue"
                                        :headervisible="false"
                                        :useserialnos="false"


                                        >

                                        </component>

                                   </td>
                                   </tr>
                            
                                </table>
                                    </template>


                            </component>
                            
                        </template>
                        
            </component>

         </template>
        </ktable>
    </div>

</template>




<script>
    import ktable from '../../../../components/ktable-cmp.vue'
    //import ktable from './ktable-cmp.vue'
    import axios from "axios"
    const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
    
        export default {
            name: 'monitororderlists',
            //delimiters: ['[[', ']]'],
            components:{ktable},
            data:function(){return{
                api_root:api_root,
                finyear:'',
                item1:'',completion:'',
               
                keyorderlist:1,
                detailrowdatareadyparentsec:'',
                checkedOperations:[],
                comp:'',item:'ddd',c:[],
                c1:{},
                 ktable_ps:[],
                 ktable_sld:[[]],
                 ktable_op:[],
                 ktable_run:[],
                 ktable_fps:[],
                 textareabgcolor:[],
                 sl_currentindex:'',
                 ps_currentindex:'',
                 sld_currentindex:'',
                
                 }
            },
            methods:{

                orderlisttableparticularsmodify:function(val){
                    this.completion=val.completion;
                },
                orderlistdataready:function(index){
                    console.log(index);

                    //this.$set(this.$refs['c1'+index].align,'completion','right')
                    this.$refs['c1'+index].align.completion='right';
                    //console.log(this.$refs['c1'+index].align);
                },
                rowclicked:function(item,index){
                    //console.log(index);
                    //this.c.splice(0,this.c.length);
                    this.ktable_ps[this.ol_currentindex]='';
                    this.ktable_sld[index]=[];
                    this.ktable_op[index]=[];
                    this.ktable_run[index]=[];
                    this.ktable_fps[index]=[];
                    
                //this.apiparentsec=this.api_root+"/ppc/ajax/parentsec?dno="+item.dno;
                console.log('op= '+this.ktable_op);
                //this.c.splice(index,1,ktable);
                    this.ktable_ps[index]=ktable;
                    this.sl_currentindex=index
                },
                rowclicked1:function(item,psindex){

                    //console.log(this.ol_currentindex);
                    // console.log(psindex);
                    
                     this.ktable_sld[this.sl_currentindex][this.ps_currentindex]='';
                     this.ktable_op[this.sl_currentindex][psindex]=[];
                     this.ktable_run[this.sl_currentindex][psindex]=[];
                     this.ktable_fps[this.sl_currentindex][psindex]=[];
                     this.ktable_sld[this.sl_currentindex][psindex]=ktable;
                     this.ps_currentindex=psindex
                        console.log('op= ');
                        console.log(this.ktable_op)
                       
                   
                    

                },
                rowclicked2:function(item,oldindex){
                    //console.log(item);
                     //console.log(oldindex);

                     this.ktable_op[this.sl_currentindex][this.ps_currentindex][this.sld_currentindex]='';
                     this.ktable_run[this.sl_currentindex][this.ps_currentindex][this.sld_currentindex]='';
                    this.ktable_fps[this.sl_currentindex][this.ps_currentindex][this.sld_currentindex]='';
                    
                     this.ktable_op[this.sl_currentindex][this.ps_currentindex][oldindex]=ktable;
                     this.ktable_run[this.sl_currentindex][this.ps_currentindex][oldindex]=ktable;
                     this.ktable_fps[this.sl_currentindex][this.ps_currentindex][oldindex]=ktable;
                     this.sld_currentindex=oldindex
                     console.log('op3= ');
                        console.log(this.ktable_op)
                    this.textareabgcolor[this.index]='white';
                },
                stdtablehasdata:function(i,e){console.log(i);console.log(e);e?'':this.partdetailid=parseInt(i)},
                defineapiorderlist:function(item,index){
                    console.log('define');
                    this.apiorderlist[String(item.parentsec)+String(item.dno)+'at'+index]='';
                    this.c1[String(item.parentsec)+String(item.dno)+'at'+index]='';
                    //console.log('d'+item.parentsec+item.dno+'at'+index);

                },
                setupOperations:function(){
                        //console.log(o);


                },
                check:function(e,item,){
                        console.log(e.target);
                        //console.log('indexcheck'+index);
                    //this.checkitem=item;
                    //this.checkindex=index;
                        var dno=item.dno;
                        var drwgno=item.drwgno;
                        var itemno=0;
                        var status=e.target.checked;
                        var opno=e.target.value;
                        //var next=this.$router.currentRoute
                        var formdata=new FormData();
                        formdata.append('dno',dno);
                        formdata.append('drwgno',drwgno);
                        formdata.append('itemno',itemno);
                        formdata.append('status',status);
                        formdata.append('opno',opno);
                        
                        
                        //var csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value;
                        
                        axios({method:'post',url:this.api_root+"/ppc/operationcreate/", data:formdata,
                        headers: {
                            
                            'content-type': 'application/x-www-form-urlencoded'
                        }

                        }).then((response)=>{
                            //console.log(item.drwgno);
                            //console.log(response);
                            //console.log(this.$refs['ktable'+item.dno+item.drwgno]);
                                    if(response.data.success)
                                        {
                                            this.$refs['ktable' + item.dno + item.drwgno].refreshData();
                                        }else
                                            {
                                                window.location.href=(this.api_root+"/accounts/login/?next="+this.api_root+'/ppc')
                                                //this.router.push('/');
                                            }

                            //console.log(this.$refs['ktable'+item.dno+item.drwgno]);

                        
                                        
                        })
                                .catch(response=>{console.log(response);});
                     },
                updateremarks:function(e,item,index){
                        //console.log(e.target);
                        //console.log('indexcheck'+index);
                    //this.checkitem=item;
                    //this.checkindex=index;
                        var dno=item.dno;
                        var drwgno=item.drwgno;
                        var itemno=0;

                        var remarks=e.target.value;

                        var formdata=new FormData();
                        formdata.append('dno',dno);
                        formdata.append('drwgno',drwgno);
                        formdata.append('itemno',itemno);
                        formdata.append('remarks',remarks);
                        //formdata.append('opno',opno);
                        //var csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value;

                        axios({method:'post',url:this.api_root+"/ppc/olitemremarksupdate/", data:formdata,
                        headers: {

                            'content-type': 'application/x-www-form-urlencoded'
                        }

                        }).then((response)=>{
                            //console.log(item.drwgno);
                            //console.log(response);
                            //console.log(this.$refs['ktable'+item.dno+item.drwgno]);
                                    if(response.data.success)
                                        {
                                            this.$refs['ktable' + item.dno + item.drwgno].refreshData();
                                            this.currentindex=index;
                                            this.textareabgcolor[index]='lightblue';
                                        }else
                                            {
                                                window.location.href=(this.api_root+"/accounts/login/?next="+this.api_root+'/ppc')
                                            }

                            //console.log(this.$refs['ktable'+item.dno+item.drwgno]);



                        })
                                .catch(response=>{console.log(response);});
                     },
                updatepdc:function(e,item){
                        console.log(e);
                        //console.log('indexcheck'+index);
                    //this.checkitem=item;
                    //this.checkindex=index;
                        var dno=item.dno;
                        var drwgno=item.drwgno;
                        var itemno=0;

                        var pdc=e;

                        var formdata=new FormData();
                        formdata.append('dno',dno);
                        formdata.append('drwgno',drwgno);
                        formdata.append('itemno',itemno);
                        formdata.append('pdc',pdc);
                        //formdata.append('opno',opno);
                        //var csrftoken=document.querySelector('[name="csrfmiddlewaretoken"]').value;

                        axios({method:'post',url:this.api_root+"/ppc/olitempdcupdate/", data:formdata,
                        headers: {

                            'content-type': 'application/x-www-form-urlencoded'
                        }

                        }).then((response)=>{
                            //console.log(item.drwgno);
                            //console.log(response);
                            //console.log(this.$refs['ktable'+item.dno+item.drwgno]);
                                    if(response.data.success)
                                        {
                                            this.$refs['ktable' + item.dno + item.drwgno].refreshData();
                                        }else
                                            {
                                                window.location.href=(this.api_root+"/accounts/login/?next="+this.api_root+'/ppc')
                                            }

                            //console.log(this.$refs['ktable'+item.dno+item.drwgno]);



                        })
                                .catch(response=>{console.log(response);});
                     },
                        

                
            },
        }

</script>
