---
layout: post
title: Jjekyll LiveReload 자동새로고침
date: 2024-03-02 10:06:52 +0900
categories: etc
tags: jekyll
---

jekyll을 사용해서 github 블로그를 작성할 때 저장 후 브라우저에서 새로고침을 해야반영이 됩니다. 핫리로드에 적응되어 있는 저는 가끔 왜 적용 안 됐지! 할 때도 있는데요, Jekyll 3.7.0 부터 수정사항이 생기면 자동으로 새로고침을 새주는 LiveReload 기능이 생겼습니다.

적용 방법은 아주 간단합니다.

빌드시 
```
jekyll serve --livereload
```
또는
```
bundle exec jekyll serve --livereload
```
<br>
<br>
<br>

---
참고
- <https://jekyllrb.com/news/2018/01/02/jekyll-3-7-0-released/>