---
layout: post
title: 자바스크립트 숫자 포맷 (,) 추가하기
date: 2024-05-13 12:20:54 +09:00
categories: javascript
tags: javascript
---

# toLocaleString

```javascript
const number = 1000000000.55555
const format = number.toLocaleString('ko-KR', { maximumFractionDigits: 4 }) //'1,000,000,000.5555'
```
자바스크립트의 toLocaleString() 을 사용하면 간단하게 3자리마다 , (콤마) 를 추가할 수 있습니다. number type 에만 사용 가능하며 string으로 리턴이 됩니다. 소숫점 자릿수 옵션(maximumFractionDigits)을 추가할 수도 있습니다.

# 정규식
```javascript
const num = 123456789
console.log(num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","))
```

<code>\B</code> 문자 존재(시작이 경계가 아닌 부분 찾기)<br>
<code>x(?= y)</code> 'y'가 뒤따라오는 'x'<br>
<code>\d</code> 숫자 문자에 대응 [0-9]<br>
<code>(\d{3})</code> 숫자가 3번 나타나는 부분에 대응되는 것을 기억<br>
<code>(?!\d)</code> 뒤에 더이상 숫자가 없는 경우<br>

3번마다 반복해서 그 지점에 콤마를 추가해주어 숫자 포맷을 작성할 수 있습니다.


정규식은 할 때마다 필요한 것만 찾아서 사용해서 진짜 간단한 것들만 알고 있는데, 자주 사용하는 것들은 한번 제대로 공부를 해보아야겠습니다.

- <https://shape-coding.tistory.com/72>