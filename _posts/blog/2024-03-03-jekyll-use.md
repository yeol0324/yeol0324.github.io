---
layout: post
title: "jekyll 문법 사용하기"
date: 2024-03-02 10:06:52 +0900
categories: jekyll
tags: jekyll blog github-page
---
{% raw %} {{content}} , {{page}} 등의 변수를 사용하여 페이지나 포스트의 렌더링 된 컨텐츠를 나타낼 수 있습니다. jekyll layout 에는 상속이라는 개념도 있습니다. 이미 존재하는 레이아웃에 추가해서 일부 페이지에만 적용할 때 사용합니다. 예를들면 post 페이지에서 항상 최상단에 제목과 카테고리가 표시되는 형식을 만들 수 있습니다.
_layouts/post.html 에 다음과 같이 작성 후 사용할 수 있습니다.
```
---
layout: default
---
<header class="post-header">
{{page.categories}}
    <h1 class="post-title p-name" itemprop="name headline">
        {{ page.title | escape }}
    </h1>
</header>
<div>
    {{ content }}
</div>
```
{% endraw %}

react 나 vue 같은 프레임워크를 사용하면 컴포넌트를 만들어서 추가할 수 있는 것처럼 Jekyll 프로젝트에서도 가능합니다.

https://jekyllrb-ko.github.io/docs/structure/
https://jekyllrb-ko.github.io/docs/layouts/
https://jekyllrb.com/docs/includes/