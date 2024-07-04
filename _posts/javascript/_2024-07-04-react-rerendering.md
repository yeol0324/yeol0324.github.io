---
layout: post
title: 리액트 리렌더링 지옥 탈출
summary: 야호~!
date: 2024-07-03 17:18:02 +09:00
categories: javascript
tags: 
---

https://sangcho.tistory.com/entry/%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8-Re-rendering%EC%9D%84-%ED%94%BC%ED%95%98%EB%8A%94-5%EA%B0%80%EC%A7%80-%EB%B0%A9%EB%B2%95

https://velog.io/@js43o/%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8%EC%9D%98-%EB%B6%88%ED%95%84%EC%9A%94%ED%95%9C-%EB%A6%AC%EB%A0%8C%EB%8D%94%EB%A7%81-%EB%B0%A9%EC%A7%80#2-%EC%BB%B4%ED%8F%AC%EB%84%8C%ED%8A%B8-%EC%B5%9C%EC%A0%81%ED%99%94%EB%A5%BC-%EC%9C%84%ED%95%9C-%EB%8F%84%EA%B5%AC%EC%97%90%EB%8A%94-%ED%81%AC%EA%B2%8C-%EC%84%B8-%EA%B0%80%EC%A7%80%EA%B0%80-%EC%9E%88%EB%8B%A4

https://velog.io/@dae_eun2/React-Re-rendering-%EA%B3%BC-%EC%B5%9C%EC%A0%81%ED%99%94


스크롤을 할 때마다 재렌더링 되는 문제가 있었다
```javascript
"use client";
import { useEffect, useState } from "react";

export const useScroll = (targetRef: React.MutableRefObject<HTMLDivElement | null>) => {
  const ref = targetRef;
  const [state, setState] = useState({
    y: 0,
  });

  useEffect(() => {
    if (typeof window === undefined) return;
    if (!ref.current) return;
    const onScroll = (event: any) => {
      if (!ref.current) return;
      setState({ y: ref.current.scrollTop });
    };
    ref.current?.addEventListener("scroll", onScroll);
    return () => ref.current?.removeEventListener("scroll", onScroll);
  }, [ref.current]);
  return { ref, state };
};
```

ref.current의 의존성 문제:
useEffect 훅에서 ref.current는 초기 렌더링 이후에도 바뀔 수 있으므로 의존성 배열에 ref.current를 직접 넣지 않는 것이 좋습니다. 대신, ref 자체를 의존성 배열에 넣어야 합니다.

스크롤 이벤트 핸들러 최적화:
스크롤 이벤트가 매우 빈번하게 발생하므로, 상태 업데이트를 필요할 때만 수행하는 것이 좋습니다. 스크롤 위치가 변경될 때만 상태를 업데이트하도록 조건을 추가할 수 있습니다.

```javascript
"use client";
import { useEffect, useState } from "react";

export const useScroll = (targetRef: React.MutableRefObject<HTMLDivElement | null>) => {
  const ref = targetRef;
  const [state, setState] = useState({
    y: 0,
  });

  useEffect(() => {
    if (typeof window === 'undefined') return;
    if (!ref.current) return;
    
    const onScroll = () => {
      if (!ref.current) return;
      const newY = ref.current.scrollTop;
      if (state.y == newY) return;
      setState({ y: newY });
    };
    
    ref.current.addEventListener("scroll", onScroll);
    return () => {
      ref.current?.removeEventListener("scroll", onScroll);
    };
  }, [ref]);

  return { ref, state };
};

```