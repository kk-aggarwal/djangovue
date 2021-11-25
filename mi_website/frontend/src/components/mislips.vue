<template>
    <div class="row">
        <div class="col-md-12 ">
            <nav>
                <div class="nav nav-tabs nav-fill" id="nav-tab" role="tablist">
                    <a class="nav-item nav-link active" id="nav-home-tab" data-toggle="tab" href="#nav-home" role="tab" aria-controls="nav-home" aria-selected="true">MI slips</a>
                    <a class="nav-item nav-link" id="nav-profile-tab" data-toggle="tab" href="#nav-profile" role="tab" aria-controls="nav-profile" aria-selected="false">MRR</a>
                </div>
            </nav>
                <div class="tab-content py-3 px-3 px-sm-0" id="nav-tabContent">
                    <div class="tab-pane fade show active" id="nav-home" role="tabpanel" aria-labelledby="nav-home-tab">
                        <mislipview></mislipview>
                    </div>
                    <div class="tab-pane fade" id="nav-profile" role="tabpanel" aria-labelledby="nav-profile-tab">
                       <mrrview></mrrview>
                    </div>
                    
                </div>
        </div>
    </div>
        

</template>

<script>
import mislipview from './mislipview-cmp.vue'
import mrrview from './mrrview.vue'

export default {
    name:"mainstore",
    components:{ mislipview,mrrview},
    
}
</script>

<style>

</style>