<template>
    <div>
        <div class="modal-heade">
    <button type="button" @click="$emit('close')" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
    </div>
    <div class="modal-body">
        <div  class="row bg-secondar">
            <span  class="col-md-12 " style="float:center;background-colo:lightblue;text-align:center">GROUP ON:{{selectedfields}}</span>
        </div>

        <table class="   table   table-striped table-sm " style="margin-bottom:5px;margin-top:5px">
            <tr>
                <th style="text-align:left" >field</th><th>function</th><th>filter</th>
            </tr>
            <template v-for="field,index in fields">
                <tr :key="index">
                    <td style="text-align:left"><input type="checkbox" @change="fieldselected($event,field,index)" :checked="selectedfields.indexOf(field)>-1?true:false" >{{field}}</td>
                    <td><b-form-select v-if="selectedfields.indexOf(field)>-1" v-model="selectedfunction[field]" :options="['group','count','sum']" >
                            
                        </b-form-select>
                    </td>
                    <td><b-form-select  v-model="selectedfilter[field]" options1="['a','b','c']"  :options="distinctvalues(field)" multiple>
                             <!-- This slot appears above the options from 'options' prop 
                            <template #first>
                                <b-form-select-option :value="undefined" >all</b-form-select-option>
                            </template>
                            -->
                        </b-form-select>
                    </td>
                    <td>{{selectedfunction}}</td>
                </tr>
            </template>
            
            
        </table>
        </div>
        <div class="row">

            <b-button class="col-md-2 offset-5" block @click="submit">Submit</b-button>
        </div>

    </div>
</template>

<script>
export default {
    name:'groupon',
    components:{},
    mounted:function(){
        //console.log('asderrrrrr')
        //for (var f of this.fields){
         //   this.$set(this.selectedfunction, f, 'group')
            
        //}
        //console.log(this.selectedfunction)

    },
    data:function(){
        return{selectedfields:[],selectedfunction:{},selectedfilter:{},}
    },
    props:{
        fields:{
            type: [],
            default: function(){
               // return ['a','b']

                return this.$parent.$parent.formFields
                }
        },
    },
    watch:{
        
    },
    computed:{
        ktable:function(){
            console.log(this.$parent.$parent)
            return this.$parent.$parent
        },
    },
    methods:{
        fieldselected:function(e,field){
            
           
            if (this.selectedfields.indexOf(field)==-1){
                this.selectedfields.push(field);
                //var i=this.selectedfields.indexOf(field);
                //if (i>-1){
                  //  var tmp=this.fields[i]
                   // this.$set(this.fields,i,field)
                   // this.$set(this.fields,index,tmp)
                  //  }
            }else{
                const i=this.selectedfields.indexOf(field);
                if(i>-1){
                    this.selectedfields.splice(i,1);
                        //console.log(this.selectedrows);
                    }
                }
        },
        distinctvalues:function(field){
            var uniquevalues=new Set();
            var tableData=this.ktable.tableData;
            for (var row of tableData){
                uniquevalues.add(row[field])
            }
            return Array.from(uniquevalues).sort();

        },
        submit:function(){
            console.log('submit')
            this.$emit('groupdatasubmit')
        },
        
    },
}
</script>