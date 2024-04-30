---
layout: post
title: "마크다운에 이미지 첨부하기"
date: 2024-4-30 10:06:52 +0900
categories: etc
tags: markdown
---

마크다운에 이미지를 첨부하는 방법입니다. 이미지 가운데 정렬, 왼쪽 오른쪽 정렬, 크기조정 방법을 알아봅시다.

```markdown
![이미지 설명](경로)

# ex
![alt](/assets/images/2024-03-02-jekyll-github-blog-1/01.png)
```

마크다운은 html 마크업 언어도 사용할 수 있어서 당연히 img 태그로도 첨부가 가능합니다.
img 태그를 사용하면 다양한 속성을 부여할 수 있습니다.
```html
<!-- 왼쪽 정렬, width, height 조정 -->
<img align="left" src="./image.png" width="100px" height="100px"/>
<!-- 가운데 정렬 -->
<p align="center">
 <img src = "./image.png">
</p>
```
