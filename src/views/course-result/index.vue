<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'
import axios from 'axios'
// import { run } from 'runjs'

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
      default: '600px'
    }
  },
  data() {
    return {
      chart: null,
      courseId: '',
      username: '',
      runId: '',
      chartData: []
    }
  },
  created() {
    this.courseId = this.$route.query.courseId
    this.runId = this.$route.query.runId
    this.username = this.$route.query.username
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
          formatter: '{a} <br/>{b} : {c} ({d}%)',
          textStyle: {
            fontSize: 16 // 调整这里
          }
        },
        legend: {
          left: 'center',
          bottom: '10',
          data: ['Happy', 'Surprise', 'Neutral', 'Sad', 'Disgust'],
          textStyle: {
            fontSize: 16 // 调整这里
          }
        },
        series: [
          {
            name: 'WRITE ARTICLES',
            type: 'pie',
            roseType: 'radius',
            // radius: [15, 95],
            radius: [20, 100],
            center: ['50%', '50%'],
            data: this.chartData,
            animationEasing: 'cubicInOut',
            animationDuration: 2600
          }
        ]
      })
    },
    fetchCourseBehavourData() {
      axios
        .get('http://localhost:5000/student/courseBehaviour', {
          params: {
            username: this.username,
            runId: this.runId,
            courseId: this.courseId
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
