---
layout: post
title: "sitemap 등록 실패 오류 해결"
summary: 검색엔진에 등록하는 sitemap.xml 작성시 오류
date: 2024-03-02 10:06:52 +0900
categories: etc
tags: jekyll markdown
---

sitemap 오류 해결하기

```error
This page contains the following errors:
error on line 2 at column 1: Start tag expected, '<' not found
Below is a rendering of the page up to the first error.
```

# urlset 형식 추가

xml 을 아무리 작성해도 자꾸 위의 오류가 발생했습니다.

<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

urlset 태그에 xmlns:xsi, xsi:schemaLocation를 추가하여 유효성 검사기에 형식을 알려주어 해결!

# 포스트 title, url 확인

포스트의 제목이나 경로에 & 가 포함되면 파싱하다가 에러가 발생합니다. 제목이나 경로에서는 & 를 사용하지 않기!


참고
- <https://www.sitemaps.org/protocol.html#validating>