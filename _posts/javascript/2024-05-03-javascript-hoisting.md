---
layout: post
title: 자바스크립트 호이스팅
summary: 
date: 2024-05-03 14:30:24 +09:00
categories: javascript
tags: javascript
---

# 호이스팅?
>JavaScript 호이스팅은 인터프리터가 코드를 실행하기 전에 함수, 변수, 클래스 또는 임포트(import)의 선언문을 해당 범위의 맨 위로 끌어올리는 것처럼 보이는 현상 - [MDN Web Docs 용어 사전](https://developer.mozilla.org/ko/docs/Glossary/Hoisting)

호이스팅(Hoisting)은 "끌어 올리기, 들어올려 나르기." 라는 뜻으로 자바스크립트가 실행될 때 변수나 함수가 끌어올려지는 현상을 말합니다. Javascript 엔진이 코드를 실행하기 전 코드를 한번 훑는 과정을 거치는데 여기서 모든 선언을 scope 에 등록을 합니다. 자바스크립트의 호이스팅을 확인해보겠습니다.

# 변수의 호이스팅

ECMAScript 2015의 let과 const는 변수를 블록의 상단으로 끌어올리지만 초기화하지 않습니다. 이때문에 let, const 에서는 이용한 선언문을 호이스팅이 발생하지 않는 것처럼 동작합니다.

```javascript
console.log(unnamed) // Uncaught ReferenceError: unnamed is not defined
```
```javascript
console.log(namevar); // undefined
var namevar = 'yurim';
```
```javascript
console.log(namelet); // ReferenceError: Cannot access 'namelet' before initialization
let namelet = 'yurim';
```
```javascript
console.log(nameconst); // ReferenceError: Cannot access 'nameconst' before initialization
const nameconst = 'yurim';
```

위에서 말했듯, let 과 const 도 호이스팅이 발생하지만 초기화가 되지 않아 접근할 수 없다는 오류로, 호이스팅이 있음을 알 수 있습니다. 변수가 선언되기 전에 블록 안에서 변수를 참조하게 되면 ReferenceError를 발생시키게 되는데, 변수는 블록 시작부터 선언이 처리될 때까지 "temporal dead zone"에 위치하게 되기 때문입니다.


# 함수의 호이스팅


함수에서는 함수 선언(function declaration)으로는 호이스팅되지만 함수 표현식(function expression)으로는 호이스팅 되지 않습니다.

```javascript
declaration()

function declaration (){
    console.log('hello') // hello
}
```
```javascript
expression()

const expression = ()=>{
    console.log('hello') // eferenceError: Cannot access 'expression' before initialization
}
```

여기서 변수의 호이스팅을 잘 이해했는지 확인해볼 수 있습니다. 함수 표현을 const가 아닌 var로 했다면 결과가 어떻게 될까요?

```javascript
console.log(expression); // undefined

expression()

var expression = ()=>{
    console.log('hello') // TypeError: expression is not a function
}
```



정답은 <span class="h-yellow">TypeError</span> 입니다. 함수를 var로 표현하여 자바스크립트에서는 var를 읽고 undefined로 초기화를 한 상태이기 때문에 함수를 실행하려고 하면 함수가 아니라는 에러가 출력되는 것입니다.

# 호이스팅 방지하기
호이스팅이 에러를 발생시키는 것은 아니지만 코드의 가독성이나 유지보수 측면에서 호이스팅이 일어나지 않도록 하는 것이 좋습니다.
변수를 선언할 때 let, const 를 사용을 지양하고, var 를 사용한다면 사용하는 함수 상단이나 문서 상단에 선언을 하는 걸 잊지 맙시다! 


참고
- <https://developer.mozilla.org/ko/docs/Glossary/Hoisting>
