---
layout: post
title: "jekyll github blog 커스텀하기 - 1"
summary: 레파지토리 만들기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

jekyll github blog 커스텀하기 입니다. 지킬 깃헙 블로그 커스텀하기는 이전에 글을 썼었는데요. 계속 욕심도 생기고 하고 싶은 것들도 생겨서 디자인도 더욱 고도화할 겸 기록을 남겨두려고 합니다.

Pass the --livereload option to serve to automatically refresh the page with each change you make to the source files: bundle exec jekyll serve --livereload

정적인 html 로 이루어져있는 사이트와 같이 /폴더명/파일명 이 곧 주소가 됩니다.
파일은 기본적으로 markdown 을 사용하며 html 도 지원하고 있습니다.
예시
.
├── about.md # => http://example.com/about.html
├── documentation # folder containing pages
│ └── doc1.md # => http://example.com/documentation/doc1.html
├── design # folder containing pages
│ └── draft.md # => http://example.com/design/draft.html

Post 를 사용하려면 다음 파일명 규칙을 지켜야합니다.
YYYY-MM-DD-title.MARKUP
예시
2011-12-31-new-years-eve-is-awesome.md
2012-09-12-how-to-write-a-blog.md

## 모든 블로그 게시물 파일은 일반적으로 레이아웃 이나 기타 메타데이터를 설정하는 데 사용되는 머리말 로 시작해야 합니다 . 간단한 예에서는 비어 있을 수 있습니다.

layout: post
title: "Welcome to Jekyll!"

---
