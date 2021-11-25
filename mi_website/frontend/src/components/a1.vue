<template >
    <span>
        {{aa}}

    </span>

</template>

<script>
     export default {
        name: 'a1', 
         delimiters: ['[[', ']]'],
         
         data: function () {
             return {
                 aa: 'component a1',

             };
         },
     }

</script>

