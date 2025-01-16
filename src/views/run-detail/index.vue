<template>
  <div>
    <h1>Live video streaming</h1>
    <div class="video-container">
      <img :src="videoStreamUrl" alt="Video Stream" class="video-stream">
    </div>
    <el-row :gutter="40" class="panel-group">
      <el-col
        v-for="student in studentList"
        :key="student.username"
        :xs="12"
        :sm="12"
        :lg="6"
        class="card-panel-col"
      >
        <div class="card-panel" @click="handleCourseRun(student.name)">
          <div class="card-panel-icon-wrapper icon-people">
            <!-- <svg-icon icon-class="peoples" class-name="card-panel-icon" /> -->
            <img :src="'data:image/png;base64,' + student.image" alt="Student Image" class="card-panel-icon">
          </div>
          <div class="card-panel-description">
            <div class="card-panel-text">
              {{ student.name }}
            </div>
            <!-- <count-to :start-val="0" :end-val="course.number" :duration="2600" class="card-panel-num" /> -->
            <div class="card-panel-subtext" :style="{ color: student.check_in ? 'green' : 'red' }">
              {{ student.check_in ? 'Attended' : 'Absence' }}
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
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
      videoStreamUrl: 'http://localhost:5001/video_feed',
      courseId: '',
      runId: '',
      studentList: []
    }
  },
  created() {
    this.courseId = this.$route.query.courseId
    this.runId = this.$route.query.runId
  },
  mounted() {
    this.fetchDetail()
  },
  methods: {
    fetchDetail() {
      axios
        .get('http://localhost:5000/student/runDetail', {
          params: {
            courseId: this.courseId,
            runId: this.runId
          }
        })
        .then((response) => {
          this.studentList = response.data.students
          console.log('获取学生列表成功:', this.studentList)
        })
        .catch((error) => {
          console.error('获取学生列表失败:', error)
        })
    },
    handleCourseRun(courseId) {
      this.$router.push({ path: '/documentation/index' })
      // this.$emit('handleSetLineChartData', courseId)
    }
  }
}
</script>

  <style lang="scss" scoped>
  .video-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px; // 可选：添加一些底部间距
  }

  .video-stream {
  width: 100%;
  max-width: 800px;
  }

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
        width: 50px; /* 设置图片宽度 */
        height: 60px; /* 设置图片高度 */
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
          color: #00000073;
          font-size: 16px;
          margin-bottom: 12px;
        }

        .card-panel-num {
          font-size: 20px;
        }

        .card-panel-subtext {
        font-size: 18px;
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
