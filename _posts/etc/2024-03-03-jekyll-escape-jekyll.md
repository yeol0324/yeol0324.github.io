---
layout: post
title: "jekyll 문법 표현하기"
date: 2024-03-02 10:06:52 +0900
categories: etc
tags: jekyll markdown
---

jekyll github blog는에 마크다운(markdown) 으로 글을 씁니다. jekyll 문법 탈출하는 방법을 정리해봤습니다.


블로그에서 예시를 작성하기 위해 {% raw %}{{ }}{% endraw %} 또는 {% raw %}{% %}{% endraw %}를 사용할 일이 많습니다. 이걸 그대로 작성하면 jekyll에서 이를 읽고 예시를 실행하려고 해서 원하는 대로 결과물이 나오지 않습니다. 코드블록을 '<code>{&#37; raw &#37;}</code>' '<code>{&#37; endraw &#37;}</code>` 로 감싸게 되면 예외 처리가 되어 실행되지 않게 작성할 수 있습니다!.


{&#37; raw &#37;}
```
코드 작성
```
{&#37; endraw &#37;}

html 주석은 텍스트가 아예 나오지 않습니다.

```html
<!-- {% raw %}{{page.title}}{% endraw %} -->
```

raw 로 감싸서 표현을 하게 되면

```
{% raw %}{{page.title}}{% endraw %}
```
짜잔 ✨


이 글을 쓰는 도중에도 {&#37; raw &#37;} 라고 글을 쓰고 싶었는데, 그냥 작성을 하니 이번엔 또 jekyll 에서 예외처리코드로 인식하는 것 같았습니다. jekyll 을 사용해서 구축 된 jekyll 의 블로그 github 에 들어가서 예시를 찾아왔습니다.

```text
<code>{&#37; raw &#37;}</code>
```

이처럼 유니코드를 사용하여 표현을 할 수 있습니다.

markdown 사용법만 익히면 쉽게 작성할 수 있을 것이라고 생각했었는데, jekyll 문법도 잘 활용해야 원하는 것들을 다 표현할 수 있는 것 같습니다.


사실 뭐라고 검색을 해야될지 감이 안 와서 찾는데 정말 오래 걸렸는데 결국은 공식 문서에서 찾게 되었습니다. 다시한번 다짐하는 공식 문서를 열심히 살펴보자... 

앞으로 공부할 게 한참이다 :0

---
참고
- <https://jekyllrb.com/docs/liquid/tags/>
- <https://jekyllrb.com/>
