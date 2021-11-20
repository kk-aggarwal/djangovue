<template>
  <div>
    <div class="row">
        <div class="col-sm-12">
        <h3 align="center">MIS: MACHINE UTILIZATION</h3><hr>
        </div>
    </div>
    <div class="row">
        <div class="col-md-8 offset-2 bg-dange">
          <barchart
            :chart-data="chartData1"
            :options="chartOptions1"
            :width="500" :height="300"
            
           >
           </barchart>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-md-6 offset-2 bg-dange">
          <horizontalbarchart
            :chart-data="chartData2"
            :options="chartOptions2"
            :width="500" :height="1000"
            
           >
           </horizontalbarchart>
           
        </div>
        <div class="col-sm-4" id="machines"></div>
       
    </div>
    <hr>
    <div class="row">
        <div class="col-md-8 offset-2 bg-dange">
          <barchart
            :chart-data="chartData3"
            :options="chartOptions3"
            :width="500" :height="300"
            
           >
           </barchart>
        </div>
        
       
    </div>
    

  </div>
</template>
<script>
import barchart from '../../../../components/barchart.vue'
import horizontalbarchart from '../../../../components/horizontalbarchart.vue'
import axios from "axios"
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
 

export default {
  name: 'manpowerutilization',
  components: {
   barchart,horizontalbarchart
    
  },
  mounted:function(){
      this.getdata();
      
  },
  data:function(){
    return{api_root:api_root,
    chartData1:{},chartOptions1:{},
    chartData2:{},chartOptions2:{},
    chartData3:{},chartOptions3:{},
    }
  },
  methods:{
      getdata:function(){
          
          var url='http://192.100.200.23:8000'+'/mtpinfoshare/ajax/mtp09'
          //{headers: {
       //'Access-Control-Allow-Origin': '*',
       //'Content-type': 'application/json',
    //}}
          axios.get(url)
                .then((response) => {
                    var labels=response.data.labels
                    var cap_util=response.data.cap_util
                    var no_opr=response.data.no_opr
                    var m_rep=response.data.m_rep
                    var e_rep=response.data.e_rep
                    var no_pwr=response.data.no_pwr
                    var no_tool=response.data.no_tool
                    var no_job=response.data.no_job
                    var misc=response.data.misc
                    var layoff=response.data.layoff

                    
                    this.chartData1= {
        labels: labels,
        datasets: [
            {
            label: '#  Cap. Util',
            data: cap_util,

            backgroundColor:
                'rgb(0,128,64)',},

            {
            label: '#  no opr',
            data: no_opr,

            backgroundColor:
                'rgb(55,167,187)',},
            {
            label: '# mech repair',
            data: m_rep,

            backgroundColor:
                'rgb(255,128,128)',},
            {
            label: '# elec repair',
            data: e_rep,
            backgroundColor:
                'rgb(0,128,0)',},
            {
            label: '# no power',
            data: no_pwr,
            backgroundColor:
                'rgb(128,0,0)',},
            {
            label: '# no tools',
            data: no_tool,
            backgroundColor:
                'rgb(223,223,0)',},
            {
            label: '#no job',
            data: no_job,
            backgroundColor:
                'rgb(255,255,45)',},
            {
            label: '# misc',
            data: misc,
            backgroundColor:
                'rgb(0,210,210)',},
            {
            label: '# layoff',
            data: layoff,
            backgroundColor:
                'rgb(98,132,251)',},

               ]
            };
        this.chartOptions1={
            scales: {
						xAxes: [{
							stacked: true,
						}],
						yAxes: [{
							stacked: true
						}]
					}
        };
                               
                   },function (error) {alert(error);}
                    );

         url=api_root+'/mtpinfoshare/ajax/mtp10'
          
          axios.get(url)
                .then((response) => {
                   var labels=response.data.labels
            var cap_util=response.data.cap_util
            var no_opr=response.data.no_opr
            var m_rep=response.data.m_rep
            var e_rep=response.data.e_rep
            var no_pwr=response.data.no_pwr
            var no_tool=response.data.no_tool
            var no_job=response.data.no_job
            var misc=response.data.misc
            var layoff=response.data.layoff
            var machines= document.getElementById("machines")
                    machines.innerHTML=response.data.machines
        this.chartData2= {
        labels: labels,
        datasets: [
            {
            label: '#  Cap. Util',
            data: cap_util,

            backgroundColor:
                'rgb(0,128,64)',},

            {
            label: '#  no opr',
            data: no_opr,

            backgroundColor:
                'rgb(55,167,187)',},
            {
            label: '# mech repair',
            data: m_rep,

            backgroundColor:
                'rgb(255,128,128)',},
            {
            label: '# elec repair',
            data: e_rep,
            backgroundColor:
                'rgb(0,255,255)',},
            {
            label: '# no power',
            data: no_pwr,
            backgroundColor:
                'rgb(128,0,0)',},
            {
            label: '# no tools',
            data: no_tool,
            backgroundColor:
                'rgb(223,223,0)',},
            {
            label: '#no job',
            data: no_job,
            backgroundColor:
                'rgb(202,0,0)',},
            {
            label: '# misc',
            data: misc,
            backgroundColor:
                'rgb(0,210,210)',},
            {
            label: '# layoff',
            data: layoff,
            backgroundColor:
                'rgb(98,132,251)',},

               ]
            };
        this.chartOptions2={
            scales: {
						xAxes: [{
							stacked: true,
						}],
						yAxes: [{
							stacked: true
						}]
					}
        }
        


    
    
    ;
                               
                   },function (error) {alert(error);}
                    );
      },
  },
}
</script>