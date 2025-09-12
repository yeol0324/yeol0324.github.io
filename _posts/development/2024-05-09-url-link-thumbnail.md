---
layout: post
title: url link 공유시 나오는 이미지 추가하기
summary: 오픈그래프프로토콜(OpenGraphProtocol)과 메타태그(MetaTag)
date: 2024-05-09 17:09:06 +09:00
categories: development
tags: web frontend html css
---

지인한테 블로그 글 꽤 많이 올렸다고 자랑하기 위해 링크를 띵~ 보내는 순간 제 프로필에 있는 사진이 대문짝하게 나오는 일이 있었습니다. 지금까지 이걸 신경도 안 쓰고 모르고 있었다니... 저 자신도 링크를 봤을 때 이미지가 이상하거나 소개글이 이상하면 눌러보지도 않으면서 신경쓰지 않은 것이 자존심이 상했습니다. 핑계 아닌 핑계를 해보자면 최근에 진행한 프로젝트가 계속 웹뷰 작업으로 앱에서 인증을 받고 들어오는 사이트라 url을 보내면 뜨는 사진을 생각도 못하고 있었던 것 같습니다. 사소한 영역이지만 또 사소한 것까지 신경쓰는 세심한 개발자가 되어봅시다.

링크 공유했을 때 나오는 사진이랑 제목 소개글을 분석하고 바로 뜯어고쳐보겠습니다. 아자자❗️

# 분석해보기 🔍

링크를 전달했을 때 나오는 영역을 살펴봐야겠습니다. 예시는 구글 이미지로 가져왔습니다. 저는 제 블로그로 확인을 해보았는데요. 블로그 링크를 공유하면 블로그 title, description이 나오는 거로 봐서는 html head 태그에 들어가는 메타태그와 관련이 있어보였습니다.

![web thumbnail](/assets/images/20240509/webThumb.png)

일반적으로 sns나 웹페이지들은 다음과 같은 정보를 사용하여 미리보기를 생성합니다.

- 페이지 제목: HTML의 <title> 태그에 지정된 제목
- 페이지 설명: 페이지의 Meta Tag 의 description 사용합니다. <meta name="description" content="...">
- 페이지 이미지: 페이지에서 사용된 이미지 중 대표적인 이미지, 페이지의 콘텐츠 중 하나

메타태그를 작성하지 않아도 웹사이트에서는 웹 페이지의 콘텐츠를 분석해서 미리보기를 생성하려고 합니다. 그래서 이 블로그같은 경우에도 메타태그에 넣지 않은 프로필 이미지가 썸네일로 나왔던 것입니다.

페이지 링크 미리보기가 랜덤으로 생성되지 않고 원하는 대로 바꿀 수는 없을까요?

# 오픈 그래프 프로토콜

웹사이트나 링크를 공유, 첨부했을 때 미리보기를 원하는 대로 만들 수 있는 것은 <span class="h-yellow">Open Graph Data</span>덕분입니다. **Meta**(구 Facebook)에서 웹 사이트에 다양한 메타 데이터를 제공하기 위해 발명한 메타 데이터 프로토콜입니다. 이를 통해서 우리가 sns에 링크를 첨부하거나, 메시지로 링크를 보냈을 때 미리보기 이미지와 요약된 페이지 정보를 볼 수 있는 것입니다.

## OG TAG 사용하기

가장 기본적인 메타데이터들입니다. 이것들을 통해서 링크 썸네일(미리보기)이 그려지게 됩니다.
- <code>og:title</code> - 페이지 제목 
- <code>og:type</code> - 페이지 유형
- <code>og:image</code> - 페이지 이미지
- <code>og:url</code> - 미리보기에 보여질 링크<br>( https://yeol0324.github.io/web/url-link-thumbnail/ -> https://yeol0324.github.io/ )
- <code>og:description</code> - 페이지 설명 


html head 태그에 meta태그를 생성 후 property 에 속성값들을 적고 content에 적어주면 끝입니다.
```html
<meta property="og:title" content="Lumi">
<meta property="og:type" content="website" />
<meta property="og:image" content="/assets/thumbnail.jpg">
<meta property="og:url" content="https://yeol0324.github.io/">
<meta property="og:description" content="LUMI's 개발 블로그">
```

짠 ✨<br>
![og 적용 이미지](/assets/images/20240509/ogimage.png)

제가 원하는 대로 잘 적용이 되었습니다.


# 테스트 해보기 (OGTAG Test)

OG태그가 잘 적용이 되었는지 테스트를 해보고싶은데 할 때마다 카톡으로 지인에게 공유하기, sns에 올리기는 너무 ···. 앞에서 og 태그는 Meta에서 발명했다고 했는데요, Meta에서는 테스트 할 수 있는 페이지도 만들어두었습니다 ! ㅋㅋㅋ

[Meta og tag 테스트](https://developers.facebook.com/tools/debug/)

# 주의 ⚡️
og 메타 태그는 html 에서 공식으로 지원하는 태그가 아닌 메타에서 발명한 태그입니다. 모든 sns, 웹사이트에서 적용되는 것이 아니라는 것은 알아두어야합니다. 일부 사이트에서는 지원이 되지 않을 수도 있다는 것이죠. 😅 그래도 언제 어디선가 공유가 되고 유명해질 저희의 사이트를 생각하면서 사소한 것도 신경을 써주는 게 좋겠습니다.

og tag가 표준이 되는 게 제일 좋겠습니다.

- <https://ogp.me/>
- <https://developer.mozilla.org/ko/docs/Learn/HTML/Introduction_to_HTML/The_head_metadata_in_HTML>
- [오픈그래프(Open Graph) meta og 태그(tag)와 트위터 카드(Twitter Cards)](https://www.next-t.co.kr/blog/%EA%B2%80%EC%83%89%EC%97%94%EC%A7%84%EC%B5%9C%EC%A0%81%ED%99%94-SEO-%ED%85%8C%ED%81%AC%EB%8B%88%EC%BB%ACSEO-%EC%98%A4%ED%94%88%EA%B7%B8%EB%9E%98%ED%94%84-OpenGraph-metaogtag-%ED%8A%B8%EC%9C%84%ED%84%B0%EC%B9%B4%EB%93%9C-TwitterCards)