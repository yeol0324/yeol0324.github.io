---
layout: post
title: "jekyll 문법 표현하기"
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

jekyll 문법을

```
{{"{% raw"}} %} {{"{{ "}} }} {{"{% endraw"}} %}
```

`{% raw %}` 과 `{% endraw %}`로 감싸주기!

예외 처리가 되어 실행되지 않게 작성할 수 있습니다!.

jekyll github blog는에 마크다운(markdown) 으로 글을 씁니다.
예시를 작성하기 위해 {% raw %}{{ }}{% endraw %} 과 {% raw %}{% %}{% endraw %}를 사용하게 되는데 그대로 작성하면 jekyll에서 이를 읽고 예시를 실행하려고 해서 원하는 대로 결과물이 나오지 않습니다.

html 주석은 텍스트가 아예 나오지 않습니다.

```html
<!-- {% raw %}{{page.title}}{% endraw %} -->
```

사용하게되면
적용

{% raw %}{{page.title}}{% endraw %}

```

```
