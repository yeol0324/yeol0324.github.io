---
layout: post
title: "github blog posting 하기"
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page markdown
---

블로그 생성, 커스텀 포스트를 먼저 쓰고 싶었는데, 설명글을 쓰다보니 markdown으로 표현하기 어려운 점들이 있었습니다. 그래서 markdown을 먼저 공부해 보고, markdown으로 글 쓰기! 와 팁! 들을 먼저 소개하겠습니다.

시작하기에 앞서, 마크다운에 대해 먼저 알아보겠습니다.

> ### What is Markdown?
>
> Markdown is a lightweight markup language that you can use to add formatting elements to plaintext text documents. Created by John Gruber in 2004, Markdown is now one of the world’s most popular markup languages.
>
> 마크다운은 일반 텍스트 텍스트 문서에 서식 요소를 추가하는 데 사용할 수 있는 경량 마크업 언어입니다. 2004년 John Gruber 가 만든 Markdown은 현재 세계에서 가장 인기 있는 마크업 언어 중 하나입니다.

markdown 의 특징

- 일반 텍스트를 입력할 수 있다.
- html 태그를 사용할 수 있다

공식 문서에 나와 있는 설명입니다. 일반적으로 깃 레파지토리에서 프로젝트 설명을 적을 때 많이 사용을 해보셨을 겁니다. 깃헙에서 레파지토리를 신규로 생성할 때도 readme.md 를 자동으로 생성할 수도 있습니다.
그래서 마크다운에도 몇가지 규칙이 있습니다.

---

웹사이트
Markdown은 웹용으로 설계되었으므로 웹 사이트 콘텐츠 생성을 위해 특별히 설계된 응용 프로그램이 많이 있다는 것은 놀라운 일이 아닙니다.

Markdown 파일을 사용하여 웹사이트를 만드는 가장 간단한 방법을 찾고 있다면 blot.im을 확인하세요 . Blot에 가입하면 컴퓨터에 Dropbox 폴더가 생성됩니다. Markdown 파일을 폴더에 끌어서 놓기만 하면 됩니다. — 귀하의 웹사이트에 있습니다. 이보다 더 쉬울 수는 없습니다.

HTML, CSS 및 버전 제어에 익숙하다면 Markdown 파일을 가져와 HTML 웹사이트를 구축하는 인기 있는 정적 사이트 생성기인 Jekyll을 확인해 보세요. 이 접근 방식의 한 가지 장점은 GitHub 페이지가 Jekyll로 생성된 웹사이트에 대한 무료 호스팅을 제공한다는 것입니다 . Jekyll이 마음에 들지 않는다면, 사용 가능한 다른 많은 정적 사이트 생성기 중 하나를 선택하세요 .

제일 찾고 싶었던 것은 커스텀을 할 때 jekyll의 문법을 자주 사용해야해서 '{% raw %}{{ page.title }}{% endraw %}' 와 같은 설명을 적고 싶었는데 코드 블럭에 넣어도, 인용에 넣어도 계속 변수로 인식하는 문제였습니다.

```
{{page.title}}
```

> {{page.title}}

{{page.title}}

> Jekyll 은 에셋 파일의 모든 Liquid 필터와 태그를 처리합니다
> 만약 Mustache 를 사용하거나 Liquid 템플릿 문법과 충돌하는 다른 JavaScript 템플릿 언어를 사용하고 있다면, 해당 코드 앞뒤에 {% raw %} 와 {% endraw %} 태그를 사용해야 합니다.

jekyll 사이트에 검색도 없어서 한참 찾았습니다 . . .

---

참고
- <https://www.markdownguide.org/>
- <https://jekyllrb.com/>
