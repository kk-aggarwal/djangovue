<template>
<div >
        <ktable
            :apiurl="api_root+'/design/ajax/products/'"
            :hideduplicatefields="false"
            :use-detail-row="true"
            @rowclicked="rowclicked"
            rowcolor="pink"
            :sortable="true"
            
            :summaryrow="false"
            

        >
         <template v-slot:detailrow="slotprops">
                      <component :is="c[slotprops.index]"
                                 :apiurl="apipartlists"
                                 :groupfields="false"
                                 :use-detail-row="true"
                                 @rowclicked="rowclicked1"

                      >
                        <template v-slot:detailrow="slotprops">
                            <div style="border: solid black 2px;">
                            <component
                                    :ref="'c1'+slotprops.index"
                                    :is="c1[slotprops.index]"
                                 :apiurl="apipartlistdetail"
                                 :groupfields="false"
                                 :use-detail-row="true"
                                       :tableexpandable="true"
                                 rowclicked="rowclicked2"
                                 :tablesearchable="false"
                                    


                            >
                               <template v-slot:detailrow="slotprops">
                                   <div class="tddetailrow">
                                        <ktable
                                        :key="slotprops.item.partdetailid"
                                        :apiurl="api_root+'/design/ajax/stditems?partdetailid=' + slotprops.item.partdetailid"
                                        rowcolor="yellow"
                                        :headervisible="false"
                                        tablehasdata="stdtablehasdata(slotprops.index,$event)"

                                        >

                                        </ktable>
                                   </div>
                                   <div class="tddetailrow">
                                       <ktable
                                       :key="slotprops.item.itemid"
                                        :apiurl="api_root+'/design/ajax/weldments?itemid=' + slotprops.item.itemid"
                                        rowcolor="lightblue"
                                        :headervisible="false"
                                        tablehasdata="stdtablehasdata(slotprops.index,$event)"

                                        >

                                        </ktable>
                                   </div>
                                    </template>


                            </component>
                            </div>
                        </template>
                      </component>
         </template>
        </ktable>
    </div>

</template>


<script>
    import ktable from '../../../../components/ktable-cmp.vue'
    
    console.log(process.env.VUE_APP_API_ROOT);
    const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
        
    export default {
            name: 'products',
            delimiters: ['[[', ']]'],
            components: {
                ktable
             },
            data:function(){
                return {api_root:api_root,item:'ddd',c:[],c1:[],apipartlists:'',apipartlistdetail:'',partdetailid:-1}},
            methods:{
                rowclicked:function(item,index){
                    console.log(index);
                this.apipartlists=this.api_root+"/design/ajax/partlists?machineid=" + item.machineid;
                console.log(this.apipartlists);
                this.c[index]=ktable;
                },
                rowclicked1:function(item,index){
                    console.log(index);
                this.apipartlistdetail=this.api_root+"/design/ajax/partlistdetail?partlistno=" + item.partlistno;
                console.log(this.apipartlistdetail);
                this.c1[index]=ktable;
                },
                stdtablehasdata:function(i,e){console.log(i);console.log(e);e?'':this.partdetailid=parseInt(i)},
            },
        }

    </script>