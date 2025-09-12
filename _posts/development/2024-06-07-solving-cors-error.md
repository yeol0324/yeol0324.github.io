---
layout: post
title: CORS 뭔데 이렇게 자주 만나?
summary: 
date: 2024-06-07 10:12:01 +09:00
categories: development
tags: cors
---

웹개발을 하고 있다면 CORS 에러를 한 번쯤은 겪어보셨을 겁니다. 저는 정말 다양한 일도 있었고, 하루 이틀을 통채로 날린 적도 있었는데요. 오늘은 일반적으로 CORS 에러가 발생하는 상황과 이를 해결하는 방법, 그리고 프론트엔드 개발자 입장에서 이런 문제를 어떻게 다뤄야 할지에 대해 이야기해보겠습니다.

# CORS 에러
CORS(Cross-Origin Resource Sharing)는 다른 출처에서 리소스를 요청할 때 보안상의 이유로 발생하는 문제입니다. 최신 브라우저에서 구현된 동일 출처 정책(same-origin policy) 때문에 등장했는데, 브라우저는 보안 정책에 따라 다른 출처에서 리소스를 요청하는 것을 제한합니다. 여기서 출처(Origin)란 <span class="h-yellow">프로토콜, 도메인, 포트</span>를 의미합니다.

예를 들어, 
- http://example.com 과 https://example.com
- https://example.com:8080 과 https://example.com:80
- https://example.com 과 https://m.example.com

들은 다른 출처로 간주됩니다.

CORS 정책이 없이 자유롭게 다른 출처로 요청을 보낼 수 있다면, 정보를 빼내는 코드를 담은 요청을 API에 보내서 인증 정보를 가져온다던지, 무한요청을 보내서 웹서버를 터뜨리는 일도 가능할 것입니다. 이런 상황을 방지하기 위해 <b>허용되지않은 출처</b>에서 보내는 요청을 브라우저단에서 막는 것입니다.

# CORS 요청과 동작 과정

CORS는 웹 애플리케이션이 다른 출처의 자원에 접근할 수 있게 해주는 보안 메커니즘입니다.
단순 요청과 예비 요청으로 나뉘며, 서버는 특정 헤더를 사용하여 어떤 출처가 자원을 공유할 수 있는지 지정합니다.
브라우저는 서버의 CORS 설정을 확인한 후, 요청을 진행하거나 차단합니다.
이를 통해 CORS는 웹 애플리케이션이 보안성을 유지하면서도 다른 출처의 자원을 안전하게 사용할 수 있도록 합니다.
CORS 요청은 크게 두 가지로 나눌 수 있습니다.

## 단순 요청 (Simple Request)

예비 요청 없이 서버에 바로 요청.

- GET, POST, HEAD 메서드 사용
- 요청 헤더가 Accept, Accept-Language, Content-Language, Content-Type 중 하나만 포함.
- Content-Type이 application/x-www-form-urlencoded, multipart/form-data, text/plain 중 하나

## 단순 요청 과정
1. 클라이언트 요청
단순 요청 조건에 맞는 요청 전송
2. 서버 응답
CORS 헤더 포함 응답 헤더에 Access-Control-Allow-Origin 헤더를 포함하여 요청을 처리하고 응답
3. 브라우저 처리
응답을 받아 요청이 허용된 출처에서 온 것인지 확인 후 응답을 처리, 아니라면 CORS 에러를 발생

## 예비 요청 (Preflight Request)

위 단순 요청의 조건을 만족하지 않는 모든 요청.

단순 요청과는 다르게 현재 요청이 유효한지를 확인하기 위해 OPTIONS 메서드로 예비 요청을 보내는 것입니다. 개발자 도구의 Network 탭에서 모든 요청을 확인해보면 같은 api가 내가 보내지 않은 OPTIONS 메서드로 먼저 요청되는 것을 볼 수 있는데요! 바로 이겁니다.

이게 왜 필요할까요? 내가 요청이 CORS 정책을 위반하는 요청이라면 통신은 되지 않고, 불필요한 트래픽이 발생한 것입니다.

이를 방지하기 위해서 예비요청을 먼저 날려서 유효한 요청인지 확인하는 절차가 생기게 됐습니다. OPTIONS 메서드를 사용하여 실제 요청을 보내기 전에 서버가 해당 출처의 요청을 허용하는지 확인합니다.

## 예비 요청 과정
1. 예비 요청 
브라우저가 OPTIONS 메서드를 사용하여 실제 요청 전 서버가 해당 요청을 허용하는지 확인차 서버에 예비 요청 전송

Request Headers 
```
Access-Control-Request-Headers:authorization
Access-Control-Request-Method:GET
Origin: https://example.com
```

