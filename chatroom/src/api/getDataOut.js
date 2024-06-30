import base from './index'
let axios = base.axios
let baseUrl = base.baseUrl
import request from "@/utils/request";
// 获取一个参数指定索引的面试经验
export const getExperienceWithOfset = params => {
    // console.log(params)
    return request.post("/getExperienceWithOfset",{
        data:params
    }).then(res=>res)
    // return axios({
    //     method: 'post',
    //     baseURL: `${baseUrl}/api/getExperienceWithOfset`,
    //     data: params
    // }).then(res => res.data)
}

export const getCompanyJobInformationWithOfset = params =>{
    // return axios({
    //     method: 'post',
    //     baseURL: `${baseUrl}/api/getCompanyJobInformationWithOfset`,
    //     data: params
    // }).then(res => res.data)
    return request.post("/getCompanyJobInformationWithOfset",{
        data:params
    }).then(res=>res)
}

export const getTechnicalQuestion = params =>{
    // return axios({
    //     method: 'post',
    //     baseURL: `${baseUrl}/api/getTechnicalQuestion`,
    //     data: params
    // }).then(res => res.data)
    return request.post("/getTechnicalQuestion",{
        data:params
    }).then(res=>res)
}

export const getLLMQuestion = params =>{
    return request.post("/getLLMQuestion",{
        data:params
    }).then(res=>res)
}

