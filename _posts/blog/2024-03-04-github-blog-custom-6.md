---
layout: post
title: "jekyll github blog 커스텀하기 [6]"
summary: 블로그 꾸미기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

블로그에 home 레이아웃을 수정하고 aside 추가하는 작업을 해보겠습니다.

minia default 테마의 home 화면은 포스팅이 최신 날짜 순으로 제목이 쭉 나열이 되어있는 곳을 먼저 바꿔보겠습니다.
제목만 나왔을 떄는 너무 허전한 느낌이라서 제목 아래에 컨텐츠 내용이 조금 보이고 아래 태그들이 달려있는 형식으로 잡았습니다.

결과물 

먼저 home.html 에서 post-list 안에 날짜 별로 묶여있는 부분을 지워주고 content와 태그들을 추가해주었습니다.
```html
{% raw %}
--- 제거
{%- assign date_format = site.minima.date_format | default: "%b %-d, %Y" -%}
<span class="post-meta">{{ post.date | date: date_format }}</span>
--- 추가
<li>
    <a class="post-link" href="{{ post.url | relative_url }}">
        <h3>
            {{ post.title | escape }}
        <div class="post-content">
            <p>
            {{post.content| markdownify | strip_html | truncate: 280 | escape }}
            </p>
        </div>
        <div class="tag-list">
        {%- for tag in post.tags -%}
            <h5>
            #{{ tag }}
            </h5>
        {%- endfor -%}
        </div>
        </h3>
        {%- if site.show_excerpts -%}
        {{ post.excerpt }}
        {%- endif -%}
    </a>
</li>
{% endraw %}
```

포스트의 컨텐츠가 렌더링 된 곳을 간단한 설명을 해보자면
{% raw %}
{{
post.content | markdownify | strip_html | truncate: 280 | escape 
}}
{% endraw %}
<code>markdownify</code> Markdown 형식의 문자열을 HTML로 변환합니다. <br>
<code>strip_html</code> 문자열에서 HTML 태그를 제거합니다.<br>
<code>truncate</code> 인수로 전달된 문자 수만큼 문자열을 줄입니다.

css 도 수정해줍니다. _layout.scss 최하단에 작성하였습니다.
```scss
/**
 * Home Layout
 */

.post-list {
  margin-left: 0;
  list-style: none;
  > li {
    border-bottom: 1px solid #ddd;
    a {
      color: $text-color;
      padding: 20px;
      h3 {
        display: inline-block;
        margin-bottom: 4px;
        background-color: #fff;
        line-height: 18px;
        transition: 0.4s;
      }
      &:hover {
        h3 {
          background-color: #fee86f;
        }
        text-decoration: none;
      }
    }
    .post-content {
      margin: 0;
      font-size: 16px;
      p {
        margin: 0;
        padding: 4px 8px;
      }
    }
    .tag-list {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      h5 {
        font-size: 12px;
      }
    }
  }
}
```