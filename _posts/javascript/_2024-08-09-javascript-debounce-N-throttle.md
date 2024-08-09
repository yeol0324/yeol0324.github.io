---
layout: post
title: Debounce & Throttle
summary: Debounce와 Throttle을 사용하여 event를 줄여보자
date: 2024-08-09 15:11:33 +09:00
categories: javascript
tags: javascript
---

Debounce와 Throttle은 무었일까?

무한 스크롤 작업이나, 인풋 이벤트를 받아야하는 작업을 할 때 들어봤을 수도 있을 겁니다. 이 두 가지 방법은 DOM 이벤트를 기반으로 실행하는 자바스크립트 이벤트를 제어하는 방법입니다.
    
scroll event로 예를 들어보겠습니다.

```javascript
const ScrollBox = forwardRef() =>{

    const handleScroll = (event: React.UIEvent<HTMLElement>) => {
      console.log(event);
    };
   return (
      <div {...props} className={className} ref={ref} onScroll={handleScroll}>
      </div>
    );
}

```
![](/assets/images/2024-08-09/image1.png)
이렇게 조금만 내려도 

throttle 적용

```javascript
    const handleScroll = (event: React.UIEvent<HTMLElement>) => {
      if (throttle) return;
      if (!throttle) {
        setThrottle(true);
        setTimeout(async () => {
          // setPage((page) => page + 1);
          // scrollTop(ev);
          console.log(event);

          setThrottle(false);
        }, 300);
      }
    };
```

![](/assets/images/2024-08-09/image2.png)

차이가 완전히 보이시죠?!

예를 들어, 웹/앱 사용자가 스크롤(scroll wheel), 트랙패드, 스크롤 막대를 드래깅 한다고 가정해 봅니다. 
스크롤을 내리거나, 트랙패드, 스크롤 막대를 드래깅을 하게 되면 수많은 스크롤 이벤트가 발생하게 됩니다. 
매번 스크롤 이벤트에 대한 콜백(callback)이 발생하고 그 콜백이 수행하는 일이 매우 큰 리소스를 잡아먹게 될 것입니다. 
다시 말해, 과도한 이벤트 횟수의 실행으로 이벤트 핸들러가 무거운 계산 및 기타 DOM 조작과 같은 작업을 수없이 많이 수행하는 경우 성능 문제가 발생하고 이는 사용자 경험까지 떨어뜨리게 될 것입니다.