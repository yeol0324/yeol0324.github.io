---
layout: post
title: url link 공유시 나오는 이미지 추가하기
summary: 오픈그래프프로토콜(OpenGraphProtocol)과 메타태그(MetaTag)
date: 2024-05-09 17:09:06 +09:00
categories: web
tags: web frontend html css
---

지인한테 블로그 글 꽤 많이 썻다고 자랑하기 위해 링크를 딱 보내는 순간 제 프로필에 있는 사진이 대문짝하게 나오는 일이 있었습니다. 지금까지 이걸 신경도 안 쓰고 모르고 있었다니... 저 자신도 링크를 봤을 때 이미지가 이상하거나 소개글이 이상하면 눌러보지도 않으면서 신경쓰지 않은 것이 자존심상했습니다. 핑계 아닌 핑계를 해보자면 최근에 진행한 프로젝트가 계속 웹뷰 작업으로 앱에서 인증을 받고 들어오는 사이트라 url을 보내면 뜨는 사진을 생각도 못하고 있었던 것 같습니다. 사소한 영역이지만 또 사소한 것까지 신경쓰는 세심한 개발자가 되어봅시다.

링크 공유했을 떄 나오는 사진이랑 제목 소개글을 분석하고 바로 뜯어고쳐보겠습니다. 아자자❗️

# 분석해보기 🔍

링크를 전달했을 때 나오는 영역을 살펴봐야겠습니다. 저는 제 블로그로 확인을 해보았는데요. 제 블로그를 공유하면 블로그 이름, description이 나오는 거로 봐서는 html head 태그에 들어가는 메타태그와 관련이 있어보였습니다.
![web thumbnail](/assets/images/20240509/webThumb.png)

# 오픈 그래프 프로토콜

웹사이트나 링크를 공유, 첨부했을 때 메타태그를 볼 수 있는 것은 <span class="h-yellow">Open Graph Data</span>덕분입니다. Facebook이 웹 사이트에 다양한 메타 데이터를 제공하기 위해 발명한 메타 데이터 프로토콜이라고 합니다.



이 외에도 다양한 옵션이 엄청 많았습니다. [공식문서](https://ogp.me/)에서는 다양한 옵션과 속성을 소개하고 있어서 훑어보는 것도 꽤 재미있었습니다.


- <https://ogp.me/>
- <https://developer.mozilla.org/ko/docs/Learn/HTML/Introduction_to_HTML/The_head_metadata_in_HTML>
- [오픈그래프(Open Graph) meta og 태그(tag)와 트위터 카드(Twitter Cards)](https://www.next-t.co.kr/blog/%EA%B2%80%EC%83%89%EC%97%94%EC%A7%84%EC%B5%9C%EC%A0%81%ED%99%94-SEO-%ED%85%8C%ED%81%AC%EB%8B%88%EC%BB%ACSEO-%EC%98%A4%ED%94%88%EA%B7%B8%EB%9E%98%ED%94%84-OpenGraph-metaogtag-%ED%8A%B8%EC%9C%84%ED%84%B0%EC%B9%B4%EB%93%9C-TwitterCards)