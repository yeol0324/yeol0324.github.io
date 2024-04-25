---
layout: post
title: "블로그 글 공개/비공개 설정"
summary: Github pages blog 글 비공개 설정
date: 2024-04-24 10:06:52 +0900
categories: blog
tags: github-page
---

Github pages blog 글을 작성하다보면 한번에 끝내기 어려운 경우도 종종 있습니다. 그래서 아직 공개가 되지 않았으면 해서 제외하고 커밋을 하곤 했었는데 각각 비공개 설정이 있었습니다.

# Github pages blog 비공개 설정
<span class="h-yellow">published: true</span> : 공개<br>
<span class="h-yellow">published: false</span> : 비공개<br>
각 포스트 상단에 포스트 정보 적는 곳에 추가를 해주면 됩니다!
```
---
layout: post
title: "블로그 글 공개/비공개 설정"
summary: Github pages blog 글 비공개 설정
date: 2024-04-24 10:06:52 +0900
categories: blog
tags: github-page
published: false << 비공개 설정
---
```

default 로 published : true 로  되어있기 때문에 비공개를 하고 싶은 글에만 published : false 설정을 하면 됩니다.