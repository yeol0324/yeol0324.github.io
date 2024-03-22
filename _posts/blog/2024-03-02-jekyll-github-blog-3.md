---
layout: post
title: "github blog 만들기 - 1 블로그 커스텀하기 (1)"
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

-태그 모음 추가하기
https://superdevresources.com/tag-cloud-jekyll/

먼저 포스트에 cateogries

---

layout: post
title: 태그 모음 추가하기
categories: developer-tools
tags: jekyll

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
<!-- :TODO: 컨텐츠로 인식하지 않게 하는 법 찾기... -->
<!-- </div> -->

````css -_layout.scss .site-sidebar { float: left; line-height:
$base-line-height _ $base-font-size _ 2.25; background: #eeeeee; } -minima.scss
line:24 // Width of the content area $content-width: 1200px
!default;-\_base.scss body { grid-template-areas: "sidebar header header"
"sidebar main main " "sidebar main main " "sidebar footer footer";
grid-template-rows: 200px 1fr 500px; grid-template-columns: 300px 2fr 1fr; }
.site-header { grid-area: header; } .site-sidebar { grid-area: sidebar; }
.site-footer { grid-area: footer; } .page-content { grid-area: main; } ```
````
