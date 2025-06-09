---
layout: post
title: "JavaScript Array Deep Dive (4) — 순회와 조건 메서드"
date: 2025-06-09 17:30:24 +09:00
summary: "돌릴 줄 알아야 배열을 쓴다"
categories: javascript
tags: javascript Array deepdive 프론트엔드 V8 최적화
---

자바스크립트 배열의 가장 큰 장점은 값 하나하나를 함수로 순회하면서 다룰 수 있다는 것입니다. 하지만 forEach, map, filter, some... 모두 비슷해 보여도 실제 동작 방식과 목적은 확연히 다릅니다. 이번 포스트에서는 자바스크립트 배열 순회 메서드들의 정확한 쓰임새를 코드 예제와 함께 정리하고, 각 메서드의 반환값, 중단 가능 여부, 성능 유의점까지 함께 살펴보겠습니다.

## forEach(callback)
- 배열의 각 요소에 대해 주어진 함수를 실행합니다.
return undefined (없음)

🛑 중단 불가: forEach 메서드는 break나 return을 무시하기 때문에 루프를 종료할 수 없습니다.

```javascript
const arr = [1, 2, 3];
arr.forEach((num) => console.log(num * 2));
```

## map(callback)
- 각 요소를 콜백의 결과로 매핑하여 새 배열을 생성합니다.
return Array (변환된 새 배열)

🛑 중단 불가: map 메서드는 break나 return을 무시하기 때문에 루프를 종료할 수 없습니다.

```javascript
const arr = [1, 2, 3];
const doubled = arr.map((num) => num * 2); // [2, 4, 6]
```

## filter(callback)
- 콜백 조건이 true인 요소만 남겨 새 배열을 생성합니다.
return Array (조건을 만족하는 요소들의 배열)

🛑 중단 불가: filter 메서드는 break나 return을 무시하기 때문에 루프를 종료할 수 없습니다.

```javascript
const arr = [1, 2, 3, 4];
const even = arr.filter((num) => num % 2 === 0); // [2, 4]
```

## find(callback)
- 콜백 조건을 만족하는 첫 번째 요소만 반환합니다.
return 해당 요소 (없으면 undefined)

🛑 중단 가능: 조건이 만족되면 루프가 종료.

```javascript
const users = [{ id: 1 }, { id: 2 }];
const user = users.find((u) => u.id === 2); // { id: 2 }
```

## some(callback)
- 배열에 하나라도 조건을 만족하는 요소가 있는지 확인하고 true 또는 false를 반환합니다.
return boolean

🛑 중단 가능: 조건이 만족되면 바로 종료.

```javascript
const hasEven = [1, 3, 5].some((num) => num % 2 === 0); // false
``` 

## every(callback)
- 배열의 모든 요소가 조건을 만족하는지 확인하고 true 또는 false를 반환합니다.
return boolean

🛑 중단 가능: 조건이 하나라도 틀리면 즉시 종료.

```javascript
const allPositive = [1, 2, 3].every((num) => num > 0); // true
```

## 비교 정리
| 메서드 | 목적 | 반환값 | 중단 가능 여부 |
|---|---|---|---|
| forEach | 단순 반복 실행 | 없음 | 불가능 |
| map | 변환 | 새 배열 | 불가능 |
| filter | 조건 필터링 | 새 배열 | 불가능 |
| find | 조건 만족 요소 찾기 | 요소 하나 | 가능 |
| some | 일부 조건 만족 여부 | Boolean | 가능 |
| every | 전부 조건 만족 여부 | Boolean | 가능 |

## for 루프 성능 ♻️
for (let i = 0; i < arr.length; i++) {
  // 고성능 반복 처리
}

for 루프는 break를 사용하여 반복을 중단할 수 있으며, 조건 제어가 용이합니다. 특정 상황에서는 대량의 데이터를 처리할 때 forEach와 같은 메서드보다 **성능상의 이점을 가질 수 있습니다**.

## forEach 🆚 map

| 항목 | forEach | map |
|---|---|---|
| 반환값 | 없음 | 새 배열 |
| 목적 | 부수 효과 실행 (side effect) | 변환 (transformation) |
| 중단 | 불가 | 불가 |

 API 호출, 콘솔 로그, DOM 조작 등 부수 효과를 위한 작업에는 **forEach**, 데이터 구조 변경이나 특정 형식으로의 변환에는 **map**이 적절합니다.

map, filter, find, some, every와 같은 메서드들은 원본 배열을 변경하지 않고 새로운 결과를 만들어냅니다!

## 목적에 맞는 순회 메서드 선택 
forEach, map, filter를 혼용하며 예상치 못한 오류를 겪곤 합니다. 이는 각 메서드의 반환값과 설계 목적이 명확히 다르기 때문입니다. 메서드의 목적에 맞게 정확하게 사용하면 코드는 더욱 간결하고 명확해지며, 버그 발생 가능성도 줄어듭니다. 배열을 능숙하게 다루고 싶다면, 오늘 배운 순회 메서드들을 확실히 이해하고 넘어가는 것이 중요합니다.

배열을 자유자재로 다루고 싶다면, 순회 메서드는 반드시 이해하고 넘어가야 합니다.
