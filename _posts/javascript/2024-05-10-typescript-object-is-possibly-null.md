---
layout: post
title: Object is possibly 'null' 해결하기
summary: typescript non null assertion operator
date: 2024-05-10 13:39:53 +09:00
categories: typescript javascript
---

```error
Object is possibly 'null'
Object is possibly 'undefined'
```
# 발생 이유
typescript 입장에서 Object가 null|undefined 일 수도 있다고 생각하여 발생하는 오류입니다.

# 해결하기
```typescript
const user = localStorage.getItem("user").split(" ")[0]; //Object is possibly 'null'.
```

## || 사용
논리연산자 (OR) 사용방법입니다. 앞의 값이 참이면 바로 반환, 거짓이면 뒤의 값을 반환합니다.
```typescript
  const storageUser = localStorage.getItem('user')
  const user = storageUser || 'default user'
```

## ?? 사용
nullish 병합 연산자 사용방법입니다. null, undefined 인 경우 뒤에 있는 값으로 반환합니다.
```typescript
  const storageUser = localStorage.getItem('user')
  const user = storageUser ?? 'default user'
```

## as 사용
```typescript
  const storageUser = (localStorage.getItem('user') as string).split(" ")[0];
```

## ? 사용
Optional Chaining(옵셔널 체이닝) <code>?</code> 사용 방법 입니다.

```typescript
  const user = localStorage.getItem("user")?.split(" ")[0];
```

Object 뒤에 <code>?</code>를 붙여서 있으면 실행하라고 알려주는 것입니다. Object 뒤에 ? 를 붙이면 이와 같아집니다.

```typescript
  const user = localStorage.getItem("user") ? localStorage.getItem("user").split(" ")[0] : null
```

## ! 사용
Non-null assertion operator(non-null 단언 연산자) <code>!</code> 사용 방법입니다.

```typescript
  const user = localStorage.getItem("user")!.split(" ")[0];
```

위에서 옵셔널 체이닝을 사용했던 곳에 ! 를 붙여주는 것인데, 앞의 Object가 undefined 또는 null이 아니라고 알리는 것입니다.

