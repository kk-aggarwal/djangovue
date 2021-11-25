<template>
    <component :is="myhello"></component>
</template>

<script>
import axios from 'axios'
export default {
    name:'hello',
    data:function(){return {myhello:null,}
    },
    mounted:function(){
        
    },
    
    
}
</script>