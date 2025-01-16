<template>
  <el-row :gutter="40" class="panel-group">
    <el-col
      v-for="courseRun in courseRunList"
      :key="courseRun.id"
      :xs="12"
      :sm="12"
      :lg="6"
      class="card-panel-col"
    >
      <div class="card-panel" @click="handleCourseRun(courseRun.id, courseRun.runId)">
        <div class="card-panel-icon-wrapper icon-people">
          <svg-icon icon-class="peoples" class-name="card-panel-icon" />
        </div>
        <div class="card-panel-description">
          <div class="card-panel-text">
            {{ courseRun.time }}
          </div>
          <!-- <count-to :start-val="0" :end-val="course.number" :duration="2600" class="card-panel-num" /> -->
          <div class="card-panel-subtext">
            {{ courseRun.classroom }}
          </div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
// import CountTo from 'vue-count-to'
import axios from 'axios'

export default {
  // components: {
  //   CountTo
  // },
  data() {
    return {
      courseId: '',
      courseRunList: []
    }
  },
  created() {
    this.courseId = this.$route.query.courseId
    console.log('Received Course ID:', this.courseId)
  },
  mounted() {
    this.fetchCourseRun()
  },
  methods: {
    fetchCourseRun() {
      axios
        .get('http://localhost:5000/professor/courseRunList', {
          params: {
            courseId: this.courseId
          }
        })
        .then((response) => {
          this.courseRunList = response.data.runs
          console.log('获取课程列表run成功:', this.courseRunList)
        })
        .catch((error) => {
          console.error('获取课程列表失败:', error)
        })
    },
    handleCourseRun(courseId, runId) {
      console.log('跳转detail中,课程id:', courseId + 'runId:', runId)
      this.$router.push({ path: '/runDetail/index', query: { courseId: courseId, runId: runId }})
      // this.$emit('handleSetLineChartData', courseId)
    }
  }
}
</script>

<style lang="scss" scoped>
.panel-group {
  margin-top: 18px;

  .card-panel-col {
    margin-bottom: 32px;
  }

  .card-panel {
    height: 108px;
    cursor: pointer;
    font-size: 12px;
    position: relative;
    overflow: hidden;
    color: #666;
    background: #fff;
    box-shadow: 4px 4px 40px rgba(0, 0, 0, .05);
    border-color: rgba(0, 0, 0, .05);

    &:hover {
      .card-panel-icon-wrapper {
        color: #fff;
      }

      .icon-people {
        background: #40c9c6;
      }

      .icon-message {
        background: #36a3f7;
      }

      .icon-money {
        background: #f4516c;
      }

      .icon-shopping {
        background: #34bfa3
      }
    }

    .icon-people {
      color: #40c9c6;
    }

    .icon-message {
      color: #36a3f7;
    }

    .icon-money {
      color: #f4516c;
    }

    .icon-shopping {
      color: #34bfa3
    }

    .card-panel-icon-wrapper {
      float: left;
      margin: 14px 0 0 14px;
      padding: 16px;
      transition: all 0.38s ease-out;
      border-radius: 6px;
    }

    .card-panel-icon {
      float: left;
      font-size: 48px;
    }

    .card-panel-description {
      float: right;
      font-weight: bold;
      margin: 26px;
      margin-left: 0px;

      .card-panel-text {
        line-height: 18px;
        color: rgba(0, 0, 0, 0.45);
        font-size: 16px;
        margin-bottom: 12px;
      }

      .card-panel-num {
        font-size: 20px;
      }
    }
  }
}

@media (max-width:550px) {
  .card-panel-description {
    display: none;
  }

  .card-panel-icon-wrapper {
    float: none !important;
    width: 100%;
    height: 100%;
    margin: 0 !important;

    .svg-icon {
      display: block;
      margin: 14px auto !important;
      float: none !important;
    }
  }
}
</style>
