<template>
    <div id="app3">
        <div class="row" >
            <span class="col-md-12  text-center bg-secondar" >
                <h5>Stock Master</h5>
            </span>

        </div>

        <div class="row bg-inf" >
            <div class="input-group">
                <div class="col-md-3 offset-2">

                    <input type="text" class="form-control" v-model="stockno" id="txtstockno" placeholder="Stock No" >
                </div>
                <div class="col-md-3 offset-2">

                    <input type="text" class="form-control" :value="finyear" id="txtfinyear" disabled>
                </div>
            </div>
        </div>
        <div class="row bg-inf" >
            <div class="col-md-10   offset-1 bg-secondar tscroll" st="height:400px;overflow-y:auto;" >
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
                    forminputchange="handlemrrforminputchange"
                    :useprintbutton="false"
                    :tablesearchable="true"
                    >

                </ktable>
            </div>
        </div>



    </div>
</template>

<script>
import ktable from '../../../../components/ktable-cmp.vue'
//import ktable from './ktable-cmp.vue'
import axios from 'axios'
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT

export default {
    
    name:'ststockmasterview',
    components:{ktable},
    mounted:function(){
                    this.getstartinfo();
    },
    data:function(){return{api_root:api_root,finyear:'',key_ktable:1,apiurl:'',stockno:'',}},
    watch:{
        stockno:function(){this.loaddata();},
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
        loaddata:function(){
                    //console.log(item);

            if(this.stockno.length>=2){
                     this.apiurl=this.api_root+"/mi/ajax/ststockmaster?finyear="+this.finyear + "&stockno="+this.stockno;
                    //console.log(this.urlmislipitems);

                    this.key_ktable+=1;
            }
        },
    },

}
</script>

  <style>
    body{font-size:80%}
    .tscroll {
        width:400px;
        height:500px;
        overflow-y: auto;
  overflow-x: auto;
  
  margin-bottom: 10px;
  border: solid black 2px;
}

.tscroll table td:irst-child  {
  position: sticky;
    left:-10px;

    color: #359900;
  background-color: #ddd;
}

.tscroll table th{
    width:auto;
  position: sticky;
  top: 0;
  background-color: #ddd;
}

</style>