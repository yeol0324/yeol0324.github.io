---
layout: post
title: 자바스크립트의 실행 컨텍스트
summary: JavaScript Execution Context (실행 컨텍스트) 란?
date: 2024-05-03 15:48:04 +09:00
categories: javascript
tags: javascript
---

Javascript의 Hoisting
# 실행 컨텍스트 (Execution Context)
실행 컨텍스트란 실행될 코드에 필요한 여러가지 정보를 모아놓은 객체입니다. 자바스크립트 엔진에 의해 만들어지는데, 엔진이 스크립트 파일을 실행하기 전에 단 하나 생셩되는 <span class="h-yellow">글로벌 실행 컨텍스트(Global Execution Context, GEC)</span>와 함수를 호출할 때마다 생성되는 <span class="h-yellow">함수 실행 컨텍스트(Function Execution Context, FEC)</span> 마지막으로 eval 함수에서 생성되는 <span class="h-yellow">Eval Function Execution Context</span>(현재는 거의 사용하지 않습니다)가 있습니다.


# 필요한 정보가 뭘까?
변수, 함수 선언, 변수의 유효범위, this 등으로 생각해볼 수 있습니다.


간단한 함수로 예시를 들어보면
```javascript
let a = 0;
function print(num: number) {
  console.log(num);
}
print(a); 
```
print(a) 라는 함수가 실행되기 위해서 필요한 정보들을 생각해보겠습니다. 
일단 a 가 뭔지 알고 있어야하고, print에 대한 정보도 알아야할 것입니다. print에 전달한 a를 보면, 우리는 한눈에 볼 수 있으니 print(a) 라는 함수를 보고 윗줄에 선언된 a라는 변수를 찾을 수 있습니다. 컴퓨터 입장에서는 이렇게 찾을 수가 없기 때문에 정보들이 필요한 것입니다.


1️⃣ 실행 컨텍스트(Execution Context)에 대해서 설명해주세요.
실행 컨텍스트는 실행 가능한 코드에 제공할 환경 정보를 모아놓은 객체입니다.
해당 객체에는 변수 객체, 스코프 체인, this 정보가 담겨있습니다.
자동으로 전역 컨텍스트가 생성된 후 함수 호출시마다 함수 컨텍스트가 생성되고, 컨텍스트 생성이 완료된 후에 함수가 실행됩니다. 함수 실행 중에 사용 되는 변수들을 변수 객체 안에서 값을 찾고 값이 존재하지 않는다면 Lexical 환경의 outerEnvironmentReference를 통해 Scope 체인을 따라 올라가면서 탐색합니다. 함수 실행이 마무리가 되면 해당 컨텍스트는 사라지고, 페이지가 종료되면 전역 컨텍스트도 사라집니다.

2️⃣ 렉시컬 환경이란 무엇인가요?
렉시컬 환경은 특정 코드가 선언된 환경을 의미하는 객체입니다.
환경 레코드와 외부환경레퍼런스로 나뉘는데,
환경레코드에는 현재 컨텍스트와 관련된 코드의 식별자 정보가 저장됩니다. 즉, JS 엔진은 코드가 실행되기 전에 실행 컨텍스트에 속한 변수명을 모두 알고 있는 것인데요, 이를 위해 호이스팅이 발생한다고 볼 수 있습니다.
외부환경레퍼런스는 현재 호출된 함수가 선언될 당시의 렉시컬 환경을 참조하는데, 이를 이용해서 스코프 체이닝이 가능해집니다.

3️⃣ 실행 컨텍스트의 객체에 담긴 정보는 무엇이 있나요?
변수 객체, Scope 체인, this 값이 있습니다.
변수 객체에는 변수, 매개변수parameter, 인수argument 정보와 함수 정보가 담겨있고, 이때 변수와 함수 표현식으로 생성된 함수는 생성은 되지만 초기화는 되지 않아 undefined 상태입니다.
스코프 체인은 연결리스트 형태로 스코프 정보가 저장된 것이고,
this 값에는 이 변수 객체의 this에 바인딩 할 객체를 저장합니다.

4️⃣ 자바스크립트는 어떤 언어인가요?
자바스크립트는 하나의 콜스택을 갖는 단일 스레드 기반 언어이자 동적 언어입니다.
![](https://miro.medium.com/v2/resize:fit:1100/1*dUl6qPEaDJJTXWythQsEtQ.gif)


- [https://medium.com/hcleedev/...](https://medium.com/hcleedev/web-javascript%EC%9D%98-%EC%8B%A4%ED%96%89-%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8-lexicalenvironment-scop-ce664aa2076)
- [https://velog.io/@imacoolgirlyo/...](https://velog.io/@imacoolgirlyo/JS-%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%EC%9D%98-Hoisting-The-Execution-Context-%ED%98%B8%EC%9D%B4%EC%8A%A4%ED%8C%85-%EC%8B%A4%ED%96%89-%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8-6bjsmmlmgy)
- <https://techwell.wooritech.com/docs/languages/javascript/execution-context/>
- <https://betterprogramming.pub/javascript-internals-execution-context-bdeee6986b3b>