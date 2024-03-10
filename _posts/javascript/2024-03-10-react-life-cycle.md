---
layout: post
title: 리액트 렌더링 과정과 함수형 컴포넌트 Lifecycle
summary: 리액트 렌더링 과정과 생명주기(브라우저 렌더링을 곁들인)
date: 2024-03-10 09:41:33 +09:00
categories: javascript
tags: frontend react
---

리액트로 개발을 하다 보니 “기능 동작은 하는데 왜 이런 현상이 발생하지?”라는 생각이 드는 부분이 많았습니다.
프로젝트의 기능 개발을 대부분 완료하고 테스트를 진행하던 중, 예상보다 잦은 렌더링과 첫 화면 깜빡임 같은 성능 관련 이슈들이 눈에 띄었습니다.

그중에서도 가장 근본적인 질문은 “리액트는 화면을 언제, 어떤 순서로 그리는 걸까?” 였습니다.

리액트의 렌더링 흐름을 중심으로 내부 동작과 useEffect, useLayoutEffect 같은 Hook이 언제 실행되고 언제 정리되는지, 컴포넌트가 mount · update · unmount 되는 흐름을 살펴보려 합니다.


## 왜 첫 화면이 깜빡일까?

처음에는 단순히 네트워크 지연 문제라고 생각했습니다. API 응답이 늦으면 화면이 늦게 뜨는 것이라고 생각하고 기능 개발에만 신경을 썼었죠. 하지만 자세히 관찰해 보니, 네트워크와 무관하게 발생하는 깜빡임이 있었습니다.

로딩 스피너가 잠깐 나타났다가 사라지는 경우, 조건부 렌더링이 많은 화면에서 초기 UI가 바뀌는 경우, 포커스나 레이아웃이 한 박자 늦게 잡히는 경우

이런 현상은 데이터가 늦게 오는 문제라기보다 렌더링 타이밍 문제라는 생각이 들었습니다.

> 리액트는 화면을 어떤 순서로 그리고 있을까?

이 문제를 이해하기위해 컴포넌트가 언제 mount되고, 언제 unmount되며, 그 사이에 어떤 코드가 실행되는지를 렌더링 단계별로 나눠서 정리를 했습니다.

## 브라우저가 화면을 그리는 순서

사용자가 브라우저에 URL을 입력하면, 다음과 같은 과정이 시작됩니다.

브라우저가 URL을 파싱하고 DNS 조회로 서버 IP 확인 후 TCP / TLS 연결 수립합니다. 연결 확립 후 서버에 HTTP 요청 전송, 서버에서는 HTML 응답을 반환합니다. HTML 응답을 받은 시점부터 브라우저 렌더링 단계가 시작됩니다.

브라우저는 응답 받은 HTML을 파싱해 DOM Tree를 생성, CSS 다운로드 및 파싱 후 CSSOM 생성. 이렇게 생성 된 DOM과 CSSOM을 합쳐 Render Tree를 생성합니다.

HTML을 파싱하던 중 `<script>` 태그를 만나면, 브라우저는 HTML 파싱을 잠시 중단하고 JavaScript를 처리합니다. 스크립트를 다운로드하고 실행하며 DOM을 직접 조작할 수도 있습니다. 스크립트 실행이 끝난 뒤 HTML 파싱이 재개됩니다.

이 지점에서 **React 번들이 다운로드되고 실행**됩니다.

## React 초기화

JavaScript 로딩이 완료되면 React 애플리케이션이 초기화됩니다. 대상 DOM 노드와 함께 createRoot를 호출한 다음 해당 컴포넌트로 render 메서드를 호출하면 이 시점부터 React의 렌더링 사이클이 시작됩니다.
```ts
const root = createRoot(document.getElementById('root'))
root.render(<App />)
```

리액트에서 렌더링은 **브라우저가 실제로 화면에 그리는 것**과 정확히 같은 의미는 아닙니다.

리액트의 렌더링은 무엇을 그릴지 계산 하는 `Render Phase`, 계산 결과를 실제 DOM에 반영하는 `Commit Phase` 크게 두 단계로 나뉩니다.
가장 먼저 실행되는 단계는 **Render Phase**입니다.

## Render Phase

Render Phase는 화면을 그리지 않고 **“어떤 UI가 필요한지 계산하는 단계”**입니다.


```jsx
function Example() {
  const [count, setCount] = useState(0)

  return <div>{count}</div>
}
```

이 컴포넌트가 “렌더된다”는 말은 이 함수가 "실행된다"는 의미입니다.

Render Phase에서는 컴포넌트 함수가 하향식으로 실행되며,
실행 과정에서 JSX를 계산하고 Hook을 호출 순서대로 이전 상태와 매칭한 뒤
Virtual DOM(React Element Tree)을 생성합니다.

이 단계에서 Router등 Provider 컴포넌트가 함께 실행되며,
실제 DOM은 전혀 변경되지 않습니다.