나 https://example.com 인데 헤더에 authorization 담아서 GET 요청 보내도 됨?

2. 서버 응답
서버는 예비 요청을 받고, 응답 헤더에 결과를 포함하여 응답

Response Headers
```
Access-Control-Allow-Headers: Origin, x-device-info, Content-Type,  Authorization
Access-Control-Allow-Methods: GET, POST, PUT, OPTIONS, HEAD
Access-Control-Allow-Origin: *
Access-Control-Expose-Headers: Authorization
Access-Control-Max-Age: 3600
```

ㅇㅇ 모든 도메인 요청 다 받아줌! 그리고 헤더에는  Origin, x-device-info, Content-Type,  Authorization 이것들이 포함되도 되고 GET, POST, PUT, OPTIONS, HEAD 메소드를 사용할 수 있어, 이 예비 요청에 대한 캐싱은 3600 초만 가능해.

3. 실제 요청
예비 요청이 성공하면, 단순 요청에서 했던 과정과 같은 실제 요청이 이루어집니다.

## 요청 헤더 종류

이처럼 CORS는 HTTP 헤더를 통해 동작합니다.

<b>Access-Control-Allow-Origin : </b> 허용하는 출처

<b>Access-Control-Allow-Methods : </b> 허용하는 HTTP 메서드

<b>Access-Control-Allow-Headers</b> 허용하는 커스텀 헤더

<b>Access-Control-Allow-Credentials</b> 자격 증명(쿠키 등) 포함한 요청 허용 여부

<b>Access-Control-Max-Age</b> 예비 요청의 결과를 브라우저가 캐시할 수 있는 시간

<b>Access-Control-Expose-Headers</b> 클라이언트가 응답에서 접근할 수 있는 헤더 목록


# 상황별 해결방법

1. 서버가 CORS를 허용하지 않음 
 - API 서버가 CORS 요청을 허용하지 않도록 설정되어 있으면, 브라우저는 이를 차단합니다. 

2. 클라이언트에서 잘못된 요청
 - 프론트엔드 코드에서 CORS 설정을 잘못 구성하거나 헤더를 잘못 추가하는 경우 

3. 프리플라이트 요청 실패
 - 브라우저는 CORS 요청 전에 프리플라이트(preflight) 요청을 보내는데, 이 요청이 실패하면 본 요청도 실패하게 됩니다. 

## 서버에서 CORS 허용하기
서버에서 CORS를 허용하도록 설정하는 것이 가장 일반적인 해결방법입니다. 예를 들어, Express.js 서버에서는 다음과 같이 설정할 수 있습니다.

```javascript
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors());

app.get('/data', (req, res) => {
  res.json({ message: 'Hello, world!' });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```
## 클라이언트에서 프록시 설정하기
개발 환경에서 프록시를 설정하여 CORS 문제를 우회할 수 있습니다.  React에서는 package.json에 프록시 설정을 추가할 수 있습니다.

```json
{
  "proxy": "http://localhost:3000"
}
```

## 프리플라이트 요청에 대응하기
프리플라이트 요청에 서버가 적절히 응답하도록 설정해야 합니다. 예를 들어, 특정 헤더를 허용하도록 설정할 수 있습니다.

```javascript
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  next();
});
```

# 프론트엔드 개발자가 취해야 할 자세
CORS 에러는 보안과 관련된 문제이기 때문에 신중하게 다뤄야 합니다. 그럼 우리는 어떤 자세로 개발을 해야할까요?

- 문제의 원인 이해하기<br>
CORS 에러가 발생하는 이유와 이를 해결하기 위한 기본 원리를 이해해야 합니다. 단순히 에러를 피하기 위한 방법에 안도하지 말고 근본적인 원인을 알아보고 이를 예방하고, 해결합시다.

- 백엔드와 협업하기<br>
백엔드 개발자와 협력하여 CORS 설정을 조정하는 것이 필요합니다. 특히, 프로덕션 환경에서는 보안을 해치지 않으면서도 필요한 요청을 허용하도록 설정해야 합니다.

- 문서화와 학습<br>
CORS와 관련된 문제와 해결 방법을 문서화하고, 팀원들과 공유하는 것이 중요합니다. 또한, 새로운 보안 이슈나 CORS 관련 변경사항에 대해 지속적으로 학습해야 합니다.

CORS 에러는 개발자라면 누구나 한 번쯤 겪게 되는 문제입니다. 하지만, 올바른 이해와 접근법을 통해 충분히 예방하고, 해결할 수 있습니다. 오늘 소개한 내용을 바탕으로 여러분의 프로젝트에서도 CORS 문제를 현명하게 해결해보세요.
