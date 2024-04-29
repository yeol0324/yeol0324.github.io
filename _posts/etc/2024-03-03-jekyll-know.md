---
layout: post
title: "jekyll 알아보기"
date: 2024-03-02 10:06:52 +0900
categories: etc
tags: jekyll
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

https://jekyllrb.com/docs/includes/
매개변수 변수를 포함에 전달고유링크
포함에 전달하려는 매개변수가 문자열이 아닌 변수라고 가정합니다. 예를 들어, {{ site.product_name }}실제 하드 코딩된 이름이 아닌 제품의 모든 인스턴스를 참조하기 위해 를 사용할 수 있습니다 . (이 경우 파일에는 제품 이름 값으로 _config.yml호출되는 키가 있습니다 .)product_name

포함 매개변수에 전달하는 문자열에는 중괄호를 포함할 수 없습니다. 예를 들어 다음이 포함된 매개변수를 전달할 수 없습니다."The latest version of {{ site.product_name }} is now available."

포함에 전달하는 매개변수에 이 변수를 포함하려면 포함에 전달하기 전에 전체 매개변수를 변수로 저장해야 합니다. capture태그를 사용하여 변수를 생성 할 수 있습니다 .
capture
포함에 전달하는 매개변수에 이 변수를 포함하려면 포함에 전달하기 전에 전체 매개변수를 변수로 저장해야 합니다. capture태그를 사용하여 변수를 생성 할 수 있습니다 .

https://jekyllrb-ko.github.io/docs/structure/
https://jekyllrb-ko.github.io/docs/layouts/
https://jekyllrb.com/docs/includes/