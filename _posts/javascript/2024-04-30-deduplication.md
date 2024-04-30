---
layout: post
title: "javascript 배열 문자열 중복 값 제거"
date: 2024-04-30 11:06:52 +0900
categories: javascript
tags: javascript array
---

javascript Array 를 다룰 때 중복 값을 제거해야할 경우가 많습니다. 오늘은 자바스크립트 배열과 문자열 중복 값을 제거하는 다양한 방법을 알아보겠습니다.

# Set 이용

Javascript 의 Set 객체를 이용하여 중복 데이터를 제거할 수 있습니다. Set 객체로 리턴이 되기 때문에 다시 array 에 담아서 사용을 할 수 있습니다. 문자열인 경우는 다시 string으로 만들기 위해서 join()을 사용해줍니다.

```javascript
// 배열 중복값 제거
const arr = [1,2,3,2,3,6,3,4];
const dup = new Set(arr); // Set(5) {1, 2, 3, 6, 4}
const uniqueArr = [...dup]; // [1, 2, 3, 6, 4]

// 문자열 중복값 제거
const str = 'hello';
const uniqueStr = [...new Set(str)].join('');

console.log(uniqueStr); // 'helo'
```

# filter 이용

<span class="h-yellow">filter()</span>는 주어진 배열에서 조건을 통과한 요소로만 필터링하는 Array 인스턴스의 메서드입니다.

```javascript
// 배열 중복값 제거
const arr = [1,2,3,2,3,6,3,4];
const uniqueArr = arr.filter((item, index) => arr.indexOf(item) === index);
console.log(uniqueArr); // [1, 2, 3, 6, 4]

// 문자열의 중복값 제거
const str = 'hello';
const uniqueStr = str.split('').filter((el, index, arr) => arr.indexOf(el) === index).join('');
console.log(uniqueStr); // 'helo'
```

# for 활용

다양한 for 문을 활용해서 제거를 해줄 수 있습니다. 빈 array를 생성해두고 forEach를 사용해 includes 로 검사를 해서 중복 아닌 값만 담아주었습니다.
```javascript
// 배열의 중복값 제거
const arr = [1,2,3,2,3,6,3,4];
const uniqueArr = [];

arr.forEach(el => {
  if (!uniqueArr.includes(el)) {
    uniqueArr.push(el);
  }
});

console.log(uniqueArr); // [1, 2, 3, 6, 4]

// 문자열 중복값 제거
const str = 'hello';
let uniqueStr = '';

str.split('').forEach( st =>{
  if (!uniqueStr.includes(st)) {
    uniqueStr += st;
  }
});

console.log(uniqueStr); // 'helo'
```

다양한 방법이 있는데 상황마다 쓸 수 있는 방법이 모두 다르죠. 해결해야 할 문제에 가장 알맞는 방법을 선택해서 사용하시면 됩니다.