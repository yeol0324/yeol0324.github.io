---
layout: post
title: JavaScript Array
summary: 자바스크립트 배열의 개념과 구조, 객체와의 차이, 유사 배열
date: 2025-05-08 14:30:24 +09:00
categories: javascript
tags: javascript Array deepdive 프론트엔드
---
이 글에서 중복되는 내용 찾아줘



## **1. 자바스크립트의 배열**

> “배열을 모르면 JavaScript를 모르는 것이다”

자바스크립트를 공부하다 보면 가장 먼저 변수를 배우고 그 다음 배열을 배우게 됩니다. 그만큼 배열은 모든 프로그래밍 언어에서 기본이자 실무에서 가장 자주 사용하는 자료 구조 중 하나입니다.  

자바스크립트의 배열은 단순한 숫자 인덱스를 가진 리스트 그 이상입니다. 객체처럼 동작하기도 하고, 함수를 내장하고 있으며, 어떤 자료형이든 자유롭게 담을 수 있는 다재다능한 구조이기도 하죠.

자바스크립트 배열의 개념과 기본 구조, 다른 자료형과의 차이점까지 꼼꼼히 정리해보았습니다.


<p class="impact">배열(Array)란 무엇인가</p>

자바스크립트에서 배열은 순서가 있는 값(value)의 집합입니다.  
각 값은 index(0부서 시작)로 접근할 수 있고, 배열 전체는 하나의 객체(Object)처럼 동작합니다. 자바스크립트의 배열의 타입은 <span class="h-yellow">"object"</span>를 반환하기때문에 정확한 타입 체크를 위해 `Array.isArray()`를 사용하는 것이 좋습니다. 

```js
const fruits = ['apple', 'banana', 'kiwi'];

console.log(fruits[0]); // 'apple'
console.log(fruits.length); // 3

typeof fruits // 'object'
Array.isArray(fruits) // true
```

### 특이한 특징

1) 다양한 타입을 동시에 저장
2) 길이를 명시적으로 설정
3) 인덱스 생략
4) 프로퍼티 추가

```js
// 1) 다양한 타입을 동시에 저장
const mixed = [1, 'two', true, null, undefined, { key: 'value' }, [3, 4]];

// 2) 길이를 명시적으로 설정
const emptyArr = new Array(5);
console.log(emptyArr.length); // 5
console.log(emptyArr); // [ <5 empty items> ]

// 3) 인덱스 생략
const sparse = [];
sparse[3] = 'hello';
console.log(sparse); // [ <3 empty items>, 'hello' ]

// 4) 프로퍼티 추가
const arr = [1, 2];
arr.foo = 'bar';
console.log(arr.foo); // 'bar'
arr // [1, 2, foo: 'bar']
arr.length // 2
```

하지만 배열에는 키가 아닌 인덱스를 사용하는 것만 권장됩니다. 일반 프로퍼티를 추가하면 `length`에 영향을 주지 않기 때문입니다. 당연히 위에 있는 내용들은 실무에서 사용해본 적이 거의 없습니다. 


그럼 이 특징들은 언제 어떻게 쓰일까요?

1) 메타데이터나 부가 정보 저장
2) 임시 디버깅용 속성
3) 커스터마이징이 어려운 경우
```js
// 1) 메타데이터나 부가 정보 저장
const scores = [85, 90, 95];
scores.source = '중간고사';
console.log(scores) //[85, 90, 95, source: '중간고사']
console.log(scores.length) //3

// 2) 임시 디버깅용 속성
arr._debugId = 'test123';

// 3) 커스터마이징이 어려운 경우
function fetchItems() {
  const items = [1,2,3];
  items.loaded = true;
  return items;
}

const data = fetchItems();
if (data.loaded) { /* 로딩 여부 확인 */ }
```

명시적으로 코딩하는 것이 유지보수나 디버깅할 때 좋기 때문에 한번도 사용해본 적이 없습니다.


실무에서는 꼭 배열과 객체를 분리하여 사용합시다.


```js
const scores = {
  values: [85, 90, 95],
  source: '중간고사'
};
```



### 유사 배열 객체

Array에 Properties를 추가한 것과 비슷한 "유사 배열 객체(Array-like objects)" 라는 개념도 있습니다. 유사 배열 객체는 그냥 객체 (Object)입니다. 단지 배열처럼 생긴 구조이고 진짜 배열은 아니며 숫자 인덱스를 키로 가지고, length 속성을 가진 객체입니다. 배열처럼 보이고 작동하지만 Array 인스턴스는 아니기때문에 헷갈림 주의!