Virtual DOM이 생성될 때 리액트는 트리 구조로 상태를 판단하기 때문에 프로그램을 작성할 때 유의할 점이 있습니다.

### 트리 구조로 상태를 판단하는 react

React는 함수 안에 어떤 조건문이 있는지 모르고, 반환된 트리만 알고 있습니다.

React는 컴포넌트 내부 로직을 분석하는 것이 아니라 Render Phase 결과로 만들어진 React Element Tree 구조를 기준으로 이전 렌더와 다음 렌더를 비교합니다.

```jsx
function App({ show }: { show: boolean }) {
  return (
    <div>
      {show ? <Counter /> : <Counter />}
    </div>
  );
}
```

겉보기에는 조건문이 있고, 로직이 갈라진 것처럼 보입니다.
하지만 Render Phase가 끝나고 React가 보는 결과는 항상 같습니다.

```jsx
<div>
  <Counter />
</div>
```

이 두 경우 모두 `<div>`의 첫 번째 자식은 `<Counter />`로  트리 구조상 위치가 동일합니다.

그래서 React는 '이 Counter는 이전 렌더의 Counter와 같은 컴포넌트'라고 판단해서 State가 그대로 유지됩니다.

컴포넌트의 위치가 이전 렌더와 다음 렌더에서 같다면, React는 같은 컴포넌트로 보고 state를 유지합니다. 조건문이 있었는지, 삼항 연산자를 썼는지는 중요하지 않습니다.

```jsx
function App({ show }: { show: boolean }) {
  if (show) {
    return (
      <div>
        <Counter />
      </div>
    );
  }

  return <Counter />;
}
```

이 경우 Render Phase 결과는 다음처럼 바뀝니다.
```jsx
// show === true
<div>
  <Counter />
</div>

// show === false
<Counter />
```

트리 구조 자체가 달라져 React 입장에서는 이전 `<Counter />`를 더 이상 찾을 수 없습니다. 그래서 React는 이전 트리의 `<Counter />`와 state를 제거 후 새로운 `<Counter />`를 생성합니다.

이게 바로 조건부 렌더링에서 state가 초기화되는 이유입니다. 리렌더링 시 state를 유지하고 싶다면 트리 구조가 같아야 합니다. 구조가 같으면 state 유지, 구조가 다르면 unmount되어 state가 제거됩니다. Hook, Router, Suspense 전부 동일하게 적용됩니다.

이 원리를 이해하면 조건부 렌더링에서 input 값이 초기화되거나 라우트 전환 시 컴포넌트 state가 유지되거나 사라짐, key를 잘못 주면 state가 꼬이는 것을 방지할 수 있습니다.

결국 React는 Render Phase 단계 에서 “무엇을 그릴지 계산(Render)”하고 그 계산 결과의 구조로 모든 것을 판단한다는 사실을 알 수 있습니다. 이 판단 결과에 따라서 어떤 컴포넌트는 **생성(mount)** 되고, 어떤 컴포넌트는 **유지(update)** 되며, 어떤 컴포넌트는 **트리에서 사라져(unmount)** 정리됩니다.

즉, 흔히 말하는 React의 생명주기는Render Phase에서 만들어진 트리 구조의 변화 결과라고 볼 수 있습니다.

## React 생명주기

React는 매 렌더링마다 이전 트리와 새로운 트리를 비교하고,
그 비교 결과에 따라 컴포넌트를 다음 세 가지 중 하나로 분류합니다.

### Mount (생성)

이전 렌더 트리에 존재하지 않던 컴포넌트가 새 렌더 트리에 처음 등장하면 mount 됩니다.

state 초기화, ref 생성, Effect 등록

```jsx
{show && <Counter />}
```

show가 false → true가 되는 순간,
`<Counter />`는 새로 생성(mount)됩니다.

### Update (유지 및 재계산)

이전 렌더와 다음 렌더에서 같은 위치에 같은 컴포넌트가 유지되면 update 됩니다.

컴포넌트 함수 재실행, state 유지, props 변화에 따른 재계산

```jsx
<Counter /> // 트리 구조 유지
```

이 경우 컴포넌트는 새로 만들어지지 않으며, 기존 인스턴스를 유지한 채 다시 렌더링됩니다.

### Unmount (제거)

이전 렌더 트리에 존재하던 컴포넌트가 다음 렌더 트리에서 사라지면 unmount 됩니다.

state 제거, ref 해제, Effect cleanup 실행

```jsx
{show ? <Counter /> : null}
```

true -> false가 되면 `<Counter />`는 트리에서 제거되고,
등록되어 있던 effect의 cleanup 함수가 실행됩니다.
```jsx
useEffect(() => {
  const id = setInterval(...)
  return () => clearInterval(id)
}, [])
```

