---
layout: post
title: "jekyll github blog 커스텀하기 [2]"
summary: post에 toc 추가하기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

TOC(Table Of Content)를 github blog 에 추가하겠습니다. TOC는 markdown 에서 헤딩 태그를 기준으로 생성이 되는 목차 입니다. 

markdown 에서는 toc 가 생겼겠지만 포스트 페이지에 렌더링이 되지 않습니다. <code>jekyll-toc</code> 라는 플러그인을 사용하여 toc 기능을 사용해 보겠습니다.

# 플러그인 추가하기

프로젝트 안에 있는 Gemfile에 명령어를 추가합니다.
```
gem 'jekyll-toc' 
```

터미널에서 명령어를 입력해 Gemfile 을 실행합니다.
```
bundle install
```
_config.yml 사이트의 섹션 에 jekyll-toc을 추가
```
plugins:
  - jekyll-toc
```

# TOC 설정하기
이제 toc 사용 설정을 해 주면 화면에서 toc가 렌더링 된 것을 확인해볼 수 있습니다.

## post(.md)마다 설정하기

md 를 작성할 때 항상 위에 페이지 정보를 써 줘야 하죠? 정보를 쓰는 곳에 toc : true 설정을 해 주면 됩니다.
그럼 해당 페이지나 게시물에서 toc 가 생긴 것을 볼 수 있습니다.
```markdown
---
layout: post
title: "Welcome to Jekyll!"
toc: true
---
```

## default 설정하기
포스트마다 사용함으로 설정하기는 귀찮고 나는 항상 떠 있으면 좋겠다! 하면 기본으로 사용함 설정을 해줄 수도 있습니다. default 설정은 _config.yml 에서 할 수 있습니다.

```yml
# the internal "default list".

defaults:

- scope:
  path: ""
  values:
  toc: true
```

# 화면에 렌더링 하기
저는 post 페이지에서만 toc 가 필요합니다. 그래서 post.html 에 추가를 할 거예요. 모든 페이지에서 toc 가 나오게 하기 위해서는 default.html 에 추가해 주시면 됩니다. {% raw %} {{ content | toc }} 로 content 에 toc 를 포함을 해주면 되는데요, toc 와 content 를 분리하고 싶다면 <code>{% toc %}</code> 태그 또는 <code>toc_only</code> filter 를 사용하면 됩니다.

```
_예시
<div>{{ content | toc }}</div>
<div>{{ content | toc_only }}</div>
<div>{% toc %}</div>

_layouts/post.html
  <div class="post-content e-content" itemprop="articleBody">
    {{ content }}
  </div>
  <div class="post-toc e-content" itemprop="articleBody">
    {% toc %}
  </div>
```
{% endraw %}

content 와 따로 표시되었으면 해서 post.html 에 content요소 아래에 배치를 하고 css 까지 적용시켰습니다.
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
  @include media-query(1600px) {
    display: none;
  }
}
```

참고 https://github.com/toshimaru/jekyll-toc
