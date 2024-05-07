---
layout: post
title: 자바스크립트의 실행 컨텍스트
summary: JavaScript Execution Context (실행 컨텍스트) 란?
date: 2024-05-03 15:48:04 +09:00
categories: javascript
tags: javascript
---

자바스크립트의 호이스팅, 스코프 체이닝이 왜 발생하는 걸까요? 자바스크립트 엔진의 실행 컨텍스트에 의해 생기는 현상입니다. 항상 헷갈리는 실행 컨텍스트를 정리해보았습니다.

# 실행 컨텍스트 (Execution Context)

"코드를 실행하는데 필요한 환경을 제공하는 객체"

실행 컨텍스트란 실행될 코드에 필요한 여러가지 정보를 모아놓은 객체입니다. 자바스크립트 엔진이 스크립트 파일을 실행하기 전에 <span class="h-yellow">글로벌 실행 컨텍스트(Global Execution Context, GEC)</span>가 생성이 되고, 이후에 함수를 호출할 때마다 생성이 됩니다.
자바스크립트는 하나의 콜스택을 갖는 단일 스레드 기반 언어이자 동적 언어인데요, Execution Context는 JavaScript 의 <span class="h-yellow">Call Stack</span>에 쌓이게 됩니다.

```javascript
function outer() {
  function inner() {
    // ...생략...
  }
  inner()
}
outer()
```
![alt text](https://velog.velcdn.com/images/hameee/post/c03345a2-8a87-4ea3-acb6-2ddbc2e242ff/image.png)
이런 순으로 Call Stack에 Execution Context가 쌓이고 빠진다.


# 필요한 정보가 뭘까?

여기서 자바스크립트가 코드를 실행하기 위해 필요한 정보들이란 뭘까요? 변수, 함수 선언, 변수의 유효범위(scope), this 등으로 생각해볼 수 있습니다.


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



# 실행 컨텍스트의 구성

실행 컨텍스트는 어떻게 생겼을까요? 실행 컨텍스트 객체는 활성화되는 시점에 VariableEnvironment, LexicalEnvironment, ThisBinding의 세 가지 정보를 수집합니다.


![실행 컨텍스트의 구성](/assets/images/2024-05-03/01.png)

<code>VariableEnvironment</code> 현재 컨텍스트 내의 식별자들에 대한 정보, 외부 환경 정보<br/>
<code>LexicalEnvironment</code> VariableEnvironment를 복사 후 변경 사항이 실시간으로 반영됨<br/>
<code>ThisBinding</code> this 식별자가 바라봐야 할 대상 객체

실행 컨텍스트를 생성할 때 VariableEnvironment에 정보를 먼저 담은 다음, 이를 그대로 복사해서 LexicalEnvironment를 만들어냅니다. 두 개 다 environmentRecord와 outerEnvironmentReference로 구성되어 있습니다. 복사를 해서 만든 객체이기때문에 동일해 보이지만 초기 값만 똑같고 코드가 진행되면서 이후에는 완전히 다른 정보가 담겨있게 됩니다.

자바스크립트 엔진은 이렇게 이루어진 실행 컨텍스트를 생성 단계(Creation Phase), 실행 단계(Execution Phase) 두가지 단계를 거쳐 생성을 합니다.

# Creation Phase 생성단계

생성 단계 동안 두 가지 일이 일어납니다.
- LexicalEnvironment 컴포넌트 생성
- VariableEnvironment 컴포넌트 생성 <br>

렉시컬 환경은 세가지 일을 한다. (VariableEnvironmnet도 동일)

- 환경 레코드(Environment Record) 식별자와 참조 혹은 값을 기록
- 외부 환경 참조(outer Environment Reference) 다른 렉시컬 환경을 참조하는 포인터
- this 바인딩(this binding)

## 환경 레코드

EnvironmentRecord(환경 레코드)에는 현재 컨텍스트와 관련된 코드의 식별자 정보들이 저장됩니다.
코딩을 할 때 변수나 함수 이름짓기가 제일 어렵습니다! 누구나 보고 이해하기 쉽게 의미를 부여해서 이름을 지으려고 합니다.하지만 javascript 엔진 (컴퓨터)는 인간이 아니기 자바스크립트의 입장에서는 변수나 함수는 그냥 단순한 하나의 메모리 주소인 것입니다. 그래서 자바스크립트 엔진은 { 이름: 값 } 처럼 대응표를 만들어 사용합니다. 이렇게 만들어진 대응표가 환경레코드와 같다고 볼 수 있습니다.

컨텍스트 전체를 처음부터 끝까지 쭉 읽으며 식별자들을 수집합니다. 여기에서 수집되는 식별자들은 매개변수 식별자, 선언된 함수, var로 선언된 변수의 식별자 등이 해당한다.

EnvironmentRecord(환경 레코드)는 현재 컨텍스트와 관련된 코드의 식별자 정보들만이 저장되기떄문에, 변수를 인식할 때 식별자만 끌어올려 수집을 하고 할당 과정은 원래 자리에 순서대로 남겨둡니다.

```javascript
var x = 'yurim' // { x : undefined }
let y = 'yurim' // { y }
const z = 'yurim' // { z }

function foo () {  // { foo : f{} }
  // function foo
}
var bar = () => {  // { bar : undefined }
  // function bar
}
```
위의 코드에서, 실행 컨텍스트의 EnvironmentRecord에는 식별자 x, y, z와 함수 foo, bar가 수집됩니다.
이 과정에서 var 는 undefined로 초기화가 되고 let, const 는 초기화가 되지 않는 것을 hoisting 에서 볼 수 있습니다. [자바스크립트 호이스팅]({{base_path}}/javascript/javascript-hoisting/)


## outer
outer Environment Reference(Scope-Chainning)는 외부 렉시컬 환경을 참조하는 포인터로, 중첩된 자바스크립트의 스코프 탐색을 위해 사용됩니다.

예를 들면
```javascript 
var text = 'hello'
function sayHello (){
  console.log(text)
}
```
엄청 간단한 위 함수를 예시로 보겠습니다. sayHello라는 함수에서 text 라는 변수를 가지고 있지 않지만 외부에 있는 변수를 참조하여 읽을 수 있게 됩니다. 외부 환경 참조(outer Environment Reference) 과정으로 인해서 스코프 체이닝이 가능한 것입니다. 자바스크립트의 스코프 체이닝에 관해서는 다시 글을 정리해볼 예정입니다.

## this binding

this 식별자가 바라봐야 할 대상 객체입니다. javascript 의 this 는 많은 것을 포함하고 또 복잡해서 새로운 글로 정리를 해보겠습니다.


# Execution Phase 실행단계
생성단계에서 식별자 정보들이 저장이 다 되고나서, 선언문 외 나머지 코드 순차적으로 진행합니다. Execution 단계가 되면 우선 variable을 update혹은 initialize합니다. 여기서 undefind였던 변수들의 값들을 할당하며 코드를 실행시킵니다.


# 마무리
정말 복잡하고 어려운 개념이었습니다. 자바스크립트의 동작 원리를 정말! 간단히만 알고 있었는데 계속 미뤄두었던 실행 컨텍스트를 깊게 공부를 해보니, 실무에서 겪었던 문제들이 조금씩 이해가 되었습니다. 글로 정리하면서도 복잡한 것 같아서 어떻게 해야 간단하게 정리할 수 있을지 한참 고민을 했는데 남에게 알기 쉽게 정리하는 것이 제일 어려운 것 같습니다. 정리하면서 찾아보는 곳마다 표현하는 용어가 조금씩 다르기도 했고 내용이나 예제가 많이 달라서 하나씩 읽어보느라 더 이해가 잘된 것 같습니다. 이 글을 읽고 애매한 부분은 다시 한번 검색을 하면서 정리를 해보시는 걸 추천합니다.


---
참고
- [자바스크립트의 실행 컨텍스트 (execution context)](https://velog.io/@ggong/%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8%EC%9D%98-%EC%8B%A4%ED%96%89-%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8-execution-context)
- [[자바스크립트] variable과 LexicalEnvironment (feat 코어 자바스크립트)](https://overcome-the-limits.tistory.com/m/331)
- [자바스크립트 동작원리와 ES6 - Fundamentals of JavaScript & ES6](https://brewagebear.github.io/fundamentals-of-javascript/#step-13-%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8-%EC%8B%A4%ED%96%89%EC%BB%A8%ED%85%8D%EC%8A%A4%ED%8A%B8javascript-execution-context)
- [[코어 자바스크립트] Execution Context](https://velog.io/@hameee/%EC%BD%94%EC%96%B4-%EC%9E%90%EB%B0%94%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8-Execution-Context)