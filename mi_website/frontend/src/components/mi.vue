<template>
<div >
    <div class="row">
        <div class="col-md-10 offset-3">
            <h3>Welcome to Incoming Materials</h3>
        </div>
    </div>
    <div class="row mt-5">
        <div class="col-md-3 offset-4 bg-inf">
            <button type="button" class=" btn btn-primary btn-block" @click="mislipclick">MI SLIPS</button>
        </div>
    </div>
    
    <div class="row mt-5">
        <div class="col-md-3 offset-4">
            <button type="button" class="btn btn-primary btn-block" @click="mainstoreclick">MAIN STORE</button>
        </div>
    </div>
</div>
</template>

<script>
export default {
    name:"mi",
    methods:{
        mislipclick:function(){
            this.$router.push('/mislips')
        },
        mainstoreclick:function(){
            this.$router.push('/mainstore')
        },
    },
}
</script>