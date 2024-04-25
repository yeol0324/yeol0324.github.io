---
layout: post
title: "jekyll github blog 커스텀하기 [2]"
summary: post에 toc 추가하기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

TOC(Table Of Content)를 github blog 에 추가하겠습니다. TOC는 markdown 에서 헤딩 태그를 기준으로 생성이 되는 목차 입니다. 

[jekyll-toc](https://github.com/allejo/jekyll-toc)를 사용해서 블로그에 TOC를 추가해주겠습니다.

# TOC html 적용

먼저 toc html을 다운로드 해줍니다. [다운로드](https://github.com/allejo/jekyll-toc/releases/download/v1.1.0/toc.html)

다운로드 한 html을 프로젝트의 _includes 폴더에 넣어 줍니다.

# post에 TOC 렌더링하기

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
# Style 적용하기

```scss
.post-toc {
  width: 200px;
  margin-left: 800px;
  border-left: 4px solid $point-color;
  position: fixed;
  top: 80px;
  ul {
    margin: 0;
    padding: 10px;
    ul {
      padding: 0 15px;
      font-size: 0.9em;
    }
  }
  * {
    list-style: none;
  }
  @include media-query($on-wide) {
    display: none;
  }
}
```

참고 https://github.com/toshimaru/jekyll-toc