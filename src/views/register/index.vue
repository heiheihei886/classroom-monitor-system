<template>
  <div class="register-container">
    <el-form ref="registerForm" :model="registerForm" :rules="registerRules" class="register-form" autocomplete="on" label-position="left">
      <div class="title-container">
        <h3 class="title">Register</h3>
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="username"
          v-model="registerForm.username"
          placeholder="Email"
          name="username"
          type="text"
          tabindex="1"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="name">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="name"
          v-model="registerForm.name"
          placeholder="Name"
          name="name"
          type="text"
          tabindex="1"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="password"
          v-model="registerForm.password"
          placeholder="Password"
          name="password"
          type="text"
          tabindex="1"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="studentId">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          ref="studentId"
          v-model="registerForm.studentId"
          placeholder="Student ID"
          name="studentId"
          type="text"
          tabindex="2"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="major">
        <span class="svg-container">
          <svg-icon icon-class="education" />
        </span>
        <el-input
          ref="major"
          v-model="registerForm.major"
          placeholder="Student major"
          name="major"
          type="text"
          tabindex="2"
          autocomplete="on"
        />
      </el-form-item>

      <el-form-item prop="courses">
        <!-- <span class="svg-container">
          <svg-icon icon-class="education" />
        </span> -->
        <el-select
          v-model="registerForm.courses"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="Select courses"
          style="width: 100%"
        >
          <el-option
            v-for="item in courses"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>

      <el-form-item prop="avatar">
        <span class="svg-container">
          <svg-icon icon-class="picture" />
        </span>
        <el-upload
          class="avatar-uploader"
          :show-file-list="false"
          :before-upload="handleAvatarChange"
        >
          <img v-if="imageUrl" :src="imageUrl" class="avatar">
          <i v-else class="el-icon-plus avatar-uploader-icon" />
        </el-upload>
        <p class="upload-description">Please upload avatar</p>
      </el-form-item>

      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="handleRegister">Register</el-button>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    const validateName = (rule, value, callback) => {
      if (!value) {
        callback(new Error('Please enter your name'))
      } else {
        callback()
      }
    }
    const validateStudentId = (rule, value, callback) => {
      if (!value) {
        callback(new Error('Please enter your student ID'))
      } else {
        callback()
      }
    }
    return {
      registerForm: {
        username: '',
        name: '',
        password: '',
        studentId: '',
        major: '',
        courses: [],
        avatar: ''
      },
      registerRules: {
        name: [{ required: true, trigger: 'blur', validator: validateName }],
        studentId: [{ required: true, trigger: 'blur', validator: validateStudentId }],
        courses: [{ type: 'array', required: true, message: 'Please select at least one course', trigger: 'change' }]
      },
      courses: [ // 可选项数组
        { value: 'Math', label: 'Mathematics' },
        { value: 'Science', label: 'Science' },
        { value: 'History', label: 'History' },
        { value: 'Art', label: 'Art' }
      ],
      imageUrl: '',
      loading: false
    }
  },
  methods: {
    handleRegister() {
      this.$refs.registerForm.validate(async(valid) => {
        if (valid) {
          this.loading = true

          try {
            // 构建 FormData 对象
            const formData = new FormData()
            formData.append('username', this.registerForm.username)
            formData.append('name', this.registerForm.name)
            formData.append('password', this.registerForm.password)
            formData.append('studentId', this.registerForm.studentId)
            formData.append('subject', this.registerForm.major)
            formData.append('course_ids', JSON.stringify(this.registerForm.courses)) // 数组转成字符串
            if (this.registerForm.avatar) {
              formData.append('file', this.registerForm.avatar) // 头像文件
            }
            for (const [key, value] of formData.entries()) {
              console.log(key, value)
            }

            // 使用 axios 发送 POST 请求到后端
            const response = await axios.post('http://localhost:5000//student/register', formData, {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            })

            // 处理后端返回的响应
            if (response.data.success) {
              this.$message.success('Registration successful!')
              this.$router.push({ path: '/login' })
            } else {
              this.$message.error(response.data.message || 'Registration failed!')
            }
          } catch (error) {
            console.error('Error during registration:', error)
            this.$message.error('An error occurred while submitting the form.')
          } finally {
            this.loading = false
          }
        } else {
          this.$message.error('Please complete the form correctly before submitting!')
          return false
        }
      })
    },

    handleAvatarChange(file) {
    // 创建一个 FileReader 用于预览
      const reader = new FileReader()
      reader.onload = (e) => {
        this.imageUrl = e.target.result // 本地显示图片
        this.registerForm.avatar = file // 保存文件对象，供后续提交使用
      }
      reader.readAsDataURL(file) // 转为 base64
      return false // 阻止默认上传行为
    },
    beforeAvatarUpload(file) {
      const isJPGorPNG = file.type === 'image/jpeg' || file.type === 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPGorPNG) {
        this.$message.error('Avatar picture must be JPG or PNG format!')
      }
      if (!isLt2M) {
        this.$message.error('Avatar picture size can not exceed 2MB!')
      }
      return isJPGorPNG && isLt2M
    }
  }
}
</script>

  <style lang="scss">
  /* 修复input 背景不协调 和光标变色 */
  /* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

  $bg:#283443;
  $light_gray:#fff;
  $cursor: #fff;

  @supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
    .register-container .el-input input {
      color: $cursor;
    }
  }

  /* reset element-ui css */
  .register-container {
    .el-input {
      display: inline-block;
      height: 47px;
      width: 85%;

      input {
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
        caret-color: $cursor;

        &:-webkit-autofill {
          box-shadow: 0 0 0px 1000px $bg inset !important;
          -webkit-text-fill-color: $cursor !important;
        }
      }
    }

    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }
  }
  </style>

  <style lang="scss" scoped>
  $bg:#2d3a4b;
  $dark_gray:#889aa4;
  $light_gray:#eee;

  .register-container {
    min-height: 100%;
    width: 100%;
    background-color: $bg;
    overflow: hidden;

    .register-form {
      position: relative;
      width: 520px;
      max-width: 100%;
      padding: 160px 35px 0;
      margin: 0 auto;
      overflow: hidden;
    }

    .tips {
      font-size: 14px;
      color: #fff;
      margin-bottom: 10px;

      span {
        &:first-of-type {
          margin-right: 16px;
        }
      }
    }

    .svg-container {
      padding: 6px 5px 6px 15px;
      color: $dark_gray;
      vertical-align: middle;
      width: 30px;
      display: inline-block;
    }

    .title-container {
      position: relative;

      .title {
        font-size: 26px;
        color: $light_gray;
        margin: 0px auto 40px auto;
        text-align: center;
        font-weight: bold;
      }
    }

    .avatar-uploader .el-upload {
      border: 1px dashed #d9d9d9;
      border-radius: 6px;
      cursor: pointer;
      position: relative;
      overflow: hidden;
    }
    .avatar-uploader .el-upload:hover {
      border-color: #409EFF;
    }
    .avatar-uploader-icon {
      font-size: 28px;
      color: #8c939d;
      width: 178px;
      height: 178px;
      line-height: 178px;
      text-align: center;
    }
    .avatar {
      width: 178px;
      height: 178px;
      display: block;
    }
    .upload-description {
      margin-top: 10px; /* 调整文字说明与上传组件的距离 */
      color: #999; /* 设置文字颜色 */
      font-size: 14px; /* 设置文字大小 */
    }
  }
  </style>