```js
const arrayLike = {
  0: 'a',
  1: 'b',
  length: 2
};

console.log(arrayLike[0]); // 'a'
console.log(arrayLike.length); // 2

// 실제로 사용되고있는 곳
const divs = document.querySelectorAll('div')
console.log(divs) //NodeList(10) [0: div.red-button, ..., length: 88]


// Array 로 변환하기
const realArray = Array.from(arrayLike);
const divArray = [...divs]

```

### 배열의 선언과 생성 방식

배열을 생성하는 방법은 여러가지가 있습니다.

배열은 선언만으로도 쉽게 사용할 수 있지만, 어떻게 만들었느냐에 따라 동작 방식이나 잠재적인 버그 발생 가능성이 완전히 달라집니다. 예를 들어, `new Array(5)`는 실제로 값을 넣는 것이 아니라 "비어 있는 5칸짜리 배열"을 만들고, `Array.of(5)`는 숫자 5 하나가 담긴 배열을 생성합니다. 헷갈리기 쉽지만 각 특성을 정리하고 꼭 기억해둡시다.

- 리터럴 방식
```js
const arr = [];                 // 가장 일반적인 방식
```

- Array 정적 메서드 사용
```js
// 전달된 값을 그대로 요소로 가지는 배열 생성
const arr = Array.of(1, 2, 3);   // [1, 2, 3]
// 이터러블/유사배열을 배열로 변환
const arr = Array.from('hello'); // ['h', 'e', 'l', 'l', 'o']
```

- 생성자 사용
```js
new Array();      // 생성자 방식 
new Array(3);     // [<3 empty items>] 길이 3짜리 비어있는 배열 생성
new Array(1,2,3)  // [1, 2, 3]
```

생성자를 사용하여 배열을 생성할 땐 주의할 점이 있습니다. 생성자 사용 예시 아래 2개를 봅시다. 인자가 1개일 때와 2개 이상일 때 전혀 다르게 동작합니다. 생성자로 배열을 생성할 때는 의도에 맞게 잘 활용해야합니다.

특히 new Array(3)은 `[undefined, undefined, undefined]`가 아닙니다. 실제로 비어 있는 슬롯이어서 map 같은 메서드를 사용할 수 없습니다.

```js
new Array(3).map(x => 1); // [ <3 empty items> ]
Array.from({ length: 3 }, () => 1); // [1, 1, 1]
```



## **2. 자바스크립트 배열의 동작 원리**

> 왜 같은 배열인데 성능이 다를까?

개발을 하다 보면 `map()` 하나 돌렸을 뿐인데 화면이 버벅이고, 수천 개의 데이터를 다루는 리스트에서 렉이 발생하는 경험을 하게 됩니다.  

이럴 때 많은 사람들은 "React 성능 때문인가?"라고 생각하지만, 사실 **자바스크립트 배열의 동작 방식**을 이해하면 문제의 원인을 훨씬 더 정확히 알 수 있습니다.

자바스크립트 배열이 메모리에서 어떻게 다뤄지는지, 그리고 왜 배열의 구조에 따라 성능 차이가 발생하는지를 알아봅시다.


### 컴퓨터에서의 배열 저장

전통적인 프로그래밍 언어(C, Java 등)의 배열은 **연속된 메모리 공간에 데이터를 저장**합니다.

```java
int arr[3] = {10, 20, 30};

/// 주소:   0x00  0x04  0x08
/// 값:     10    20    30
```

정적 배열로 길이가 고정이며 메모리에 연속으로 할당을 받습니다. 인덱스를 이용해 직접 주소 계산이 가능해서 접근 속도가 빠릅니다.


<span class="impact">자바스크립트는?</span>

자바스크립트 배열은 실제로는 **객체(Object)** 입니다.  
각 요소는 객체의 속성처럼 키-값으로 저장되며, 이 키는 문자열로 변환된 인덱스입니다.

```js
const arr = ['a', 'b'];
console.log(typeof arr); // 'object'
console.log(Object.keys(arr)); // ['0', '1']
```

자바스크립트의 배열은 실제로 `length` 속성과 정수형 키를 가진 객체이며 배열 요소가 비연속적으로 존재할 수 있습니다. 따라서 배열처럼 보여도 객체처럼 느리게 동작할 수 있는 것입니다.


### V8 엔진의 최적화

