---
layout: post
title: "axios 커스텀해서 사용하기"
summary: axios interceptors로 토큰 재발급하기
date: 2024-05-20 10:06:52 +0900
categories: javascript
tags: javascript axios
---

오늘은 제가 axios 를 사용하는 방법을 설명해보려고 합니다. fetch보다 사용하기 편리해서 axios를 자주 사용했습니다. 특히 Axios 에서 지원하는 interceptors를 사용하면 jwt + access Token을 사용할 때 정말 편하게 사용할 수 있습니다. axios 사용하는 방법과 custom, 토큰 재발급 받는 과정을 알아봅시다.

# Axios
[Axios](https://axios-http.com/kr/)는 <span class="h-yellow">Promise 기반 HTTP 통신 라이브러리</span>입니다. 요청 및 응답 인터셉트, 응답 데이터 변환, 요청 취소 등 다양한 API 와 기능을 제공합니다. axios를 불러와서 axios.get('url',config) 형식으로 간편하게 사용할 수 있습니다.

# Axios custom
Axios에서 제공하는 Axios 인스턴스를 사용하여 사용자 지정 config로 새로운 Axios 인스턴스를 생성할 수 있습니다. 
## create 
axios.ts 파일을 생성해준 후 axios.create([config]) 작성을 해줍니다.

```javascript
const instance: AxiosInstance = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_BASE_URI,
  timeout: 1000,
  headers: {
    Authorization: '',
    ContentType: 'application/json',
  }
})
```

- baseURL : default로 설정된 url, baseURL + url 로 요청
- timeout : 요청 기다릴 시간 ( 시간보다 길어지면 요청이 중단됨 )
- headers : 사용자 지정 헤더

## Axios interceptors

Axios는 비동기 기반이기때문에 then 또는 catch 로  에러 핸들링을 할 수 있는데요. axios interceptors를 통해 then 또는 catch로 처리되기 전에 요청과 응답을 가로챌 수 있습니다. 여기서 요청 전달 전, 또는 응답 데이터 받기 전에 공통으로 작업될 내용들을 작성해줍니다.

```javascript
// 요청
axios.interceptors.request.use(function (config) {
  // 요청이 전달되기 전
  return config;
}, function (error) {
  // 에러 핸들링, 호출한 곳에서 error 를 return 받음
  return Promise.reject(error);
});

// 응답 인터셉터 추가하기
axios.interceptors.response.use(function (response) {
  // status code 2xx 
  // 응답 데이터가 있는 작업 수행
  return response;
}, function (error) {
  // status code 2xx 제외한 응답 
  // 에러 핸들링, 호출한 곳에서 error 를 return 받음
  return Promise.reject(error);
});
```

- 요청 : interceptors.<span class="h-yellow">request</span>.use()
- 응답 : interceptors.<span class="h-yellow">response</span>.use()

## 토큰 재발급
사용자의 인터렉션으로 수만은 요청과 응답을 주고받을 때, 항상 accessToken이 담아서 요청을 하겠죠? 이를 받는 곳에서는 해당 token이 정상이라면 statusCode 200, 만료된 토큰이라면 statusCode 401로 응답을 주기로 약속했습니다.
interceptors.response를 사용해서 statusCode가 2xx이 아닐 때 처리하는 함수에서 토큰 재발급 요청을 해보겠습니다.

```javascript
instance.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    const token = getToken()
    if (!token) {
      window.location.href = '/login';
    }
    config.headers['Authorization'] = `Bearer ${token}`
   
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
    const { response } = error
    if (response && response.data) {
      const code = response.data.errorState.code
      const message = response.data.errorState.message
      if (response.status === 401) {
        if (response.config.url.indexOf('issue') > 0) {
          // token issue 중복호출되었을 경우 login page로 redirect 시킴
          return window.location.href = "/login"
        }
        //401 token 만료
        const { data } = await API.authTokenRefresh()
        // 새로운 토큰 저장
        sessionStorage.setItem('token', data.result.accessToken)
        // 새로운 토큰으로 재요청 ❗️ 중요
        error.config.headers.Authorization = `Bearer ${data.result.accessToken}`;
        return instance(error.config)
      } else if (response.status === 404) {
        window.location.href = "/notFound"
      }
      return Promise.reject({ code, message })
    } else {
      return Promise.reject(error)
    }
  }
)
export default instance
```

❗️ 중요

라고 표시한 부분은 제가 생각했을 때 중요하다고 생각되는 부분입니다. 사용자가 토큰이 만료됐다는 이유로 응답을 받지 못하고 오류 화면을 마주하거나, 갑자기 로그인 페이지로 리다이렉트가 된다면 엄청 당황스러울 것입니다. 이전에 요청을 다시 새로운 토큰으로 요청을 해주면 사용자는 토큰이 만료됐다가 새로 발급받았다는 것도 눈치챌 수도 없습니다. 이를 동작 할 수 있게 하는 이전 요청은 error 객체 안에 config 에 담겨있습니다. 그래서 새로운 토큰을 발급받고 나면 instance에 새로운 토큰을 발급받은 후 재요청을 해줍니다.

마지막으로 토큰 재발급 api 요청하는 코드입니다.

```javascript
const API = {
  authTokenRefresh: async () =>
    await axios.get('url', {
      params: {
        ...
      },
      headers: {
        RefreshToken: getRefreshToken()
      }
    }),
    ...
}
```



const CancelToken = axios.CancelToken
instance.interceptors.request.use(
	(config: AxiosRequestConfig) => {
		const key = `${config.url}$${JSON.stringify(config.data || config.params)}`
		if (sourceRequest[key]) {
      if (Date.now() - sourceRequest[key] < 2000) { //2초 이내에 같은 요청이 오면 취소 요청
        const source = CancelToken.source()
        config.cancelToken = source.token
        source.cancel()
      } else {
        sourceRequest[key] = Date.now() // 중복호출이 아닌 경우 새로운 키 발급
      }
    } else {
      sourceRequest[key] = Date.now() // 중복호출이 아닌 경우 새로운 키 발급
    }
	},
  (error) => {
    return Promise.reject(error)
  }
)