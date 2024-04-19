---
layout: post
title: "jekyll github blog 커스텀하기 [5]"
summary: 페이지 추가하기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

처음에 테마를 다운 받고 about 페이지가 있었는데요, 저한테 필요한 카테고리 페이지를 추가해보겠습니다.
프로젝트 최상단에 index.markdown about.markdown 이 있을 겁니다. 최상단에 만드는 게 페이지가 되는 구조입니다.
md, html 모두 가능합니다.
저는 categories.html 로 만들어주었어요.

---
layout: page
permalink: /categories/
title: Category
---

최상단에 이렇게 써줄 거예요!
하나씩 살펴보면
layout : page 라는 레이아웃을 가짐
permalink :  baseUrl/categories/ 를 접속 하면 나오는 페이지
title : 해당 페이지 타이틀 ( 페이지에 접속하면 상단 탭에 표시되는 이름 ) 입니다