Google Chrome의 V8 엔진은 성능 최적화를 위해 배열을 분류합니다. 내부적으로는 타입에 따라 더 세부적으로 나누지만 크게 두 가지가 있습니다.

- Packed Elements : 연속된 인덱스를 가진 배열, 데이터의 타입이 일정할 수록 최적화 유리
- Holey Elements : 누락된 인덱스를 가지거나 <empty slot>이 존재하는 경우

```js
const packed = [1, 2, 3]; // Fast
const holey = [1, , 3];   // Slower
```

따라서 배열 중간에 `delete arr[1]` 또는 `arr[100] = 5`처럼 인덱스를 건너뛰면 V8은 해당 배열을 느린 구조로 취급하는 것입니다.

<span class="impact">배열 성능을 떨어뜨리는 흔한 실수들</span>

[ 비연속 인덱스 ]

배열을 초기화할 땐 모든 슬롯을 채우는 것이 좋습니다. 배열이 비어있으면  <3 empty items> 처럼 **Sparse Array(구멍 있는 배열)**로 인식되어 엔진 최적화가 해제됩니다.

```js
const arr = [];
arr[100] = 'a'; // 0~99까지는 hole이 생김
```

[ 타입 혼합 ]

V8 엔진은 배열이 같은 타입의 요소들로 구성되어 있으면 Packed Array로 최적화 하지만 숫자, 문자열, 객체 등 타입이 섞이면 성능 저하가 생기기때문에 배열 요소는 동일한 타입으로 유지하는 게 좋습니다.

```js
const arr = [1, 2, 3];
arr.push('four'); // 배열 내부 타입이 혼합됨 number|string
```

[ delete 사용 ]
```js
delete arr[1]; // arr[1] empty Hole 발생
```


## **3. 기존 조작 메서드**

> 배열을 조작해보자

배열을 만들기만 한다면 공부할 필요도 없겠죠. 기본적인 조작 메서드들 명확하게 정리했습니다.

### 기본 조작 메서드

기본적으로 배열의 양 끝에 요소를 추가하거나 제거하는 기본적인 메서드가 있습니다. 아래 네 가지 메서드는 원본 배열을 직접 변경합니다.

[ push ]

배열의 마지막에 하나 이상의 요소를 추가하고, 변경된 배열의 `length`를 반환합니다. 원본 배열을 직접 변경합니다.

```js
const arr = [1, 2];
arr.push(3);
console.log(arr);   // [1, 2, 3]
arr.push(4, 5);     // 여러 요소 추가 가능
console.log(arr);   // [1, 2, 3, 4, 5]
```

[ pop ]

배열의 마지막 요소를 제거하고 그 요소를 반환합니다. 배열이 비어 있으면 `undefined`를 반환합니다.

```js
const arr = [1, 2, 3];
const lastElement = arr.pop(); 
console.log(lastElement);   // 3
console.log(arr);           // [1, 2]
```

[ unshift ]

배열의 맨 앞에 하나 이상의 요소를 추가하고, 변경된 배열의 `length`를 반환합니다.

```js
const arr = [1, 2];
arr.unshift(0);
console.log(arr);    // [0, 1, 2]
arr.unshift(-2, -1); // 여러 요소 추가 가능
console.log(arr);    // [-2, -1, 0, 1, 2]
```

[ shift ]

배열의 첫 번째 요소를 제거하고 그 요소를 반환합니다. 배열이 비어 있으면 `undefined`를 반환합니다.

```js
const arr = [0, 1, 2];
const firstElement = arr.shift();
console.log(firstElement);  // 0
console.log(arr);           // [1, 2]
```

<span class="impact">기본 조작 메서드의 시간복잡도</span>

배열은 내부적으로 인덱스 기반 구조라, unshift 또는 shift를 사용하여 첫 요소를 지우면 나머지 모든 요소들의 인덱스를 하나씩 당겨야 합니다. 이게 O(n) 시간복잡도를 만들어서 데이터가 많을 때 눈에 띄게 느려집니다. 반대로 push/pop은 끝에서만 다루니까 인덱스 이동이 없어서 O(1)에 가깝게 처리됩니다.


### 배열의 길이

`length` 속성은 배열의 요소 개수를 나타냅니다. 이 속성을 직접 조작하여 배열의 크기를 변경할 수도 있습니다.

