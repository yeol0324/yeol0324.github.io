---
layout: post
title: typescript 타입, 대체 뭘까?
summary: 
date: 2024-05-10 16:40:46 +09:00
categories: javascript
tags: typescript deepdive
---

타입스크립트란 자바스크립트에 타입을 추가한 슈퍼셋 프로그래밍 언어입니다. 컴파일을 거쳐 JavaScript 코드로 변환됩니다. 유연한 JS와 달리 조금 더 엄격한 문법으로 작성할 수 있습니다. 특히 타입을 명시하는 덕분에 "1"+"1" ="11" 같은 오류를 만나지 않을 수 있습니다. 타입은 <code>const num : number</code> 형식으로 지정합니다.

# 기본 타입
가장 중요한, 가장 많이 사용되는 기본적인 타입입니다.
```typescript
const name: string = 'yurim' // 단순 문자열
const age: number = 25 // 숫자 0, -1, 0.4 등 모든 숫자는 number 사용
const happy: boolean = true // 참|거짓 값으로 두가지 값만 가짐
```
# 배열
Array<T>, T[]로 표시하여 배열 안의 타입을 명시해줍니다.
```typescript
const list: string[] = ['item01','item02','item03']
const numbers: number[] = [1,2,3]
const fruits: Array<string> = ['apple','banana']
const sum: Array<number | string> = ["hi", 10]
```

튜플은 배열의 길이가 고정되며 각 요소의 타입이 정의됩니다.
```typescript
const list: [number, string] = ["hello", 10]; // ❌
const array: [string, number] = ['bye', 10] //⭕️
```

# 객체
```typescript

```

블로그를 시작하기 전에는 기록할 것이 있거나 오류 해결 내용은 다 notion에 기록을 했었습니다. 아마 javascript 만 사용하다가 typescript를 처음 사용하게 되면서 시작을 했던 것 같습니다. 이번에 블로그로 notion의 글들을 이전하면서 notion에 있는 글을 하나씩 읽어보니 ts를 사용하면서 겪은 오류의 대부분이 타입에 관한 문제였습니다. 전에는 뭣도 모르고 any 를 남발했던 것 같은데, 그때 했던 프로젝트 파일을 열어보면 아주 빨간 줄 천지입니다.
지금은 물론 any를 사용하는 일이 거의 없지만 개발을 하면서 타입을 검색하느라 애를 먹는 경우가 종종 있는 것 같습니다. 이번 기회에 typescript에 있는 타입을 한번 쭉 훑어보면서 정리도 하고 리마인드하는 시간이 되었습니다.