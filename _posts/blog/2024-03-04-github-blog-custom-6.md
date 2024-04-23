---
layout: post
title: "jekyll github blog 커스텀하기 [6]"
summary: 블로그 꾸미기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

블로그 home 디자인과 구성을 수정하고 sidebar 까지 추가해보겠습니다.

# 디렉토리 구조

먼저 jekyll 디렉토리 구조에 대해 간단히 알아보겠습니다.
> <a href="{{base_path}}/jekyll/jekyll-use/">jekyll 사용하기</a>
{% raw %}
_layouts/

- <code>default.html</code> 화면 템플릿 소스코드를 입력합니다. 
- <code>*.html</code> 에 default.html 레이아웃을 상속받는 페이지 레이아웃을 만들 수 있습니다.

_includes/
- <code>*.html</code> {% include *.html %} 처럼 include 태그를 사용하여 렌더링할 수 있습니다.
{% endraw %}


# home 구성하기

minia default 테마의 home 화면은 포스팅이 최신 날짜 순으로 제목이 쭉 나열이 되어있는 곳을 먼저 바꿔보겠습니다.
제목만 나왔을 떄는 너무 허전한 느낌이라서 제목 아래에 컨텐츠 내용이 미리보기 형식으로 보이고 아래 태그들이 달려있는 모양으로 구성을 했습니다.

먼저 _layouts/home.html 에서 post-list 안에 날짜 별로 묶여있는 부분을 지워주고 content와 태그들을 추가해주었습니다.
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

_layout.scss 최하단에 css 를 추가했습니다.
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
        color: #808080;
        margin: 0;
        padding: 4px 10px;
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

# sidebar 추가하기

sidebar는 모든 페이지에서 항상 떠있도록 추가할 거예요. 블로그에서 그 글을 보다보면 어떤 카테고리들이 있는지 쭉 보고 싶었던 적이 많았던 것 같습니다. 카테고리 상세 페이지를 가게 되면 이전에 보던 글을 다시 찾기 어려웠던 기억이 있어서 저는 sidebar 에서 블로그에 카테고리를 쭉 보여주고, 그 아래에는 tag들을 볼 수 있도록 만들겠습니다.

_includes 디렉토리 안에 sidebar.html 을 생성해 주고, 전체 페이지에서 보이도록 하기 위해 default.html 에서 header 아래에 배치했습니다.

{% raw %}
```html
<!-- default.html -->
 <body>
   {%- include header.html -%}
    {%- include sidebar.html -%} // 추가
    <main class="page-content" aria-label="Content">
      <div class="wrapper">
        {{ content }}
      </div>
    </main>
    {%- include footer.html -%}
  </body>
<!-- sidebar.html -->
<sidebar class="site-sidebar">
  <div class="profile-wrap">
    <div class="profile-img">
      <img src="/assets/profile.png" alt="">
    </div>
    <h1><a rel="author" href="{{ "/" | relative_url }}">{{ site.title | escape }}</a></h1>
  </div>
  <div class="category-wrap">
    <h2>CATEGORIES</h2>
    <ul>
    {% for category in site.categories %}
      {% capture category_name %}{{ category | first }}{% endcapture %}
      <li><a href="{{base_path}}/categories/#{{category_name}}">{{ category_name }}</a></li>
      {% endfor %}
    </ul>
  </div>
  <div class="tag-wrap">
    <h2>TAGS</h2>
    <ul>
      {% for tag in site.tags %}
      {% capture tag_name %}{{tag|first|slugize}}{% endcapture %}
      <li>
        <a href="#{{tag_name}}" onclick="showTag('#{{tag_name}}')">
          {{tag_name}}
        </a>
      </li>
      {% endfor %}
    </ul>
  </div>
</sidebar>
```
{% endraw %}

여기서 사용된 capture 태그를 설명하자면
> 포함에 전달하는 매개변수에 이 변수를 포함하려면 포함에 전달하기 전에 전체 매개변수를 변수로 저장해야 합니다. capture태그를 사용하여 변수를 생성 할 수 있습니다.

for 문에 선언한 변수를 바로 사용할 수 없으므로 capture 태그를 사용하여 변수를 저장해야합니다. 그래서 capture 태그를 사용해서 변수를 저장 후 사용해줬습니다.
https://jekyllrb-ko.github.io/docs/structure/