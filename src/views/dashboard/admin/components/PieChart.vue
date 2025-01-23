<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'
import axios from 'axios'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '300px'
    },
    username: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      chart: null,
      chartData: []
    }
  },
  created() {
    this.fetchCourseBehavourData()
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')

      this.chart.setOption({
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          left: 'center',
          bottom: '10',
          data: ['Happy', 'Surprise', 'Neutral', 'Sad', 'Disgust']
        },
        series: [
          {
            name: 'EMOTION ARTICLES',
            type: 'pie',
            roseType: 'radius',
            radius: [15, 95],
            center: ['50%', '38%'],
            data: this.chartData,
            animationEasing: 'cubicInOut',
            animationDuration: 2600
          }
        ]
      })
    },
    fetchCourseBehavourData() {
      console.log('开始获取图表数据:', this.username)
      axios
        .get('http://localhost:5000/professor/generalBehaviour', {
          params: {
            username: this.username
          }
        })
        .then((response) => {
          const courseData = response.data
          console.log('获取课程数据成功:', courseData)

          // 提取 emotions 数据
          if (courseData && courseData.emotions) {
            this.chartData = courseData.emotions
            console.log('chartData:', this.chartData)
            this.initChart() // 初始化图表
          }
        })
        .catch((error) => {
          console.error('获取课程数据失败:', error)
        })
    }
  }
}
</script>
