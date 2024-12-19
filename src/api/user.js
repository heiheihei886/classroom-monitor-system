import request from '@/utils/request'

export function login(data) {
  console.log('执行登录请求')
  return request({
    // url: '/vue-element-admin/user/login',
    url: '/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  console.log('执行用户信息请求')
  return request({
    url: '/get_user_info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-element-admin/user/logout',
    method: 'post'
  })
}
