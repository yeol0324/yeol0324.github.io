---
layout: post
title: JavaScript Array Deep Dive (1) — 배열이란 무엇인가?
summary: 자바스크립트 배열의 개념과 구조, 객체와의 차이, 유사 배열까지 완벽 정리해보자
date: 2025-05-08 14:30:24 +09:00
categories: javascript
tags: javascript Array deepdive 프론트엔드
---

1화: 배열이란 무엇인가 — 자바스크립트 배열 개요

 “배열을 모르면 JavaScript를 모르는 것이다”

자바스크립트를 공부하다 보면 가장 먼저 마주치는 것이 변수이고, 그 다음이 배열입니다.  
그만큼 배열은 모든 프로그래밍 언어에서 기본 중의 기본이자, 실무에서 가장 자주 사용하는 자료 구조 중 하나죠.  

하지만 자바스크립트의 배열은 단순한 숫자 인덱스를 가진 리스트 그 이상입니다.  
객체처럼 동작하기도 하고, 함수를 내장하고 있으며, 어떤 자료형이든 자유롭게 담을 수 있는 다재다능한 구조이기도 하죠.

이번 포스트에서는 자바스크립트 배열의 개념과 기본 구조, 다른 자료형과의 차이점까지 꼼꼼히 정리해보겠습니다.

---

## 1. 배열(Array)란 무엇인가?

자바스크립트에서 배열은 **순서가 있는 값(value)의 집합**입니다.  
각 값은 **0부터 시작하는 정수 인덱스(index)**로 접근할 수 있고, 배열 전체는 하나의 객체(Object)처럼 동작합니다.

```js
const fruits = ['apple', 'banana', 'kiwi'];
console.log(fruits[0]); // 'apple'
console.log(fruits.length); // 3
```

> 배열은 `Object`의 하위 타입이며, 타입 판별 시 `typeof`는 `"object"`를 반환합니다.  
> 정확한 타입 체크를 위해 `Array.isArray()`를 사용하는 것이 좋습니다.

---

## 2. 배열 vs 객체 차이점 알아보기

| 특징 | 배열 (Array) | 객체 (Object) |
|------|---------------|----------------|
| 인덱스 | 숫자 기반 (0부터 시작) | 문자열 기반 키 |
| 순서 | 있음 | 없음 (ES6 이후 일부 순서 보장) |
| length | 자동 관리됨 | 없음 |
| 용도 | 목록/리스트 | 키-값 저장소 |

```js
const arr = ['a', 'b'];
const obj = { 0: 'a', 1: 'b' };

console.log(arr.length); // 2
console.log(Object.keys(obj).length);// 2
console.log(obj.length); // undefined
```

---

## 3. 자바스크립트 배열의 특이한 특징들

#### 1) 다양한 타입을 동시에 저장 가능
```js
const mixed = [1, 'two', true, null, undefined, { key: 'value' }, [3, 4]];
```

#### 2) 길이를 명시적으로 설정 가능
```js
const emptyArr = new Array(5);
console.log(emptyArr.length); // 5
console.log(emptyArr); // [ <5 empty items> ]
```

#### 3) 인덱스를 건너뛸 수 있음 (sparse array)
```js
const sparse = [];
sparse[3] = 'hello';
console.log(sparse); // [ <3 empty items>, 'hello' ]
```

#### 4) 배열도 객체이기 때문에 프로퍼티를 추가할 수 있음
```js
const arr = [1, 2];
arr.foo = 'bar';
console.log(arr.foo); // 'bar'
```

• 하지만 배열에는 키가 아닌 **숫자 인덱스를 사용하는 것만** 권장됩니다.  
• 일반 프로퍼티를 추가하면 `length`에 영향을 주지 않기 때문입니다.

✏️ 이런 상황에 쓰여요
1) 메타데이터나 부가 정보 저장
```js
const scores = [85, 90, 95];
scores.source = '중간고사';
console.log(scores) //[85, 90, 95, source: '중간고사']
console.log(scores.length) //3
```

2) 임시 디버깅용 속성
```js
arr._debugId = 'test123';
```

3) 커스터마이징이 어려운 경우
```js
function fetchItems() {
  const items = [1,2,3];
  items.loaded = true;
  return items;
}

const data = fetchItems();
if (data.loaded) { /* 로딩 여부 확인 */ }
```

 배열에 프로퍼티를 쓰는 건 “가능하지만 비권장”,
정말 간단한 임시 용도일 때만 제한적으로 사용하고,
실전에서는 배열+객체 분리하여 사용합시다!
```js
const scores = {
  values: [85, 90, 95],
  source: '중간고사'
};
```

---

## 4. 유사 배열 객체(Array-like objects)

```js
const arrayLike = {
  0: 'a',
  1: 'b',
  length: 2
};

console.log(arrayLike[0]); // 'a'
console.log(arrayLike.length); // 2

// Array.from으로 배열로 변환 가능
const realArray = Array.from(arrayLike);
console.log(realArray); // ['a', 'b']
```

✏️ "유사 배열 객체 (array-like object)"는 사실상 그냥 객체 (Object)이다. 단지 배열처럼 생긴 구조이고 진짜 배열은 아님!
• 숫자 인덱스를 키로 가지고 있다.
•	length 속성을 가진 객체이다 ‼️

즉, 배열처럼 보이고 작동하지만 Array 인스턴스는 아님.
```js
const divs = document.querySelectorAll('div')
console.log(divs) //NodeList(10) [0: div.red-button, ..., length: 88]
```

Array.from(divs) 또는 [...divs] 로 배열로 변환할 수 있습니다.

---

## 5. 배열의 선언과 생성 방식

```js
const arr1 = [];                 // 가장 일반적인 방식
const arr2 = new Array();        // 비추: 생성자 방식
const arr3 = Array.of(1, 2, 3);  // 명확한 생성
const arr4 = Array.from('hello'); // 'h', 'e', 'l', 'l', 'o'
```

✏️ 생성자 방식은 왜 비추일까? 🤔
1. 매개변수 개수에 따라 완전히 다른 동작을 함
```js
const a = new Array(3);     // [ <3 empty items> ]
const b = new Array(1, 2);  // [1, 2]
```
2. 비어 있는 슬롯(Hole)이 생김
```js
const arr = new Array(3);
console.log(arr); // [ <3 empty items> ]
```

3. 코드 일관성과 가독성 저하
```js
Array.of(3);        // [3] → 직관적
new Array(3);       // [ <3 empty items> ] → 헷갈림
```

❔그럼 개수만큼 array를 생성하고 싶은데, 어떻게 해야할까?
array 생성자 사용 후, fill을 사용해서 empty slot을 예방하자!

```js
const arr = new Array(5).fill('');
console.log(arr); // ['', '', '', '', '']
```
‼️객체일 때는 주의하자
fill(obj)는 같은 객체 참조를 채우기 때문에 모든 요소가 동일한 객체를 공유함

이럴 땐 .map(() => ({}))으로 분리 생성해야 합니다.
```js
const arr = new Array(3).fill({});
arr[0].x = 1;
console.log(arr); // 모든 요소가 {x: 1}
```
---


## 배열은 단순한 리스트가 아니다

자바스크립트에서 배열은 단지 데이터를 담는 그릇이 아니라, 객체와 함수의 성격을 동시에 가진 고급 자료 구조입니다.  
특히 그 유연함과 강력함 덕분에 프론트엔드, 백엔드, 알고리즘 구현 등 어디에서나 핵심적으로 사용됩니다.

**이제 진짜 "배열 고수"가 되어보자 🎖️**



