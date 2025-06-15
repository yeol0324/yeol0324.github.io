---
layout: post
title: "JavaScript Array Deep Dive (6) — 실전 배열 활용"
date: 2025-06-14 22:01:24 +09:00
summary: "배열을 기반으로 한 실전 구현! 다차원 배열, 큐/스택, 알고리즘 문제까지"
categories: javascript
tags: javascript Array deepdive 프론트엔드 V8 최적화
---


배열, 단순 리스트 넘어 자료구조

지금까지 배열의 개념과 메서드를 배웠다면, 이제 활용할 차례입니다. 배열은 단순한 리스트 이상의 역할을 하며, 실전에서는 **큐, 스택**, 심지어 **행렬 같은 다차원 배열**까지 표현할 수 있습니다. **자바스크립트 배열을 자료구조처럼 활용하는 실전 예제들**을 알아봅시다.

---

## 다차원 배열

**다차원 배열**: 행(row)과 열(column)로 구성된 2차원 배열을 살펴보고, 중첩 루프를 통해 순회하는 방법을 알아봅니다.

```js
const matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
];

console.log(matrix[1][2]); // 6
```

- 행(row)과 열(column)로 구성
- 중첩 루프를 통해 순회 가능

```js
for (let row of matrix) {
  for (let value of row) {
    console.log(value);
  }
}
```

---

## 큐 (Queue): FIFO

**큐**: `push()`로 요소를 넣고 `shift()`로 꺼내는 FIFO (First In First Out) 구조를 배열로 구현합니다.

```js
const queue = [];

queue.push(1); // enqueue
queue.push(2);
console.log(queue.shift()); // dequeue → 1
console.log(queue.shift()); // 2
```

- `push()`로 넣고 `shift()`로 꺼냄
- **입력은 뒤, 출력은 앞**

---

## 스택 (Stack): LIFO

**스택**: `push()`로 요소를 넣고 `pop()`으로 꺼내는 LIFO (Last In First Out) 구조를 배열로 구현합니다.

```js
const stack = [];

stack.push(1);
stack.push(2);
console.log(stack.pop()); // 2
console.log(stack.pop()); // 1
```

- `push()`로 넣고 `pop()`으로 꺼냄
- **입력도, 출력도 뒤**

---

## 배열 활용 알고리즘 예시

#### 괄호 짝 검사 (스택 활용)

```js
function isValidParen(s) {
  const stack = [];
  for (let ch of s) {
    if (ch === '(') stack.push(ch);
    else {
      if (stack.length === 0) return false;
      stack.pop();
    }
  }
  return stack.length === 0;
}

isValidParen("(())"); // true
isValidParen("(()");  // false
```

---

#### 2차원 배열 회전

```js
function rotateMatrix(matrix) {
  return matrix[0].map((_, colIndex) =>
    matrix.map(row => row[colIndex]).reverse()
  );
}

rotateMatrix([
  [1, 2],
  [3, 4]
]);
// → [[3, 1], [4, 2]]
```

---

#### 중복 제거

```js
const arr = [1, 2, 2, 3, 4, 4];
const unique = [...new Set(arr)];
console.log(unique); // [1, 2, 3, 4]
```

> Set과 배열을 결합하면 빠르게 중복 제거 가능

---

## 배열은 진짜 자료구조

배열은 단순한 값 목록을 넘어 **큐, 스택, 트리, 그래프 구현까지** 다양한 자료구조를 표현하는 데 활용될 수 있습니다. 배열 메서드에 익숙해졌다면 이제 **구조적 활용**에 익숙해질 차례입니다. 알고리즘 문제 해결 능력 향상을 위해서도 배열을 자유자재로 다루는 것은 필수적입니다.
