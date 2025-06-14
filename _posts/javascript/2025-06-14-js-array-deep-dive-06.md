---
title: "JavaScript Array Deep Dive (6) — 검색과 정보 추출 메서드"
date: 2024-06-14
description: "includes, indexOf, lastIndexOf, find, findIndex, join, at 등 검색 관련 메서드 총정리"
tags: ["JavaScript", "Array", "검색", "includes", "indexOf", "find"]
---

 배열에서 원하는 값 찾기


실무에서 배열을 다룰 때 가장 많이 하는 작업 중 하나는 "값이 있는지 찾기", "어디에 있는지 확인하기", 그리고 "필요한 정보를 변환해서 보여주기" 입니다. 이번 포스트에서는 includes, indexOf, find, at, join 등 검색과 정보 추출에 특화된 배열 메서드들을 총정리하고, 실무에서 어떻게 활용할 수 있는지 살펴봅니다.

## includes

includes(): 배열에 특정 값이 존재하는지 확인하여 true 또는 false를 반환합니다.
const arr = [1, 2, 3];
arr.includes(2); // true
arr.includes(5); // false

 * NaN도 감지 가능 (indexOf는 못함)
 * === 비교 방식

## indexOf


indexOf(): 배열에서 특정 값의 첫 번째 인덱스를 반환하며, 없으면 -1을 반환합니다.
const arr = ['a', 'b', 'c', 'a'];
arr.indexOf('a'); // 0
arr.indexOf('z'); // -1

 * 없으면 -1 반환
 * NaN은 인식하지 못함


## lastIndexOf

lastIndexOf(): 배열에서 특정 값의 마지막 인덱스를 반환합니다.
arr.lastIndexOf('a'); // 3

 * 전체를 뒤에서부터 순회하며 가장 마지막 인덱스를 반환


## find

find(): 주어진 콜백 함수를 만족하는 배열의 첫 번째 요소를 반환합니다.
const users = [{ id: 1 }, { id: 2 }];
const result = users.find((user) => user.id === 2); // { id: 2 }

 * 객체 검색 시 유용
 * 조건을 만족하는 값 자체 반환 (없으면 undefined)
## findIndex

findIndex(): 주어진 콜백 함수를 만족하는 배열의 첫 번째 요소의 인덱스를 반환합니다.
users.findIndex((user) => user.id === 2); // 1

 * find와 달리 인덱스를 반환

## join

join(): 배열의 모든 요소를 지정된 구분자로 연결하여 하나의 문자열로 반환합니다.
const words = ['hello', 'world'];
words.join(' '); // 'hello world'
words.join('-'); // 'hello-world'

 * 구분자를 직접 지정 가능
 * 비어 있는 배열은 빈 문자열 반환


## toString

toString(): 배열의 모든 요소를 쉼표로 연결한 문자열을 반환합니다.
[1, 2, 3].toString(); // '1,2,3'

 * join(',')과 동일한 결과
 * 내부적으로 호출되는 경우 많음 (alert(arr) 등)


## at

at(): 지정된 인덱스의 요소를 반환하며, 음수 인덱스를 사용하여 배열의 끝에서부터 접근할 수 있습니다.
const arr = [10, 20, 30];
arr.at(-1); // 30
arr.at(0);  // 10

 * arr[arr.length - 1] 대신 사용 가능
 * 가독성과 안정성이 좋아짐


## 비교 정리표
| 메서드 | 목적 | 반환값 | 음수 인덱스 지원 | 없음 시 |
|---|---|---|---|---|
| includes | 존재 여부 | Boolean | X | false |
| indexOf | 값의 위치 | index | X | -1 |
| lastIndexOf | 뒤에서 위치 | index | X | -1 |
| find | 조건 만족 값 | 요소 | O (조건 기반) | undefined |
| findIndex | 조건 만족 위치 | index | O | -1 |
| join | 문자열로 결합 | String | N/A | '' |
| at | 안전한 인덱싱 | 요소 | O | undefined |


## 목적에 맞는 배열 검색 도구 선택 🔎

배열 검색 시에는 필요한 정보가 값인지, 인덱스인지, 단순 존재 여부인지에 따라 적절한 메서드를 선택하는 것이 중요합니다. 올바른 도구 선택은 더 깔끔하고 효율적인 코드를 만드는 데 도움이 됩니다.

검색은 정확하고 빠르게, 정보는 읽기 좋게 정리하는 것이 배열 마스터의 기본입니다. 💯
