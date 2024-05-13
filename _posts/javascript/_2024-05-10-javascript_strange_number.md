---
layout: post
title: 자바스크립트 가장 큰 숫자
summary: javascript MAX_SAFE_INTEGER
date: 2024-05-10 17:36:01 +09:00
categories: javascript
tags: javascript
---

javascript에는 숫자를 Number 타입 한가지로만 정의합니다. 64비트 IEEE 754 기준이며 -(2^53 -1) 와 2^53 -1 사이의 숫자만 정확한 계산이 가능합니다. 즉, -9007199254740991 ~ 9007199254740991 사이의 값만 존재하는 것입니다. 이 범위를 넘어가는 숫자를 사용한다면 주의를 기울여야합니다.

# MAX 그리고 MIN
javascript 의 Number 객체에는 MAX_VALUE, MIN_VALUE 라는 값이 존재합니다. 자바스크립트에서 표현 가능한 가장 큰, 가장 작은 숫자입니다. 시작할 때 말했듯 JS 는 -(2^53 -1) 와 2^53 -1 사이의 값만 정확하게 계산할 수 있기 떄문에 사실상 필요없는 값이라고 볼 수도 있습니다. 이보다 큰 값은 Infinity라고 표현합니다.


# SAFE_INTEGER
MAX_SAFE_INTEGER는 JS에서 안전한 가장 큰 숫자입니다. 반대로 가장 작은 숫자인 MIN_SAFE_INTEGER도 있습니다. 다음 예시를 보겠습니다.
```javascript
const max = Number.MAX_SAFE_INTEGER; //9007199254740991

const a = Number.MAX_SAFE_INTEGER + 1;
const b = Number.MAX_SAFE_INTEGER + 2;
console.log(a==b) // true

const min = Number.MIN_SAFE_INTEGER; //-9007199254740991
const c = Number.MIN_SAFE_INTEGER -1
const d = Number.MIN_SAFE_INTEGER -2
console.log(c==d) // true
```
이게 가능한가요? JS에서는 가능합니다. MAX_SAFE_INTEGER는 자바스크립트가 계산할 수 있는 가장 큰 숫자입니다. 그래서 그 숫자를 넘어간 MAX_SAFE_INTEGER + 1 과 MAX_SAFE_INTEGER + 2가 같다는 결과가 나옵니다. 2^53 -1 이상의 값을 사용하면 오류가 발생할 수 있습니다. 예상하지 못한 오류를 방지하기 위해 <span class="h-yellow">근사값을 계산해야하는 일이 있으면 미리 검사가 필요</span>합니다. 

# isSafeInteger
```javascript
Number.isSafeInteger(3939) // true
Number.isSafeInteger(Number.MAX_VALUE) //false
Number.isSafeInteger(Number.MAX_SAFE_INTEGER) //true
Number.isSafeInteger(Number.MAX_SAFE_INTEGER + 1) //false
```
Number.isSafeInteger() 의 인자값으로 숫자를 검사하고 사용할 수 있습니다.