```js
const arr = [1, 2, 3, 4];

arr.length = 2; 
console.log(arr);       // [1, 2]

arr.length = 5; 
console.log(arr);       // [1, 2, <3 empty items>]
console.log(arr[3]);    // undefined (empty item에 접근하면 undefined)

arr.push(undefined)     // [1, 2, <3 empty items>,undefined]

arr[3] === arr[5]       // true

const mapped = arr.map((v, i) => i);  // [0, 1, 2, <empty × 2>, 5]
```

배열의 length를 줄이면 뒤에서부터 요소가 제거되어 배열이 잘립니다. 반대로 length를 늘리게되면 추가된 공간은 **empty items**으로 채워집니다. 이 empty items는 실제 undefined 값과는 다릅니다. 둘다 존재하지 않는 값으로 값이 같아 보이지만 map, forEach 같은 배열 메서드도 동작이 달라져서 주의해야합니다. empty slot은 아예 순회 대상에서 건너뛰지만, undefined는 “존재하는 값”으로 취급돼서 콜백이 실행됩니다.

배열의 `at` 메서드는 지정된 인덱스의 요소를 반환하며, 음수 인덱스를 사용하여 배열의 끝에서부터 접근할 수 있습니다. arr[arr.length - 1] 대신 사용 가능하며 가독성과 안정성이 좋아집니다.

```js
const arr = [10, 20, 30];
arr.at(-1); // 30
arr.at(0);  // 10
```

### 배열 초기화

특정 패턴이나 값으로 배열을 초기화하고 싶을 때, 주의할 점을 정리했습니다.

```js
const initArray = Array.from({ length: 5 }, (_, i) => i + 1);
console.log(initArray);  // [1, 2, 3, 4, 5]

const b = new Array(10); // 길이 10을 가진 빈 배열 (10개의 <empty items>)
console.log(b);          // [ <10 empty items> ]

const filled = new Array(3).fill(0);
console.log(filled);     // [0, 0, 0]
```

<span class="impact">Object에게 무시무시한 fill</span>

fill 메서드에 **객체와 같은 참조 타입**의 값을 전달하면, 배열의 모든 요소가 **동일한 객체를 참조**하게 됩니다. 예상치 못한 버그로 이어지기 딱 좋습니다.

```js
const arr = new Array(3).fill({}); 

arr[0].name = 'a'; 
console.log(arr); // [ {name: 'a'}, {name: 'a'}, {name: 'a'} ]
```

이러한 문제를 피하려면, `Array.from()`과 매핑 함수를 사용하여 각 요소마다 새로운 객체를 생성하는 것이 안전합니다.

```js
const arr = Array.from({ length: 3 }, () => ({})); 

arr[0].name = 'a';
console.log(arr); // [ {name: 'a'}, {}, {} ]
```


<span class="impact">배열 생성과 조작, 제대로 알아야 실수를 줄인다</span>

자바스크립트에서 배열을 만드는 방법은 다양하며, 각각의 미묘한 차이점을 이해하는 것이 중요합니다. 특히 빈 배열의 생성 방식, 타입 혼합 문제는 개발자들이 의외로 실수하기 쉬운 부분입니다.

## **4. 순회와 조건 메서드**

자바스크립트에는 배열 순회와 조건 메서드가 내장되어있습니다. 비슷해 보여도 실제 동작 방식과 목적은 확연히 다릅니다. 각 특징을 잘 알아두고 있어야 필요할 때 알맞은 메서드를 잘 사용할 수 있겠죠! 자바스크립트 배열 순회 메서드들의 정확한 쓰임새를 코드 예제와 함께 정리했습니다.

### 배열 순회 메서드

각 원소를 돌면서 무언가 처리하는 메서드, break나 return을 무시하기 때문에 루프를 종료할 수 업습니다.

[ forEach ]

배열의 각 요소에 대해 주어진 함수를 실행합니다.<br>
return undefined

```javascript
const arr = [1, 2, 3];
arr.forEach((num) => console.log(num * 2));
```

[ map ]


각 요소를 콜백의 결과로 매핑하여 새 배열을 생성합니다.<br>
return Array (변환된 새 배열)

```javascript
const arr = [1, 2, 3];
const doubled = arr.map((num) => num * 2); // [2, 4, 6]
```

[ filter ]


콜백 조건이 true인 요소만 남겨 새 배열을 생성합니다.<br>
return Array (조건을 만족하는 요소들의 배열)

```javascript
const arr = [1, 2, 3, 4];
const even = arr.filter((num) => num % 2 === 0); // [2, 4]
```

[ reduce ]

