<template>
<div >
        <ktable
            :apiurl="api_root+'/hr/ajax/wgps/'"
            :hideduplicatefields="false"
            :use-detail-row="false"
            rowclicked="rowclicked"
            rowcolor="pink"
            :sortable="true"
            :summaryrow="false"
            :tablesearchable="true"
            :groupinginforequired="true"
            

        >
         
        </ktable>
    </div>

</template>


<script>
    import ktable from '../../../../components/ktable-cmp.vue'
    
    console.log(process.env.VUE_APP_API_ROOT);
    const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
        
    export default {
            name: 'wgps',
           // delimiters: ['[[', ']]'],
            components: {
                ktable
             },
            data:function(){
                return {api_root:api_root,}
                },
            methods:{

            },
                
        }

    </script>