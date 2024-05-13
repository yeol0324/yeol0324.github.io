---
layout: post
title: 웹뷰 동영상 재생 오류 해결
summary: 
date: 2024-05-13 10:40:04 +09:00
categories: web
tags: webview android
---

# Manifest 파일 확인
```java
<activity android:name="MainActivity" android:hardwareAccelerated="true">
```
가용가능한 리소스가 부족해서 재생이 안될수있다.

# webview 설정
```java
settings.mediaPlaybackRequiresUserGesture = false
```

웹에서 테스트할 때는 잘 재생되던 동영상들이 태블릿의 앱으로 열면 재생이 안 되는 일이 있었습니다. 웹으로 한참 디버깅 했는데 앱에서 설정이 필요했었어요.

<span class="h-yellow">🌳 나무를 보지 말고 숲을 보자 🌳</span>