배열을 순회하면서 누적 결과를 계산합니다.<br>
return Any (최종 누적값)

```javascript
const arr = [1, 2, 3, 4];
const sum = arr.reduce((acc, cur) => acc + cur, 0); // 10
```

[ reduceRight ]

`reduce`와 동일하지만, 배열을 오른쪽에서 왼쪽으로 순회합니다.<br>
return Any (최종 누적값)

```javascript
const arr = ["a", "b", "c"];
const result = arr.reduceRight((acc, cur) => acc + cur, ""); // "cba"
```


[ flatMap ]

각 요소를 매핑한 후, 결과를 1단계 평탄화(flat)합니다.<br>
return Array

```javascript
const arr = [1, 2, 3];
const result = arr.flatMap((num) => [num, num * 2]); 
// [1, 2, 2, 4, 3, 6]
```


### 배열 조건 메서드

배열 원소 중 특정 조건을 만족하는지 검사하는 메서드, 각 조건을 만족하면 즉시 종료됩니다.

[ every ]

모든 요소가 콜백 조건을 만족하는지 검사합니다.<br>
return Boolean

```javascript
const arr = [2, 4, 6];
const allEven = arr.every((num) => num % 2 === 0); // true
```

[ some ]

하나라도 콜백 조건을 만족하는 요소가 있는지 검사합니다.<br>
return Boolean

```javascript
const arr = [1, 3, 5, 6];
const hasEven = arr.some((num) => num % 2 === 0); // true
```

[ includes ]

특정 값이 배열에 존재하는지 검사합니다.<br>
return Boolean

```javascript
const arr = ["apple", "banana", "cherry"];
console.log(arr.includes("banana")); // true
```


[ find ]

콜백 조건을 만족하는 **첫 번째 요소 값**을 반환합니다.<br>
return Value (없을 때 undefined)

```javascript
const arr = [5, 12, 8, 130, 44];
const found = arr.find((num) => num > 10); // 12
```


[ findIndex ]

콜백 조건을 만족하는 **첫 번째 요소 인덱스**를 반환합니다.<br>
return Number (없을 때 -1)

```javascript
const arr = [5, 12, 8, 130, 44];
const index = arr.findIndex((num) => num > 10); // 1
```

### for 루프 성능 ♻️
for (let i = 0; i < arr.length; i++) {
  // 고성능 반복 처리
}

for 루프는 break를 사용하여 반복을 중단할 수 있으며, 조건 제어가 용이합니다. 특정 상황에서는 대량의 데이터를 처리할 때 forEach와 같은 메서드보다 **성능상의 이점을 가질 수 있습니다**.

**forEach vs map**

| 항목 | forEach | map |
|---|---|---|
| 반환값 | 없음 | 새 배열 |
| 목적 | 부수 효과 실행 (side effect) | 변환 (transformation) |
| 중단 | 불가 | 불가 |

 API 호출, 콘솔 로그, DOM 조작 등 부수 효과를 위한 작업에는 **forEach**, 데이터 구조 변경이나 특정 형식으로의 변환에는 **map**이 적절합니다.

map, filter, find, some, every와 같은 메서드들은 원본 배열을 변경하지 않고 새로운 결과를 만들어냅니다!

### 목적에 맞는 순회 메서드 선택 
forEach, map, filter를 혼용하며 예상치 못한 오류를 겪곤 합니다. 이는 각 메서드의 반환값과 설계 목적이 명확히 다르기 때문입니다. 메서드의 목적에 맞게 정확하게 사용하면 코드는 더욱 간결하고 명확해지며, 버그 발생 가능성도 줄어듭니다. 배열을 능숙하게 다루고 싶다면, 오늘 배운 순회 메서드들을 확실히 이해하고 넘어가는 것이 중요합니다.

배열을 자유자재로 다루고 싶다면, 순회 메서드는 반드시 이해하고 넘어가야 합니다.

<span class="impact">forEach, map 보다는 for 루프 직접 순회</span>

forEach와 map은 선언적으로 깔끔하지만, 수천 건 이상을 순회하는 경우엔 for문이 더 유리합니다. forEach와 map은 내부적으로 callback function을 매번 호출하는 과정이 반복됩니다.

다음 코드 실행으로 속도 차이를 확인해볼 수 있습니다.

