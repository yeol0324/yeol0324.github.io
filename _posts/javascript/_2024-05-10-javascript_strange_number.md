---
layout: post
title: Javascript 이상한 Number
summary: javascript MAX_SAFE_INTEGER, EPSILON
date: 2024-05-10 17:36:01 +09:00
categories: javascript
tags: javascript
---

javascript에는 숫자를 Number 타입 한가지로만 정의합니다. 64비트 IEEE 754 기준이며 -(2^53 -1) 와 2^53 -1 사이의 숫자만 표현하고 계산이 가능합니다. 즉, -9007199254740991 ~ 9007199254740991 사이의 값만 존재하는 것입니다.

# MAX_SAFE_INTEGER
MAX_SAFE_INTEGER는 JS에서 안전한 가장 큰 숫자입니다. 다음 예시를 보겠습니다.
```javascript
const max = Number.MAX_SAFE_INTEGER; //9007199254740991

const a = Number.MAX_SAFE_INTEGER + 1;
const b = Number.MAX_SAFE_INTEGER + 2;
console.log(a==b) // true
```
이게 가능한가요? JS에서는 가능합니다. MAX_SAFE_INTEGER는 자바스크립트가 계산할 수 있는 가장 큰 숫자입니다. 그래서 그 숫자를 넘어간 MAX_SAFE_INTEGER + 1 과 MAX_SAFE_INTEGER + 2가 같다는 결과가 나옵니다. 2^53 -1 이상의 값을 사용하면 오류가 발생할 수 있습니다. 그래서 근사값을 계산해야하는 일이 있으면 미리 검사가 필요합니다. 

# isSafeInteger
```javascript
Number.isSafeInteger(3939) // true
Number.isSafeInteger(Number.MAX_VALUE) //false
Number.isSafeInteger(Number.MAX_SAFE_INTEGER) //true
Number.isSafeInteger(Number.MAX_SAFE_INTEGER + 1) //false
```
Number.isSafeInteger() 의 인자값으로 숫자를 검사하고 사용할 수 있습니다.

# EPSILON
```javascript
Number.EPSILON - 1 //-0.9999999999999998
```

- <https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER>