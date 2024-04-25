---
layout: post
title: "axios 커스텀해서 사용하기"
date: 2024-03-02 10:06:52 +0900
categories: javascript
tags: javascript axios
published : false
---

const instance: AxiosInstance = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_BASE_URI,
  headers: {
    Authorization: ''
  }
})
const sourceRequest = {
  any: Date
}
const CancelToken = axios.CancelToken
instance.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = localStorage.getItem('token')
    const r_token = localStorage.getItem('refreshToken')
    const gwapi = useMainStore().gwapi
    if (gwapi) {
      config.baseURL = gwapi
    }
    if (token && config.headers && !config.headers.Authorization) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    if (!token && !config.headers.Authorization) {
      config.headers['Authorization'] = `Bearer ${useMainStore().user.token}`
    } else if (token.length < 2 && !config.headers.Authorization) {
      config.headers['Authorization'] = `Bearer ${useMainStore().user.token}`
    }
    if (config.url === '/v2/authenticate/token/issue') {
      if (!r_token) {
        config.headers['Authorization'] = `Bearer ${
          useMainStore().user.refreshToken
        }`
      } else if (r_token.length < 2) {
        config.headers['Authorization'] = `Bearer ${
          useMainStore().user.refreshToken
        }`
      } else {
        config.headers['Authorization'] = `Bearer ${r_token}`
      }
    }

    const key = `${config.url}$${JSON.stringify(config.data)}`
    if (sourceRequest[key]) {
      if (config.method !== 'post') return config
      if (config.url.includes('enter')) return config
      if (Date.now() - sourceRequest[key] < 2000) {
        const source = CancelToken.source()
        config.cancelToken = source.token
        source.cancel()
      } else {
        sourceRequest[key] = Date.now() // 중복호출이 아닌 경우 새로운 키 발급
      }
    } else {
      sourceRequest[key] = Date.now() // 중복호출이 아닌 경우 새로운 키 발급
    }
    // "get" | "GET" | "delete" | "DELETE" | "head" | "HEAD" | "options" | "OPTIONS" | "post" | "POST" | "put" | "PUT" | "patch" | "PATCH" | "purge" | "PURGE" | "link" | "LINK" | "unlink" | "UNLINK"
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)
instance.interceptors.response.use(
  (response: AxiosResponse) => {
    if (response.data.ok || response.status === 200) return response
  },
  async (error) => {
    //  token error 401 || 400 && 6101,6203,6204,6205,6106,6107
    if (error.name == 'CanceledError') return true
    const { response } = error
    if (response && response.data) {
      const cd = response.data.errorState.code
      const msg = response.data.errorState.message
      if (cd === 404) return true
      if (cd === 6101 || response.status === 401 || response.status === 403) {
        if (response.config.url.indexOf('issue') > 0) {
          // token issue 때 401 응답왔을 때 무한 호출 방지
          useMainStore().popupList.popDenial.name = `마이올린 JOY 학습앱을 다시 실행해 주세요.`
          useMainStore().popupList.popDenial.class = 'close'
          useMainStore().isLoading = false
          return
        }
        //401 token 만료 // 403 무체주문 종료
        try {
          const { data } = await API.authTokenRefresh()
          const originalRequest = error.config
          localStorage.setItem('token', data.result.authToken)
          localStorage.setItem('refreshToken', data.result.refreshToken)
          useMainStore().user.token = data.result.authToken
          useMainStore().user.refreshToken = data.result.refreshToken
          originalRequest.headers.Authorization = `Bearer ${data.result.authToken}`
          if (response.status === 403) {
            useMainStore().setNewUserInfo()
          } else {
            const data2 = await axios(originalRequest)
            return data2
          }
        } catch (rerror) {
          useMainStore().popupList.popDenial.name = `마이올린 JOY 학습앱을 다시 실행해 주세요.`
          useMainStore().popupList.popDenial.class = 'close'
          useMainStore().isLoading = false
        }
      } else if (cd === 3201 || cd === 3200) {
        // 미니게임 구매 불가 팝업 응답값 return
        return response
      } else {
        useMainStore().popupList.popDenial.name = `마이올린 JOY 학습앱을 다시 실행해 주세요.`
        useMainStore().popupList.popDenial.class = 'close'
        useMainStore().isLoading = false
      }
      const code = response.data.errorState.code
      const message = response.data.errorState.message
      console.error(`[Axios Error]`, `code: ${code}`, `msg: ${message}`)
      return Promise.reject({ code, msg })
    } else {
      if (error.code == 'ERR_NETWORK' && error.response.status == 0) {
        const originalRequest = error.config
        if (!navigator.onLine) {
          useMainStore().popupList.popDenial.name =
            '와이파이가 연결되어 있지 않거나,<br />연결 상태가 불안정해요.<br />와이파이 연결을 확인해 주세요!'
          useMainStore().popupList.popDenial.class = 'wifi'
          useMainStore().isLoading = false
        } else {
          useMainStore().popupList.popDenial.name = `네트워크 연결이 원활하지 않아요.<br />잠시 후에 다시 시도해 주세요!`
          useMainStore().popupList.popDenial.class = 'close'
          useMainStore().isLoading = false
        }
      } else {
        useMainStore().popupList.popDenial.name = `마이올린 JOY 학습앱을 다시 실행해 주세요.`
        useMainStore().popupList.popDenial.class = 'close'
        useMainStore().isLoading = false
      }
      console.error(error)
    }
    return Promise.reject(error)
  }
)
export default instance