```js
const arr = Array.from({ length: 1000000 }, (_, i) => i);

// for 루프
console.time('for');
let sum1 = 0;
for (let i = 0; i < arr.length; i++) {
  sum1 += arr[i];
}
console.timeEnd('for');

// forEach
console.time('forEach');
let sum2 = 0;
arr.forEach(v => sum2 += v);
console.timeEnd('forEach');

// map 
console.time('map');
let sum3 = 0;
arr.map(v => sum3 += v);
console.timeEnd('map');

/** log 결과
for: 3.514892578125 ms
forEach: 8.708984375 ms
map: 18.7568359375 ms
 */
```

그렇다고 실제로 코딩할 때 무조건 for문만 사용하라는 것은 아닙니다. 가독성과 성능을 고려해서 때에 맞는 코드를 만들어 봅시다.

## 5. 정렬과 구조 변형 메서드


배열을 자르거나, 정렬하거나, 평탄화할 때 원본 배열 변경 여부는 매우매우 * 1000 중요합니다. 제가 자바스크립트 어레이에 대해 정리하고, 알아보고 싶었던 계기이기도 합니다. 자바스크립트를 사용한다면 가장 많이 사용하고 활용하는 Array 관련 메서드들의 특징과 사용법은 충분히 알고 있어야 됩니다.

의도치 않은 원본 변경으로 디버깅에 엄청 고생했던 기억이 새록새록 😅

이번에는 배열의 **구조를 바꾸는 주요 메서드들**을 정리하고, **원본 변경 여부**, **성능**, **주의사항**을 꼼꼼히 정리해 보겠습니다.

[ sort ]

- 배열을 정렬하며, 기본적으로 문자열 기준으로 정렬하므로 숫자 정렬 시 비교 함수가 필요합니다.

 * 기본 정렬은 문자열 기준 (Unicode code)
 * 숫자 정렬 시 반드시 비교 함수를 제공해야 함

⭕️ 원본 배열을 변경

```javascript 
const arr = [10, 2, 30];
arr.sort(); // [10, 2, 30] → ['10', '2', '30'] → 정렬 이상함!

arr.sort((a, b) => a - b); // [2, 10, 30]
```

[ reverse ]

- 배열의 순서를 반대로 뒤집습니다.

⭕️ 원본 배열을 변경

```javascript 
const arr = [1, 2, 3];
arr.reverse(); // [3, 2, 1]
```


[ slice ]

- 배열의 일부를 추출하여 새로운 배열로 반환합니다.

 * 시작 인덱스 포함, 끝 인덱스는 제외
 * 음수 인덱스 사용 가능: slice(-2) → 끝에서 2개
 
☑️ 원본 배열 유지

```javascript 
const arr = [1, 2, 3, 4];
const part = arr.slice(1, 3); // [2, 3]
```


[ splice ]

- 배열의 일부를 삭제하거나 추가합니다.

 * 첫 번째 인자: 시작 인덱스
 * 두 번째 인자: 삭제할 개수
 * 세 번째 이후: 삽입할 요소들

⭕️ 원본 배열을 변경

```javascript 
const arr = [1, 2, 3, 4];
const removed = arr.splice(1, 2); // [2, 3], arr → [1, 4]

arr.splice(1, 0, 'a'); // [1, 'a', 4]
```

[ concat ]

- 여러 배열이나 값을 병합하여 새로운 배열을 반환합니다.


 * 여러 배열/값을 이어 붙일 수 있음


☑️ 원본 배열 유지

```javascript 
const a = [1, 2];
const b = [3, 4];
const c = a.concat(b); // [1, 2, 3, 4]
```

[ flat ]

-  중첩된 배열을 지정한 깊이까지 평탄화하여 새로운 배열을 반환합니다.

 * 기본 depth는 1
 * Infinity를 주면 모든 깊이를 평탄화

☑️ 원본 배열 유지


```javascript 
const arr = [1, [2, [3]]];
arr.flat(); // [1, 2, [3]]
arr.flat(2); // [1, 2, 3]
```

[ flatMap ]

- map을 수행한 후 그 결과를 1단계 평탄화한 새로운 배열을 반환합니다.

* map().flat(1)과 같지만 더 효율적이고 많이 사용

☑️ 원본 배열 유지

```javascript 
const arr = [1, 2, 3];
const result = arr.flatMap(x => [x, x * 2]);
// [1, 2, 2, 4, 3, 6]

```

### 원본 변경 여부 정리

