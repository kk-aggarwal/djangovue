<script>
import { HorizontalBar,mixins } from 'vue-chartjs'

export default {
  extends: HorizontalBar,
  mixins: [mixins.reactiveProp],
  props: {
    chartData: {
      type: Object,
      default: null
    },
    options: {
      type: Object,
      default: null
    }
  },
  mounted () {
    console.log(this.chartdata)
    this.renderChart(this.chartData, this.options)
  },
  data: () => ({
    chartdat: {
      labels: ['January', 'February'],
      datasets: [
        {
          label: 'Data One',
          backgroundColor: '#f87979',
          data: [40, 20]
        }
      ]
    },
    option: {
      responsive: true,
      maintainAspectRatio: false
    }
  }),
}

</script>