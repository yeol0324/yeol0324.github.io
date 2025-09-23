---
layout: post
title: "presignedUrl cors 에러 해결"
summary: 내가 겪은 s3 관련 오류 모음
date: 2024-05-12 10:06:52 +0900
categories: development
tags: s3 cors presignedUrl
---

# s3 버킷명 확인하기
```error
Failed to load: resource: net::ERR_CERT_COMMON_NAME_INVALID
```
버킷 이름에 .이 들어가면 해당 오류가 발생합니다. postman으로도 테스트가 잘 되었는데 브라우저에서 안 되었습니다. [버킷명 규칙](https://docs.aws.amazon.com/ko_kr/AmazonS3/latest/userguide/bucketnamingrules.html)을 잘 따라서 생성해줍니다.

**소문자, 숫자, 점(.) 및 하이픈(-)만 포함해야 합니다**

# CORS 정책 업데이트

AWS bucket CORS 정책을 확인해 줍니다. 발급받은 presignedUrl Put Method를 사용해서 파일을 업로드 하는데 CORS 정책을 추가해주어야합니다. 권한이 필요한 도메인을 AllowedOrigins 에 추가, 필요한 메쏘드들은 AllowedMethods에 추가해줍니다.
```info
버킷 > 권한 > CORS(Corss-origin 리소스 공유)
```
![CORS추가.png](/assets/images/2024-03-02-s3-error/01.png)