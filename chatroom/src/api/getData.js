import base from './index'
let axios = base.axios
let baseUrl = base.baseUrl

// 获取好友
export const getFriend = params => {
    return axios({
      method: 'post',
      baseURL: `${baseUrl}/friend/friendList`,
      data: params
    }).then(res => res.data)
  }

  // 获取聊天信息
export const getChatMsg = params => {
  return axios({
    method: 'post',
    baseURL: `${baseUrl}/friend/chatMsg`,
    data: params
  }).then(res => res.data)
}

// 获取一个参数指定索引的面试经验
export const getExperienceWithOfset = params => {
  // console.log(params)
  return axios({
    method: 'post',
    baseURL: `${baseUrl}/experience`,
    data: params
  }).then(res => res.data)
}

// 获取公司的岗位
export const getCompanyJobList = params => {
  return axios({
    method: 'post',
    baseURL: `${baseUrl}/company/jobs`,
    data: params
  }).then(res => res.data)
}

// 获取公司的岗位信息
export const getCompanyJobInformationList = params => {
  return axios({
    method: 'post',
    baseURL: `${baseUrl}/company/jobs`,
    data: params
  }).then(res => res.data)
}