| 메서드 | 원본 변경 여부 | 설명 |
|---|---|---|
| sort() | O | 기본 문자열 정렬, 숫자 정렬 시 compare 필요 |
| reverse() | O | 배열 순서 뒤집기 |
| slice() | X | 일부 추출, 새 배열 반환 |
| splice() | O | 일부 제거/추가 |
| concat() | X | 배열 병합, 새 배열 반환 |
| flat() | X | 중첩 배열 평탄화 |
| flatMap() | X | map + flat(1) |




### 배열의 참조와 복사

자바스크립트에서 배열을 다룰 때 가장 흔하게 헷갈리는 부분이 **참조(reference)** 와 **복사(copy)** 개념입니다. 배열은 객체(Object)와 같은 참조 타입이기 때문에, 단순히 다른 변수에 할당한다고 해서 새로운 배열이 만들어지지 않습니다.

[ 참조 공유 (Assignment) ]

배열을 다른 변수에 그대로 할당하면, 실제 배열의 복사본이 만들어지는 것이 아니라 **동일한 배열을 가리키는 참조**가 전달됩니다.

```js
const original = [1, 2, 3];
const copy = original;

copy[0] = 99;
console.log(original);    // [99, 2, 3]
```

이 경우는 "복사"가 아니라 **같은 배열을 공유**하는 것뿐입니다.

[ 얕은 복사 (Shallow Copy) ]

원본 배열과는 **다른 배열 객체**를 새로 생성하지만, 내부에 있는 참조 타입(객체, 배열 등)은 여전히 같은 메모리를 가리킵니다.

```js
const original = [1, 2, 3, { name: '객체' }];

// 1. 스프레드 연산자
const cloned = [...original];
cloned[0] = 99;
console.log(original); // [1, 2, 3, { name: '객체' }];

cloned[3].name = '변경됨';
console.log(original); // [1, 2, 3, { name: '변경됨' }];

// 2. slice()
const sliced = original.slice();
sliced[0] = 77;
console.log(original); // [1, 2, 3, { name: '객체' }];
```

얕은 복사는 배열 자체는 새로 생성되지만, 내부 요소가 **참조 타입**일 경우 그 참조는 그대로 복사됩니다.

[ 깊은 복사 (Deep Copy) ]

배열 내부에 있는 참조 타입 요소들까지 완전히 새로운 객체로 복제하는 방식입니다.

간단하게 JSON.parse(JSON.stringify(obj)) 를 사용할 수 있지만 `Date`, `Map`, `Set`, 함수, `undefined`, 순환 참조 등은 제대로 복사되지 않습니다.

최신 브라우저/Node.js에서는 더 안전하고 편리한 `structuredClone()`을 사용할 수 있습니다.

```js
const original = [{ a: 1 }, { b: 2 }];

const deep = structuredClone(original);
deep[0].a = 99;

console.log(original[0].a); // 1 (완전히 분리됨)
```

structuredClone도 여전히 복사할 수 없는 타입들이 있어서 유의해야합니다.

### Non-destructive 메서드

ES2023에서는 원본 배열을 변경하지 않으면서 정렬, 뒤집기, 특정 요소 교체를 수행하는 새로운 메서드들이 추가되었습니다. 🎊 이들은 기존의 sort(), reverse(), splice()와 기능은 유사하지만 항상 새로운 배열을 반환하여 불변성을 유지하는 데 도움이 됩니다.


[ toReversed ]
- 배열의 순서를 뒤집은 새로운 배열을 반환합니다. 원본 배열은 변경되지 않습니다.

```javascript 
const arr = [1, 2, 3];
const reversedArr = arr.toReversed(); // [3, 2, 1]
console.log(arr);       // [1, 2, 3] (원본 유지)
``` 

[ toSorted ]
- 배열을 정렬한 새로운 배열을 반환합니다. sort()와 동일하게 비교 함수를 인자로 받을 수 있으며, 원본 배열은 변경되지 않습니다.

```javascript 
const arr = [10, 2, 30];
const sortedArr = arr.toSorted((a, b) => a - b); // [2, 10, 30]
console.log(arr);      // [10, 2, 30] (원본 유지)
``` 

[ toSpliced ]
- splice()와 동일한 인자를 받아 배열의 일부를 삭제하거나 추가한 새로운 배열을 반환합니다. 원본 배열은 변경되지 않습니다.

```javascript 
const arr = [1, 2, 3, 4];
const splicedArr1 = arr.toSpliced(1, 2); // [1, 4]
console.log(arr);         // [1, 2, 3, 4] (원본 유지)

const splicedArr2 = arr.toSpliced(1, 0, 'a'); // [1, 'a', 2, 3, 4]
console.log(arr);         // [1, 2, 3, 4] (원본 유지)
``` 

