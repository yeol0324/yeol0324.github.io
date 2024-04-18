---
layout: post
title: "typescript type vs interface"
date: 2024-03-02 10:06:52 +0900
categories: javascript
tags: javascript typescript
---
이름만 다르고 타입을 정의한다는 점과 선언 시 형태가 다르다고만 생각했었던 것

https://steadily-worked.tistory.com/537
```
interface Book {
  title: string
  page: number
}

const myBook: Book = {
  title: 'typescript',
  page: 34,
}

type Book = {
  title: string
  page: number
}

const myBook: Book = {
  title: 'typescript',
  page: 34,
}
```