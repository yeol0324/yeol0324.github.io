---
layout: post
title: TypeScript 타입 추론 타입 단언 Assertions
summary: 
date: 2024-05-10 16:18:00 +09:00
categories: javascript
tags: 
---

# 뭘 써야 좋을까?
개발할 당시에는 당연히 객체가 있고 null이 아니라고 가정하고 개발을 하지만 100% 모든 상황을 예측하고 개발하기는 어렵습니다. 그래서 저는 저는 대부분 if문, ||, ?? 을 사용해줍니다. <code>||</code><code>??</code> 는 예외처리도 습관적으로 하게 되어서 실제 운영되는 상황에서 큰 문제가 발생하지 않는 것 같아서 선호합니다. 특히 next 같은 경우에 흰 화면에 떡하니 " Application error: a client-side exception has occurred (see the browser console for more information)" 라고 나온다든가 누가봐도 에러가 발생한 화면처럼 나옵니다. 사용자 입장에서는 엄청나게 당황스러운 일이 아닐 수 없어요. 특히 !(타입 단언)을 사용하게되면 자주 발생하는 에러 화면입니다. 무조건 있을 거라고 생각을 했는데 없을 경우가 정말 많이 생긴다고요. 🥲 타입 단언은 html 요소에 접근할 때 같은 정말로 해당하는 object가 무조건 있을 수밖에 없을 때만 사용합니다. 