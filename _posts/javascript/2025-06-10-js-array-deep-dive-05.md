---
layout: post
title: "JavaScript Array Deep Dive (5) — 정렬과 구조 변형 메서드 완전 분석"
date: 2025-06-10 22:01:24 +09:00
summary: "자바스크립트 배열 구조 변경 메서드 총 정리"
categories: javascript
tags: javascript Array deepdive 프론트엔드 V8 최적화
---

 
배열을 자르거나, 정렬하거나, 평탄화할 때 원본 배열 변경 여부는 매우 매우 매우 * 1000 중요합니다‼️ 제가 자바스크립트 어레이에 대해 깊게 알아보고 싶었던 계기이기도 합니다. 자바스크립트가 주 언어라면 가장 많이 사용하고 활용하는 Array 관련 메서드들의 특징과 사용법은 충분히 알고 있어야 됩니다.

의도치 않은 원본 변경으로 디버깅에 엄청 고생했던 기억이 새록새록 😅

이번에는 배열의 **구조를 바꾸는 주요 메서드들**을 정리하고, **원본 변경 여부**, **성능**, **주의사항**을 꼼꼼히 정리해 보겠습니다.

## sort

- 배열을 정렬하며, 기본적으로 문자열 기준으로 정렬하므로 숫자 정렬 시 비교 함수가 필요합니다.

 * 기본 정렬은 문자열 기준 (Unicode code)
 * 숫자 정렬 시 반드시 비교 함수를 제공해야 함

⭕️ 원본 배열을 변경

```javascript 
const arr = [10, 2, 30];
arr.sort(); // [10, 2, 30] → ['10', '2', '30'] → 정렬 이상함!

arr.sort((a, b) => a - b); // [2, 10, 30]
```

## reverse

- 배열의 순서를 반대로 뒤집습니다.

⭕️ 원본 배열을 변경

```javascript 
const arr = [1, 2, 3];
arr.reverse(); // [3, 2, 1]
```


## slice

- 배열의 일부를 추출하여 새로운 배열로 반환합니다.

 * 시작 인덱스 포함, 끝 인덱스는 제외
 * 음수 인덱스 사용 가능: slice(-2) → 끝에서 2개
 
☑️ 원본 배열 유지

```javascript 
const arr = [1, 2, 3, 4];
const part = arr.slice(1, 3); // [2, 3]
```


## splice

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


## concat

- 여러 배열이나 값을 병합하여 새로운 배열을 반환합니다.


 * 여러 배열/값을 이어 붙일 수 있음


☑️ 원본 배열 유지

```javascript 
const a = [1, 2];
const b = [3, 4];
const c = a.concat(b); // [1, 2, 3, 4]
```

## flat

-  중첩된 배열을 지정한 깊이까지 평탄화하여 새로운 배열을 반환합니다.

 * 기본 depth는 1
 * Infinity를 주면 모든 깊이를 평탄화

☑️ 원본 배열 유지


```javascript 
const arr = [1, [2, [3]]];
arr.flat(); // [1, 2, [3]]
arr.flat(2); // [1, 2, 3]
```

## flatMap

- map을 수행한 후 그 결과를 1단계 평탄화한 새로운 배열을 반환합니다.

* map().flat(1)과 같지만 더 효율적이고 많이 사용

☑️ 원본 배열 유지

```javascript 
const arr = [1, 2, 3];
const result = arr.flatMap(x => [x, x * 2]);
// [1, 2, 2, 4, 3, 6]

```

## 원본 변경 여부 총 정리 ✏️

| 메서드 | 원본 변경 여부 | 설명 |
|---|---|---|
| sort() | O | 기본 문자열 정렬, 숫자 정렬 시 compare 필요 |
| reverse() | O | 배열 순서 뒤집기 |
| slice() | X | 일부 추출, 새 배열 반환 |
| splice() | O | 일부 제거/추가 |
| concat() | X | 배열 병합, 새 배열 반환 |
| flat() | X | 중첩 배열 평탄화 |
| flatMap() | X | map + flat(1) |


## Non-destructive 변경 메서드 (ES2023)

ES2023에서는 원본 배열을 변경하지 않으면서 정렬, 뒤집기, 특정 요소 교체를 수행하는 새로운 메서드들이 추가되었습니다. 🎊 이들은 기존의 sort(), reverse(), splice()와 기능은 유사하지만 항상 새로운 배열을 반환하여 불변성을 유지하는 데 도움이 됩니다. ~~정말 세상 좋아졌어요 😊~~


### toReversed
- 배열의 순서를 뒤집은 새로운 배열을 반환합니다. 원본 배열은 변경되지 않습니다.

```javascript 
const arr = [1, 2, 3];
const reversedArr = arr.toReversed(); // [3, 2, 1]
console.log(arr);       // [1, 2, 3] (원본 유지)
``` 

### toSorted
- 배열을 정렬한 새로운 배열을 반환합니다. sort()와 동일하게 비교 함수를 인자로 받을 수 있으며, 원본 배열은 변경되지 않습니다.

```javascript 
const arr = [10, 2, 30];
const sortedArr = arr.toSorted((a, b) => a - b); // [2, 10, 30]
console.log(arr);      // [10, 2, 30] (원본 유지)
``` 

### toSpliced
- splice()와 동일한 인자를 받아 배열의 일부를 삭제하거나 추가한 새로운 배열을 반환합니다. 원본 배열은 변경되지 않습니다.

```javascript 
const arr = [1, 2, 3, 4];
const splicedArr1 = arr.toSpliced(1, 2); // [1, 4]
console.log(arr);         // [1, 2, 3, 4] (원본 유지)

const splicedArr2 = arr.toSpliced(1, 0, 'a'); // [1, 'a', 2, 3, 4]
console.log(arr);         // [1, 2, 3, 4] (원본 유지)
``` 

9. toString(): 배열을 문자열로 변환
toString(): 배열의 모든 요소를 쉼표로 연결한 단일 문자열로 변환하여 반환합니다. 원본 배열은 변경되지 않습니다.

```javascript 
const arr = [1, 2, 3];
const str = arr.toString(); // "1,2,3"
console.log(arr); // [1, 2, 3] (원본 유지)
``` 


## 성능 🚨

 * 대량의 배열을 다룰 땐 불변성을 유지하는 slice와 concat을 선호
 * splice는 상태 관리에서 위험할 수 있음
 * sort는 매번 정렬되는 방식이므로, 자주 정렬하면 성능 저하
 * 단순 배열 복사에는 **전개 구문 (...)**이 slice()보다 간결하고 성능도 좋음
 * toReversed(), toSorted(), toSpliced() 등 ES2023에 추가된 비파괴적 메서드들은 불변성을 유지해야 하는 최신 개발 환경에서 매우 유용함


## 배열 구조 변경 시 부작용
배열을 정렬하고 자르고 붙이는 작업은 실무에서 자주 발생합니다. 하지만 원본을 변경하는 메서드를 무심코 사용하면, 불변성이 중요한 상황에서는 큰 문제가 될 수 있습니다. 이번 편을 통해 어떤 메서드가 원본을 유지하고, 어떤 메서드가 **파괴적(mutative)**인지를 확실히 이해했다면, 실수 없는 배열 조작이 가능해질 것입니다.


배열을 다룰 때 가장 많은 오류는 '의도치 않은 원본 변경'에서 시작됩니다.