중요한 점은, 이 mount / update / unmount 판단이 Commit Phase에서 이루어지는 것이 아니라 Render Phase에서 결정된다는 것입니다.

Render Phase에서 만들어진 트리 구조가 이전과 같으면? update, 새로 생기면? mount, 사라지면? unmount되는 것입니다.

Commit Phase는 그 판단 결과를 DOM과 Effect 실행으로 반영하는 단계일 뿐입니다.

즉, React의 생명주기는 렌더링 파이프라인 위에서 자연스럽게 만들어지는 결과라고 볼 수 있습니다.

## Commit Phase

Render Phase가 끝나면 **Commit Phase**로 넘어갑니다.

용어 그대로 실제 DOM 변경이 일어나는 단계입니다. render phase에서 만든 가상 트리와 현재 DOM 상태를 비교해서 DOM 노드를 생성하고 속성을 변경하거나 불필요한 노드를 제거합니다. 이 과정에서 더 이상 트리에 존재하지 않는 컴포넌트는 unmount 되며, 컴포넌트의 Effect cleanup 함수가 실행됩니다.

## 브라우저의 Paint
DOM이 실제로 반영된 이후, 브라우저는 다음 작업을 수행합니다.

요소 크기·위치 계산 하는 Layout, 실제 화면 출력하는 Paint / Composite를 거친 후 사용자가 화면을 볼 수 있게 됩니다.

## useLayoutEffect와 useEffect

React에서 mount / unmount 시점에 side effect를 처리할 때 가장 먼저 떠올리는 훅이 useEffect입니다. 하지만 모든 effect를 useEffect로 처리하는 것은 좋지 않습니다.

React에는 서로 다른 타이밍에서 실행되는 두 가지 Effect 훅이 있으며, 이 차이를 이해하지 못하면 FOUC, 레이아웃 틀어짐, 불필요한 paint 지연 같은 문제를 쉽게 만들게 됩니다.

- useEffect 실행 시점

화면이 그려진 이후, 브라우저 paint가 끝난 뒤 실행됩니다.

```ts
useEffect(() => {
  inputRef.current?.focus();
}, []);
```

이 경우 화면이 먼저 보이고, 그 다음 포커스가 잡히면서 깜빡임이 발생할 수 있습니다.

- useLayoutEffect 실행 시점

DOM 반영 직후, paint 직전에 실행됩니다.

```ts
useLayoutEffect(() => {
  inputRef.current?.focus();
}, []);
```

사용자가 화면을 보는 순간에는 이미 포커스가 잡혀 있는 상태가 됩니다. `useLayoutEffect`는 브라우저 페인트를 막기 때문에 어떤 코드를 넣어야할지 신중히 선택해야합니다.


## 마무리

React의 생명주기는 정해진 메서드 호출 순서가 아니라 렌더링 결과에 따라 결정되는 상태 변화였습니다.

컴포넌트는 Render Phase에서 만들어진 트리 구조를 기준으로 mount · update · unmount 여부가 결정되고, Commit Phase에서는 그 판단 결과가 DOM과 Effect 실행으로 반영됩니다.

브라우저의 Layout / Paint와 Effect 실행 타이밍을 함께 놓고 보면, 우리가 흔히 겪는 첫 화면 깜빡임, 포커스 지연, 레이아웃 튐 같은 문제는 데이터 문제가 아니라 타이밍라는 것도 이해할 수 있습니다.

[React의 흐름]

1. **Render Phase** – 계산만 수행
2. **Commit Phase** – DOM 반영
3. **useLayoutEffect** – DOM 커밋 직후, paint를 막고 실행
4. **브라우저 Layout / Paint** – 화면 표시
5. **useEffect** – 보여준 이후 작업

지금까지 저는 “render = paint” 라고 오해하고 있었습니다. 실제로 렌더는 계산이고, DOM 변경은 Commit이며 화면 출력은 브라우저의 역할입니다.

이 흐름을 정확히 이해해두고 FOUC, 불필요한 리렌더링, 라우팅 전환 이슈를 타이밍과 책임의 문제로 바라볼 수 있게 되었습니다.
이제는 컴포넌트가 다시 mount 되고, effect가 두 번 실행되고, 화면이 한 박자 늦게 반영되는 현상들을 막연한 React 특성이 아니라 렌더링 흐름과 생명주기의 결과로 바라볼 수 있게 되었습니다.

렌더링을 계산으로, 생명주기를 결과로 이해하는 것만으로도 React에서 발생하는 많은 UI 문제를 훨씬 예측 가능하게 다룰 수 있습니다.


- <https://ko.react.dev/learn/render-and-commit><br/>
- <https://ko.react.dev/learn/lifecycle-of-reactive-effects><br/>
- <https://web.dev/articles/howbrowserswork?hl=ko#the_main_flow><br/>
- <https://ko.react.dev/learn/preserving-and-resetting-state#same-component-at-the-same-position-preserves-state>