[ toString ]
toString(): 배열의 모든 요소를 쉼표로 연결한 단일 문자열로 변환하여 반환합니다. 원본 배열은 변경되지 않습니다.

```javascript 
const arr = [1, 2, 3];
const str = arr.toString(); // "1,2,3"
console.log(arr); // [1, 2, 3] (원본 유지)
``` 


<span class="impact">배열 사용시 가장 많은 오류는 '의도치 않은 원본 변경'에서 시작</span>

배열을 정렬하고 자르고 붙이는 작업은 실무에서 자주 발생합니다. 하지만 원본을 변경하는 메서드를 무심코 사용하면, 불변성이 중요한 상황에서는 큰 문제가 될 수 있습니다. 이번 편을 통해 어떤 메서드가 원본을 유지하고, 어떤 메서드가 **파괴적(mutative)**인지를 확실히 이해했다면, 실수 없는 배열 조작이 가능해질 것입니다.



## 6
<span class="impact">목적에 맞는 배열 검색 도구 선택 🔎</span>

배열 검색 시에는 필요한 정보가 값인지, 인덱스인지, 단순 존재 여부인지에 따라 적절한 메서드를 선택하는 것이 중요합니다. 올바른 도구 선택은 더 깔끔하고 효율적인 코드를 만드는 데 도움이 됩니다.

검색은 정확하고 빠르게, 정보는 읽기 좋게 정리하는 것이 배열 마스터의 기본입니다. 💯



## 7. 배열의 자료구조 활용

> 배열, 단순 리스트 넘어 자료구조

배열은 단순한 리스트 이상의 역할을 하며, 큐, 스택, 심지어 행렬 같은 다차원 배열까지 표현할 수 있습니다. 자바스크립트 배열을 자료구조처럼 활용하는 예제들을 정리했습니다.


[ 다차원 배열 ]

행(row)과 열(column)로 구성된 2차원 배열을 살펴보고, 중첩 루프를 통해 순회하는 방법을 알아봅니다.

```js
const matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
];

console.log(matrix[1][2]); // 6
```

행(row)과 열(column)로 구성되어 중첩 루프를 통해 순회 가능합니다.

```js
for (let row of matrix) {
  for (let value of row) {
    console.log(value);
  }
}
```

[ 큐 (Queue) ]

`push()`로 요소를 넣고 `shift()`로 꺼내는 FIFO (First In First Out) 구조를 배열로 구현합니다.

- `push()`로 넣고 `shift()`로 꺼냄
- **입력은 뒤, 출력은 앞**
```js
const queue = [];

queue.push(1); // enqueue
queue.push(2);
console.log(queue.shift()); // dequeue → 1
console.log(queue.shift()); // 2
```



[ 스택 (Stack) ]

`push()`로 요소를 넣고 `pop()`으로 꺼내는 LIFO (Last In First Out) 구조를 배열로 구현합니다.

```js
const stack = [];

stack.push(1);
stack.push(2);
console.log(stack.pop()); // 2
console.log(stack.pop()); // 1
```


### 배열 활용 알고리즘

[ 괄호 짝 검사 ]

스택을 활용할 수 있습니다.

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


[ 2차원 배열 회전 ]

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


[ 중복 제거 ]

```js
const arr = [1, 2, 2, 3, 4, 4];
const unique = [...new Set(arr)];
console.log(unique); // [1, 2, 3, 4]
```

Set과 배열을 결합하면 빠르고 깔끔하게 중복제거를 할 수 있어서 자주 사용하게 됩니다!


배열은 단순한 값 목록을 넘어 **큐, 스택, 트리, 그래프 구현까지** 다양한 자료구조를 표현하는 데 활용될 수 있습니다. 배열 메서드에 익숙해졌다면 이제 **구조적 활용**에 익숙해질 차례입니다. 알고리즘 문제 해결 능력 향상을 위해서도 배열을 자유자재로 다루는 것은 필수적입니다.

## 마무리

단순한 Array 함수는 맨날 사용해도 헷갈려서 검색하고 또 까먹고 이런 일이 반복되었었는데, 자바스크립트 언어를 사용하는 이상 오늘 정리한 내용은 꼭 기억하고 싶어서 정리를 해보았습니다. 각 원리와 특징을 알고 짧은 코드를 작성하는 데도 의미를 둘 수 있는 개발자를 향해 나아가봅시다. ✨