---
layout: post
title: "css 동작 방식"
date: 2024-03-04 10:06:52 +0900
categories: web
tags: css
published : false
---

<!-- 우리가 보고 있는 화려한 웹이라든가 보기 좋은 웹은 html 만으로 구현하기는 어렵습니다. css로 색을 입히고, html 의 요소들을 꾸며 더욱 가독성있는 웹을 만들 수 있습니다. css는 단순히 html의 요소를 꾸며서 화면에 렌더링 되는 게 아닙니다. css 동작 방식을 정리해 -->

# css의 작동 원리
브라우저가 문서를 불러올 때 문서의 콘텐츠와 스타일 정보를 결합해서 웹페이지를 로드합니다.

1. HTML 로드
2. HTML을 DOM(Document Object Model) 으로 변환
3. HTML에 연결된 이미지, 동영상, css등 리소스 로드
4. 렌더 트리
5. 렌더 트리는 규칙이 적용된 후에 표시되어야 하는 구조로 배치됩니다.
6. 페이지의 시각적 표시가 화면에 표시됩니다 (이 단계를 페인팅 이라고 합니다).


![css 작동 원리](https://developer.mozilla.org/ko/docs/Learn/CSS/First_steps/How_CSS_works/rendering.svg)




- <https://panython.tistory.com/38>
- <https://developer.mozilla.org/ko/docs/Learn/CSS/First_steps/How_CSS_works>
- <https://medium.com/@ferencalmasi/10-best-practices-for-improving-your-css-84c69aac66e>
