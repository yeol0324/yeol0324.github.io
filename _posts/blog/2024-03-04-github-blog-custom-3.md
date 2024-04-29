---
layout: post
title: "jekyll github blog 커스텀하기 [3]"
summary: post에 toc, sidebar 추가하기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

아직은 허전한 github blog에 목차와, sidebar 를 추가하겠습니다.

# TOC

TOC 는 markdown 에서 헤딩 태그를 기준으로 생성이 되는 목차 입니다. 원하는 목차로 갈 수 있도록 하는 기능인데요 저는 항상 오른쪽에 떠있게 두겠습니다.

[jekyll-toc](https://github.com/allejo/jekyll-toc)를 사용해서 블로그에 TOC를 추가해주겠습니다.

## toc 적용

먼저 toc html을 다운로드 해줍니다. [다운로드](https://github.com/allejo/jekyll-toc/releases/download/v1.1.0/toc.html)

다운로드 한 html을 프로젝트의 _includes 폴더에 넣어 줍니다.

## post에 toc 렌더링하기

저는 post 페이지에서만 toc 가 필요합니다. 그래서 post.html 에 추가를 할 건데요, 모든 페이지에서 toc 가 나오게 하기 위해서는 default.html 에 추가해 주시면 됩니다.
{% raw %}
```
<div class="post-content e-content" itemprop="articleBody">
  {{ content }}
</div>
<div class="post-toc e-content" itemprop="articleBody">
  {% include toc.html html=content %}
</div>
```
{% endraw %}
<br><br>
> ![](/assets/images/2024-03-04-github-blog-custom-2/01.png)
짠✨

content 하단에 toc 를 추가해주었더니 포스트 아래에 toc가 나왔습니다. 이제 css만 적용해주면 끝 ❗️
## toc✨ style

```scss
.post-toc {
  width: 200px;
  margin-right: -300px;
  border-left: 4px solid #fee86f;
  position: sticky;
  float: right;
  clear: both;
  margin-top: 200px;
  top: 100px;
  a {
    color: $light-text-color;
  }
  ul {
    margin: 0;
    padding: 0 10px;
    li {
      padding: 4px;
    }
    ul {
      padding: 0 15px;
      font-size: 0.9em;
    }
  }
  * {
    list-style: none;
  }
  @include media-query($on-layout) {
    display: none;
  }
}
```


# Side Bar

sidebar 는 저의 프로필이나 카테고리 등을 나타내어 한눈에 볼 수 있도록 만들어 두려고 합니다. 오른쪽에는 toc를 배치해두었으니 sidebar 는 오른쪽에 배치를 하겠습니다.

## sidebar 추가하기

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
      <li><a href="{{base_path}}/categories/?category={{category_name}}">{{ category_name }}</a></li>
      {% endfor %}
    </ul>
  </div>
  <div class="tag-wrap">
    <h2>TAGS</h2>
    <ul>
      {% for tag in site.tags %}
      {% capture tag_name %}{{tag|first|slugize}}{% endcapture %}
      <li>
        <a href="{{base_path}}/categories/?tag={{tag_name}}">
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

마지막으로 카테고리나 태그를 누르면 해당 포스트 리스트를 바로 열어주기 위해서 파라미터를 추가해주었습니다. 이전 글에서 만들었던 categories.html 에 기능을 추가해주었습니다.
```javascript
// categories.html

const checkParam = ()=>{
  const url = new URL(window.location.href)
  const urlParams = url.searchParams
  if (urlParams.size !== 1) return false
  if(urlParams.get('category')) showList('category', urlParams.get('category'))
  if(urlParams.get('tag')) showList('tag', urlParams.get('tag'))
}
checkParam()
```

## sidebar✨ style

```scss
.site-sidebar {
  width: 200px;
  top: 100px;
  margin-left: -300px;
  position: fixed;
  border-right: 2px solid #eee;
  a {
    color: $light-text-color;
  }
  .profile-wrap {
    @include column-flexbox(center, center);

    .profile-img {
      width: 100px;
      height: 100px;
      border: inset $point-color 6px;
      border-radius: 100%;
      overflow: hidden;
      pointer-events: none;
      img {
        height: 100%;
        max-width: none;
        margin-left: -10%;
      }
    }
  }
  .category-wrap {
    margin-top: 20px;
  }
  .tag-wrap {
    margin-top: 20px;
    ul {
      @include flexbox(start, center);
      flex-wrap: wrap;
      margin: 0;
      li {
        list-style: none;
        border: 1px solid #ddd;
        border-radius: 50px;
        padding: 0px 10px;
        margin: 2px;
      }
    }
  }
  @include media-query($on-layout) {
    position: sticky;
    top: 0;
    margin-left: 0;
    display: flex;
    background: #fff;
    width: 100%;
    border-right: none;
    border-bottom: 2px solid #eee;
    .profile-wrap {
      .profile-img {
        width: 60px;
        height: 60px;
        border: inset #fee86f 2px;
      }
      h1 {
        display: none;
      }
    }
  }
}
```

---

참고
- <https://github.com/toshimaru/jekyll-toc>
- <https://jekyllrb-ko.github.io/docs/structure/>