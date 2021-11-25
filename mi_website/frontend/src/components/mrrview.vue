 <template>
 <div id="app1">
        <div class="row" >
            <span class="col-md-9  text-center bg-secondary" >
                <h4>View Add Edit MRRs</h4>
            </span>
            

        </div>

        <div class="row bg-inf" >
            <div class="input-group">
                <div class="col-md-3 offset-2">
                    <label for="txtfinyear">Fin Year:</label>
                    <input type="text" class="form-control" :value="finyear " id="txtfinyear" disabled>
                </div>
                <div class="col-md-3">
                    <label for="mrrdate">Select Mrr date:</label>
                    <vue-date-pick
                        id="mrrdate"
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
            <div class="col-md-12">
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
                    @forminputchange="handlemrrforminputchange"
                    :useprintbutton="true"
                    >
                    <template v-slot:addtext>new</template>
                 <template v-slot:detailrow="slotprops">


                <!-- Tab panes -->

                       <component :is="c[slotprops.index]"
                                  :key="key_c"
                                  :ref="'c_'+slotprops.index"
                                                 :apiurl="urlmrrvalues"
                                                 :groupfields="false"
                                                 :use-detail-row="false"
                                                    :use-action-button="!slotprops.item.inspauth"
                                                :sortable="false"

                                  rowcolor="lightgreen"

                                      >
                           <template  v-slot:printaction>
                        <p v-show="false">kk</p>
                    </template>
                       </component>



                         </template>
                    </ktable>
        </div>
    </div>
    </div>

</template>



<script>
import ktable from '../../../../components/ktable-cmp.vue'
import VueDatePick from '../../../../components/vuedatepick-cmp.vue'
import axios from 'axios'
import $ from 'jquery'
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
  
export default {
            name: 'mrrview',
            components: {
                ktable,VueDatePick
            },
            mounted:function(){
                this.getstartinfo();
            },
            data:function(){
                return{api_root:api_root,finyear:'',key:[],dated:"",apiurl:'',key_index_ktable:1,key_index_c:1,key_index_c1:1,key_index_c2:1,c:[],c1:[],c2:[],urlmislipitems:'',urlmrrs:'',urlmislipbills:'',urlmrrvalues:'',currentindex:'',}
            },
            watch:{
                dated:function(){this.dateclicked();},
            },
            computed:{
                key_ktable:{
                    get:function(){return 'ktable'+this.key_index_ktable},
                    //set:function(newvalue){this.key_index_ktable=newvalue},
                },
                key_c:{
                    get:function(){return 'c'+this.key_index_c1},
                    //set:function(newvalue){this.key_index_c1=newvalue},
                },
                key_c1:{
                    get:function(){return 'c1'+this.key_index_c},
                   // set:function(newvalue){this.key_index_c=newvalue},
                },
                key_c2:{
                    get:function(){return 'c2'+this.key_index_c2},
                    //set:function(newvalue){this.key_index_c2=newvalue},
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
                },
                datachanged:function(i){
                    //console.log('aqwerty');
                    this.$refs['c2_'+i].refreshData()
                },
                handlemrrforminputchange:function(e){
                    //console.log(e.target.name);
                    if(e.target.name=='pono') {
                        var url=this.api_root+"/mi/ajax/getsuppaddfrompono?pono="+e.target.value;
                        axios.get(url)
                            .then((response) => {
                                //console.log(response);
                                this.$refs.ktable.$refs.mm1.$refs.ref_suppname.value = response.data.suppadd;



                                },function (error) {console.log(error);}
                        );
                        //this.$refs.ktable.$refs.mm1.$refs.ref_suppname.value = e.target.value;
                    }

                },
                handleforminputchangeinmislipitems:function(e,index){
                    //console.log(e.target.name);
                    if(e.target.name=='stockno') {
                        var url=this.api_root+"/mi/ajax/getstocknodes?stockno="+e.target.value;
                        axios.get(url)
                            .then((response) => {
                                //console.log(response);

                                this.$refs['c_'+index].$refs.mm1.$refs.ref_des.value = response.data.stockdes;



                                },function (error) {console.log(error);}
                        );
                    }

                },
                handleforminputchangeinmislipibills:function(e){
                    console.log(e.target.name);
                },
                dateclicked:function(){
                    //console.log('date clicked');
                    //this.key_index_ktable=1;
                    this.key_index_c=1;
                    this.key_index_c1=1;
                    this.key_index_c2=1;
                    this.apiurl=this.api_root+"/mi/mrrs?finyear="+this.finyear+"&dated="+this.dated;
                    this.key_index_ktable+=1;
                },
                rowclicked:function(item,index){
                    //console.log(item);
                    this.urlmrrvalues='';
                    this.c[this.currentindex]='';
                    this.key_c+=1;
                    this.currentindex=index;
                     this.urlmrrvalues=this.api_root+"/mi/mrrvalues?finyear="+item.finyear+"&mrrno="+item.mrrno;
                    //console.log(this.urlmislipitems);
                    this.c[index]=ktable;
                    this.key_c+=1;






                    //this.keyktable+=1;
                    this.key_index_c+=1;
                    this.key_index_c1+=1;
                    this.key_index_c2+=1;
                },

            },

}

$(function(){
  $("#__form").on("change", "#id_pono", function () {

      var pono = $(this).val();

  alert(pono);
  $.ajax({
      url: api_root+"/mi/ajax/getsuppaddfrompono/",
      data: {'pono':pono},

      type: 'GET',
      dataType: 'json',
      success: function (data) {
          //alert(data.suppadd);
          $(".mislipeditform textarea[name='suppname']").val(data.suppadd);
      },
      error:function () {
          //alert(data.suppadd);
          $(".mislipeditform textarea[name='suppname']").val('');
      }
  })})});
</script>