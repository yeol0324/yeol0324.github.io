---
layout: post
title: "jekyll github blog 커스텀하기 [1]"
summary: 블로그 꾸미기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

jekyll github blog 커스텀하기 입니다. 지킬 깃헙 블로그 생성하기는 이전에 글을 썼었는데요. 계속 욕심도 생기고 하고 싶은 것들도 생겨서 디자인도 더욱 고도화할 겸 기록을 공유합니다.

# 디렉토리 구조

먼저 jekyll 디렉토리 구조에 대해 간단히 알아보겠습니다.
> <a href="{{base_path}}/etc/jekyll-know/">jekyll 자세히 알아보기</a>
{% raw %}
_layouts/

- <code>default.html</code> 화면 템플릿 소스코드를 입력합니다. 
- <code>*.html</code> 에 default.html 레이아웃을 상속받는 페이지 레이아웃을 만들 수 있습니다.

_includes/
- <code>*.html</code> {% include *.html %} 처럼 include 태그를 사용하여 렌더링할 수 있습니다.
{% endraw %}

# HTML/CSS 수정
제 글을 따라왔다면 테마를 따로 설치하지 않고 기본 테마를 사용하고 있을 거예요. jekyll default theme 이름이 minima 테마입니다. 이 테마를 커스터마이징 하기 위해서는 minima 가 제시하는 규약에 따라 작성을 해야합니다.
minima 설치 경로에서 이 구조를 확인할 수 있습니다.

먼저 터미널을 켜줍니다. 프로젝트의 경로로 들어와서 다음과 같이 입력해 줍니다.
```bash
bundle show minima

> /Users/leeyurim/.rbenv/versions/3.3.0/lib/ruby/gems/3.3.0/gems/minima-2.5.1
```
minima 테마가 설치된 경로를 얻었습니다. 이제 해당 경로로 들어가 봅시다.
> 꿀팁 ❗️ MAC finder 에서 cmd + shift + g 하면 경로로 바로 이동할 수 있다!

해당 경로로 접속을 해보면 바로 전에 알아봤던 폴더 구조와 많이 비슷한 것을 확인할 수 있을 거예요.

```bash

├── LICENSE.txt
├── README.md
├── _includes
│   ├── disqus_comments.html
│   ...
│   └── social.html
├── _layouts
│   ├── default.html
│   ├── home.html
│   ├── page.html
│   └── post.html
├── _sass
│   ├── minima
│   │   ├── _base.scss
│   │   ├── _layout.scss
│   │   └── _syntax-highlighting.scss
│   └── minima.scss
└── assets
    ├── main.scss
    └── minima-social-icons.svg

```
각 폴더를 복사해서 제 프로젝트로 가져오겠습니다. 안에 html, scss 를 그대로 두고 커스터마이징하면 쉽게 따라할 수 있습니다. <span class="h-yellow">구조가 바뀌면 적용이 안 되니 그대로 가져오세요!</span>

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
        {{post.content| markdownify | strip_html | truncate: 200 | escape }}
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

포스트의 컨텐츠가 렌더링 된 곳을 보자면, 
{% raw %}{{post.content | markdownify | strip_html | truncate: 200 | escape}}{% endraw %}
- <code>markdownify</code> Markdown 형식의 문자열을 HTML로 변환합니다. <br>
- <code>strip_html</code> 문자열에서 HTML 태그를 제거합니다.<br>
- <code>truncate</code> 인수로 전달된 문자 수만큼 문자열을 줄입니다.

truncate 값을 조절하여 원하는 만큼 바꿔주시면 됩니다.

# home style
_layout 디렉토리 안에 위치한 html 의 style 은 _layout.scss 에 적용되어 있어서, _layout.scss 최하단에 css 를 추가했습니다.
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

# 다른 페이지 추가하기

처음에 테마를 다운 받고 about 페이지가 있었는데요, 저한테 필요한 카테고리 페이지를 추가해보겠습니다.
프로젝트 최상단에 index.markdown about.markdown 이 있는데요 최상단에 만드는 파일을 읽어 페이지가 되는 구조입니다.
작성은 md, html 모두 가능합니다. 저는 categories.html 로 만들어주었어요.
{% raw %}
```html
# categories.html

---
layout: page
permalink: /categories/
title: Category
---

<div id="archives">
  {% for category in site.categories %}
  <div class="archive-group">
    {% capture category_name %}{{ category | first }}{% endcapture %}
    <h1 id="{{category_name}}"class="category-head">{{ category_name }}</h1>
    <!-- <a href="#{{category_name}}" onclick="showTag('#{{category_name}}')">
      {{category_name}} (0)
    </a> -->
    {% for post in site.categories[category_name] %}
    <article class="archive-item">
      <h4><a href="{{ site.baseurl }}{{ post.url }}">{{post.title}}</a></h4>
    </article>
    {% endfor %}
  </div>
  {% endfor %}
</div>
```
상단에 <span class="h-yellow">permalink: /categories/</span> 라고 작성을 했기떄문에 
{{base_path}}/categories/ 로 접속해보면 카테고리 별로 카테고리의 글을 한눈에 확인할 수 있는 페이지가 생겼습니다!
카테고리별이 아닌 태그모음도 추가하고 싶어지는데...

다음은 태그 모음 추가하기로 돌아오겠습니다.
{% endraw %}
<br>
<br>
---
참고
- <https://jekyllrb.com/tutorials/convert-site-to-jekyll/>
- <https://jekyllrb.com/docs/structure/>
- <https://jekyllrb.com/docs/themes/>