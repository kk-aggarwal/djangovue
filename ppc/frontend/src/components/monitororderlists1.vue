  <template>
  <div>

        <ktable
            :apiurl="api_root+'/ppc/ajax/workordernos/'"
            :groupfields="false"
            :use-detail-row="true"
            @rowclicked="rowclicked"
            rowcolor="pink"
            :sortable="false"
            :useserialnos="false"
            caption="Order Lists"
            :tablesearchable="false"
        >
         <template v-slot:detailrow="slotprops">
                      <component
                                :ref="'c'+slotprops.index"
                              :is="c[slotprops.index]"
                                 :apiurl="apiparentsec"
                                    :groupfields="false"
                                 :use-detail-row="true"
                                 @rowclicked="rowclicked1"
                                 :useserialnos="false"


                      >


                        <template   v-slot:detailrow="slotprops" >


                            <component
                                    :key="keyorderlist"
                                    :ref="'c1'+slotprops.index"
                                    :is="c1[String(slotprops.item.parentsec)+String(slotprops.item.dno)+'at'+slotprops.index]"
                                    vbind="defineapiorderlist(slotprops.item,slotprops.index)"

                                 :apiurl="apiorderlist[String(slotprops.item.parentsec)+String(slotprops.item.dno)+'at'+slotprops.index]"
                                 :groupfields="false"
                                 :use-detail-row="true"
                                       :tableexpandable="false"
                                 @rowclicked="rowclicked2"
                                @dataloaded="orderlistdataready(slotprops.index)"
                                @tableparticularschanged="orderlisttableparticularsmodify"
                                :tablesearchable="true"
                                    :displaytableparticulars="true"
                                    :sortable="true"
                                    :exportto="true"
                            >

                               <template v-slot:detailrow="slotprops">
                               <table>
                               <tr>
                               <td colspan="2" width="100%">
                               <ktable
                                       :key="'ktable'+slotprops.item.dno+slotprops.item.drwgnoa"
                                       :ref="'ktable'+slotprops.item.dno+slotprops.item.drwgnoa"
                                        :apiurl="api_root+'/ppc/ajax/operations?dno='+slotprops.item.dno+'&drwgno='+slotprops.item.drwgnoa+'&parentsec='+slotprops.item.parentsec"
                                        rowcolor="white"
                                        :headervisible="false"
                                        :useserialnos="false"


                                        >
                                        <template v-slot:oplist="slotprops" >
                                    
                                        

                                        <span :style="{'background-color':slotprops.item.opstatus[index]==1?'green':''}" 
                                        v-for="item,index in ((slotprops.item.oplist).split(','))" :key="index"
                                        :title="slotprops.item.datestatus[index]"
                                        >
                                        
                                        <input type="checkbox" 
                                        model="checkedOperations" 
                                        :value="item"

                                        :checked="slotprops.item.opstatus[index]==1?true:false"

                                        @click.prevent="check($event,slotprops.item,slotprops.index)"
                                        >
                                        <label>{{item}}</label>
                                        
                                        </span>
                                       
                                        
                                        
                                    
                                        </template>
                                   <template v-slot:remarks="slotprops" >
                                       <textarea :style="{'background-color':textareabgcolor[slotprops.index]}" :value="slotprops.item.remarks" cols="20" @change="updateremarks($event,slotprops.item,slotprops.index)"></textarea>
                                   </template>

                                   <template v-slot:pdc="slotprops" >

                                       <b-form-datepicker
                                                placeholder="Select date"
                                               :value="slotprops.item.PDC"
                                               @input="updatepdc($event,slotprops.item,slotprops.index)"
                                               :date-format-options="{ year: 'numeric', month: 'short', day: 'numeric' }"
                                       >

                                       </b-form-datepicker>
                                   </template>



                                        </ktable>
                               
                               </td>
                               </tr>
                                   <tr>
                                   <td class="tddetailrow" width="50%">
                                        <ktable
                                          :key="'running'+slotprops.item.dno+slotprops.item.drwgnoa"
                                        :apiurl="api_root+'/ppc/ajax/smallparts_running?workorderno='+slotprops.item.workorderno+'&drwgno='+slotprops.item.drwgnoa"
                                        rowcolor="lightgreen"
                                        :headervisible="false"
                                        :useserialnos="false"




                                        >

                                        </ktable>

                                   </td>
                                   <td class="tddetailrow" width="50%">
                                       <ktable
                                          :key="'stdparts'+slotprops.item.dno+slotprops.item.drwgnoa"
                                        :apiurl="api_root+'/ppc/ajax/hom_transac?won='+slotprops.item.workorderno+'&drwgno='+slotprops.item.drwgnoa"
                                        rowcolor="lightblue"
                                        :headervisible="false"
                                        :useserialnos="false"


                                        >

                                        </ktable>

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
                currentIndexOrderList:'',
                keyorderlist:1,
                detailrowdatareadyparentsec:'',
                checkedOperations:[],
                comp:'',item:'ddd',c:[],
                c1:{},
                 apiparentsec:'',
                 apiorderlist:{},
                 apipartlistdetail:'',
                 partdetailid:-1,
                 textareabgcolor:[],
                 currentindex:'',}
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
                    this.c[index]='';
                this.apiparentsec=this.api_root+"/ppc/ajax/parentsec?dno="+item.dno;
                console.log(this.apiparentsec);
                //this.c.splice(index,1,ktable);
                    this.c[index]=ktable;
                },
                rowclicked1:function(item,index){

                    console.log('rowclickedparentsec')
                       // this.$refs['c'+index].d[index]='none'
                    //console.log('kk'+item);
                     //this.c1.splice(index,1,'');

                   // this.c1.splice('',this.c1.length);
                    //this.c1.splice(index,1,'');
                    //this.c1[index]='';
                    this.apiorderlist[this.currentIndexOrderList]='';
                    this.c1[this.currentIndexOrderList]='';
                    this.keyorderlist+=1;
                    this.currentIndexOrderList=String(item.parentsec)+String(item.dno)+'at'+index;
                var url=this.api_root+"/ppc/ajax/orderlist?dno="+item.dno+"&parentsec="+item.parentsec;
                this.apiorderlist[String(item.parentsec)+String(item.dno)+'at'+index]=url;
                //console.log(this.apiorderlist);
                //console.log(this.c1);

                //this.c1.splice(index,1,ktable);
                    //this.c1[index]=ktable;
                    //this.c1[String(item.parentsec)+String(item.dno)+'at'+index]='';
                    this.c1[String(item.parentsec)+String(item.dno)+'at'+index]=ktable;
                    //this.keyorderlist+=1
                     //console.log(this.c1);

                },
                rowclicked2:function(item,index){
                    console.log(item);
                     console.log(index);
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
                                                window.location.href=(this.api_root+"/accounts/login/?next="+api_root+'/ppc')
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

                        axios({method:'post',url:this.api_root+"/ppc/olitemremarksupdate", data:formdata,
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
                                                window.location.href=(this.api_root+"/accounts/login/?next={{ request.path }}")
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
                                                window.location.href=(this.api_root+"/accounts/login/?next={{ request.path }}")
                                            }

                            //console.log(this.$refs['ktable'+item.dno+item.drwgno]);



                        })
                                .catch(response=>{console.log(response);});
                     },
                        

                
            },
        }

</script>

