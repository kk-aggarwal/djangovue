<template>
  <div>
    <div class="row">
        <div class="col-sm-12">
        <h3 align="center">MIS: MANPOWER UTILIZATION</h3><hr>
        </div>
    </div>
    <div class="row">
        <div class="col-md-8 offset-2 bg-dange">
          <barchart
            :chart-data="chartData1"
            :options="chartOptions1"
            
           >
           </barchart>
        </div>
    </div>
    <hr>
    <div class="row">
        <div class="col-md-8 offset-2 bg-dange">
          <barchart
            :chart-data="chartData2"
            :options="chartOptions2"
            :width="500" :height="300"
            
           >
           </barchart>
        </div>
        
       
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
import axios from "axios"
const api_root=process.env.VUE_APP_API_ROOT===undefined?'':process.env.VUE_APP_API_ROOT
 

export default {
  name: 'manpowerutilization',
  components: {
   barchart
    
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
          
          var url=api_root+'/mtpinfoshare/ajax/mtp01'
          //{headers: {
       //'Access-Control-Allow-Origin': '*',
       //'Content-type': 'application/json',
    //}}
          axios.get(url)
                .then((response) => {
                                var labels=response.data.labels
                                var data1=response.data.data1
                                
                                var data2=response.data.data2
                                console.log(labels)
                                var data3=response.data.data3
                                var data4=response.data.data4
                                var data5=response.data.data5
                                var data6=response.data.data6
                                //var data7=response.data.data7
                                //var data8=response.data.data8
                                var data9=response.data.data9
                                var data10=response.data.data10
                                var data11=response.data.data11
                                var data12=response.data.data12
                                var data13=response.data.data13
                               var data14=response.data.data14
                               // var data15=response.data.data.data15
                               // var data16=response.data.data.data16
                               // var data17=response.data.data.data17
                               // var data18=response.data.data.data18
                               // var data19=response.data.data.data19
                               // var data20=response.data.data.data20
                                this.chartData1= {
        labels: labels,
        datasets: [{
            label: '# act hrs',
            data: data1,
            backgroundColor:
                'rgb(55,167,187)',},
            {
            label: '# std hrs',
            data: data2,
            backgroundColor:
                'rgb(255,128,128)',},

               ]
        };
        this.chartOptions1= {
      responsive: true,
      maintainAspectRatio: false
    }
    this.chartData2={
        labels: labels,
        datasets: [{
            label: '# act hrs',
            data: data1,
            stack:'a',
            backgroundColor:
                'rgb(55,167,187)',},
            {
            label: '# idle hrs',
            data: data3,
                stack:'a',
            backgroundColor:
                'rgb(255,128,128)',},
            {
            label: '# absent hrs',
            data: data4,
                stack:'a',
            backgroundColor:
                'rgb(236,19,73)',},
            {
            label: '# std hrs',
            data: data2,
                stack:'b',
            backgroundColor:
                'rgb(0,128,0)',},
               ]
            }

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
        this.chartData3={
        labels: labels,
        datasets: [{
            label: '#  no job',
            data: data5,
            backgroundColor:
                'rgb(55,167,187)',},
            {
            label: '# no raw mat',
            data: data6,
            backgroundColor:
                'rgb(255,128,128)',},
            {
            label: '# no mfg parts',
            data: data9,
            backgroundColor:
                'rgb(0,128,0)',},
            {
            label: '# mech repair',
            data: data10,
            backgroundColor:
                'rgb(128,0,0)',},
            {
            label: '# elect repair',
            data: data11,
            backgroundColor:
                'rgb(223,223,0)',},
            {
            label: '#no machine',
            data: data12,
            backgroundColor:
                'rgb(255,255,45)',},
            {
            label: '# no power',
            data: data13,
            backgroundColor:
                'rgb(0,210,210)',},
            {
            label: '# no tools',
            data: data14,
            backgroundColor:
                'rgb(98,132,251)',},

               ]
            }
        this.chartOptions3={
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