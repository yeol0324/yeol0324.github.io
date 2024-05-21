---
layout: post
title: github pages 리액트 호스팅 에러 해결
summary: 
date: 2024-05-21 11:29:30 +09:00
categories: error
tags: error github react
---

github pages 호스팅 서비스를 이용하려고 했는데, 리액트로 만든 프로젝트를 배포하면 화면이 렌더링되지 않고 흰 화면만 보여지는 문제가 있었습니다. Html 을 열어보면 자바스크립트가 활성화 되야된다고 떠서 한참 찾았는데......
```html
<noscript>You need to enable JavaScript to run this app.</noscript>
```

react-router-dom 때문에 발생하는 문제였습니다.

index.html 에서 BrowserRouter 에 basename을 추가해줍니다! 절대로 ❗️ 전체 경로가 아닌 앞에 있는 경로만 적어주시면 됩니다. 전체 경로를 적어주어서 저는 한참 헤맸어요. 😅

```html
<!-- https://yeol0324.github.io/Interactive-UX/ 인 경우 -->
<BrowserRouter basename="Interactive-UX">
```