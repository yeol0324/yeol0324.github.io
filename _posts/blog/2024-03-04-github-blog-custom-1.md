---
layout: post
title: "jekyll github blog 커스텀하기 [1]"
summary: 태그 모음 추가하기
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



## 모든 블로그 게시물 파일은 일반적으로 레이아웃 이나 기타 메타데이터를 설정하는 데 사용되는 머리말 로 시작해야 합니다 . 간단한 예에서는 비어 있을 수 있습니다.

layout: post
title: "Welcome to Jekyll!"

---

<h1>Tag Cloud</h1>
'{% raw %}{% assign tags = site.tags | sort %} {% for tag in tags %}
``` html
<span class="site-tag">
  <a href="/tag/{{ tag | first | slugify }}/">
    '{{ tag[0] }}' ('{{ tag | last | size }}')
  </a>
</span>
```
{% endfor %}{% endraw %}' 나는 동글동글한 태그가 필요하고, 태그를 누르면
카테고리 페이지에 해당 태그의 글 목록을 보여주고 싶다! -카테고리 추가하기
<!-- \_config.yml file by using this line permalink: /:categories/:title/ 를 추가하여
줍니다 -default.html -->
<!-- <div class="wrapper"> -->
{%- include sidebar.html -%} — navigation 추가 '{{ content }}' '{% raw %}{{ page.title }}{% endraw %}'
<!-- </div> -->

-_layout.scss 
````css 
.site-sidebar { float: left; line-height:
$base-line-height _ $base-font-size _ 2.25; background: #eeeeee; } -minima.scss
line:24 // Width of the content area $content-width: 1200px
!default;-\_base.scss body { grid-template-areas: "sidebar header header"
"sidebar main main " "sidebar main main " "sidebar footer footer";
grid-template-rows: 200px 1fr 500px; grid-template-columns: 300px 2fr 1fr; }
.site-header { grid-area: header; } .site-sidebar { grid-area: sidebar; }
.site-footer { grid-area: footer; } .page-content { grid-area: main; } ```
````
