---
layout: post
title: 자바스크립트 웹뷰 화면 꺼짐 감지
summary: 자바스크립트 페이지 가시성 API
date: 2024-05-13 11:30:23 +09:00
categories: javascript
tags: javascript webview
---


# visibilitychange 이벤트
Document.visibilityState 는 문서의 가시성을 반환합니다. 유저에게 보일 수 있는 상황이면 'visible', 아니면 'hidden' 값이 반환이 되고 속성의 값이 변경되면 visibilitychange이벤트가 실행이 됩니다. 이 속성을 사용해서 웹뷰의 화면 꺼짐을 확인할 수 있습니다.
```javascript
document.addEventListener("visibilitychange", () => {
    if(document.visibilityState == 'hidden'){
        // 화면 off
    }else{
        // 화면 on
    }
});
```