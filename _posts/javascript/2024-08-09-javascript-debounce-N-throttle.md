---
layout: post
title: Debounce & Throttle
summary: Debounce와 Throttle을 사용하여 event를 줄여보자
date: 2024-08-09 15:11:33 +09:00
categories: javascript
tags: javascript
---

<span class="h-yellow">Debounce</span>와 <span class="h-yellow">Throttle</span>은 무엇일까?

스크롤 이벤트나, 인풋 이벤트를 사용할 때 사용해봤거나 한 번 쯤은 들어봤을 겁니다. 자바스크립트에서 디바운스(debounce)와 스로틀(throttle)은 성능 최적화를 위해 자주 사용되는 두 가지 기법입니다. 이 기법들은 사용자가 자주 발생시킬 수 있는 이벤트(예: 스크롤, 마우스 이동, 키보드 입력 등)에 대한 처리를 효율적으로 관리하여 불필요한 리소스 낭비를 줄이는데 도움을 줍니다.


## 자원 낭비 🧨

scroll event로 예를 들어보겠습니다.

```javascript
const ScrollBox = forwardRef() =>{

    const handleScroll = (event: React.UIEvent<HTMLElement>) => {
      console.log(event);
    };

   return (
      <div {...props} className={className} ref={ref} onScroll= {handleScroll}>
      </div>
    );
}

```

<img src="/assets/images/2024-08-09/image1.png" style="width: 50%; margin:0"/>

스크롤을 조금만 내려도 handleScroll 함수가 잔뜩 실행이 되는데요. 지금은 정말 간단한 console.log를 나타내는 함수였지만 복잡한 로직이 들어간 함수가 과도하게 실행이 된다면 성능 문제도 있고 사용자 경험까지 떨어뜨릴 수 있습니다.

이와같이 디바운스와 스로틀은 자바스크립트에서 자주 발생하는 이벤트 처리 문제를 해결하기 위해 등장했습니다. 웹 애플리케이션에서 이벤트는 매우 빈번하게 발생할 수 있습니다. 이 두 기법은 특히 브라우저 성능 최적화와 네트워크 비용 절감을 위해 널리 사용됩니다.

**디바운스(debounce)** 짧은 시간 동안 이벤트가 여러 번 발생하면, 그 중 마지막 이벤트만 처리하도록 하는 방식입니다.
**스로틀(throttle)** 이벤트가 지속적으로 발생하더라도 일정 간격으로만 함수를 실행하도록 제한하는 방식입니다.

## debounce vs throttle
그렇다면 이 두 가지 방법은 언제 어떻게 사용하면 좋을까요? 하나씩 예제를 보며 정리해보겠습니다. ✍️

### 스로틀(Throttle)

스로틀은 이벤트가 지속적으로 발생하더라도 일정한 시간 간격으로만 함수를 실행합니다. 즉, 지정된 시간 동안에는 한 번만 함수를 실행할 수 있으며, 그 시간 간격이 지나면 다시 이벤트를 처리합니다.

먼저 위에서 봤던 예시에 스로틀을 적용해볼까요?

```javascript
const handleScroll = (event: React.UIEvent<HTMLElement>) => {
  if (throttle) return;
  if (!throttle) {
    setThrottle(true);
    setTimeout(async () => {
      setThrottle(false);
    }, 300);
  }
};
```
<img src="/assets/images/2024-08-09/image2.png" style="width: 50%; margin:0"/>

차이가 완전히 보이시죠?!

스로틀은 이처럼 이벤트가 지속적으로 발생하는 동안, 성능을 고려해 주기적으로만 함수를 실행해야 할 때 적합합니다. 대표적으로 스크롤, 윈도우 리사이즈, 마우스 이동 등의 이벤트에 유용합니다.


### 디바운스(Debounce)

디바운스는 일정 시간 동안 이벤트가 반복되면 마지막 이벤트만 처리합니다. 즉, 지정된 시간 내에 다시 이벤트가 발생하면 타이머를 리셋하고, 해당 시간이 지나면 마지막 이벤트를 실행합니다.

디바운스는 방금 전에 본 스크롤 이벤트 보다는 input 에서 사용을 많이 합니다. input에 닉네임 입력이 끝난 후 유요한 닉네임인지 확인하는 로직에서 사용할 수 있습니다. 이때 input 이벤트를 사용하게 되면, 키보드를 한 번 누를 때마다 확인을 하고 오겠죠? 키보드를 입력하고 싶었는데 검사하지 않아도 되는 ㅋ, 키, 킵, 키보, 키볻 하나하나 다 확인을 하게 되는 것입니다. 이처럼 사용자가 검색창에 입력할 때, 연속해서 발생하는 키보드 입력 이벤트에 대해 마지막 입력이 끝난 후 일정 시간 이후에만 검색 API를 호출하는 경우에 사용됩니다.


```javascript
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

const searchInput = document.getElementById('search');
searchInput.addEventListener('input', debounce((event) => {
    // 검색 API 호출
    console.log("API 호출", event.target.value);
}, 300));
```

디바운스는 사용자가 이벤트를 연속적으로 발생시킬 가능성이 높고, 그 중 마지막 이벤트만 처리하는 것이 합리적인 경우에 적합합니다. 대표적으로 입력 폼이나 버튼 클릭 등의 이벤트가 해당됩니다.

## 마무리

스로틀과 디바운스는 이런 상황에 적절하게 사용할 수 있습니다.
- 스로틀 : 무한 스크롤, 스크롤 위치에 따라 애니메이션 트리거, 마우스 이동에 따른 UI 업데이트
- 디바운스 : 자동 저장 기능, 검색창의 실시간 필터링, 윈도우 리사이즈가 끝난 후 레이아웃 재조정

한눈에 봐도 정말 사용할 때가 많은데, 맞습니다. 스로틀과 디바운스는 자바스크립트 사용 시에 정말 자주 사용하는 기능으로 다양한 라이브러리들 ( [lodash](https://github.com/lodash/lodash), [throttle-debounce](https://github.com/niksy/throttle-debounce) )도 존재합니다.



디바운스와 스로틀은 유사해 보이지만 각기 다른 상황에서 유용하게 사용됩니다. 디바운스는 마지막 이벤트만 처리하는 데 적합하고, 스로틀은 지속적인 이벤트를 일정 간격으로 처리하는 데 적합합니다. 두 기법을 적절히 사용해서 성능 최적화와 사용자 경험 개선에 크게 기여하는 웹을 만들어봅시다. 🔥