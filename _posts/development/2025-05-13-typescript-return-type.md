---
layout: post
title: TypeScript의 ReturnType
summary: typescript 더 잘 쓰기
date: 2025-05-13 09:41:33 +09:00
categories: development
tags: frontend typescript javascript 
---

{TypreScript의 ReturnType에 관심을 가지게 된 이유 : 도입부}

TypeScript의 `ReturnType<T>`는 **제네릭 유틸리티 타입**입니다. 함수 타입 `T`가 있을 때, 그 함수 리턴값의 타입을 추출해 줍니다. 내부적으로는 조건부 타입과 `infer` 키워드를 써서 동작합니다.

## 기본 정의

타입스크립트에서 ReturnType을 확인해보겠습니다.

```ts
/**
 * Obtain the return type of a function type
 */
type ReturnType<T extends (...args: any) => any> = T extends (...args: any) => infer R ? R : any;
```

여기서 핵심은 `infer R` 부분입니다.

`T`가 함수 타입일 때  `(...args: any) => something`
* 그 `something`을 `R`이라는 이름으로 "추론(infer)"합니다.
* 최종적으로 `R`을 반환합니다.


## Typescript에서의 infer

타입스크립트 infer는 조건부 타입에서 미리 정의되지 않은 타입을 유연하게 정의할 수 있게 도와주는 문법입니다. 항상 조건부 타입 문법과 같이 사용되며 복잡한 타입 코드를 줄여줍니다.
```typescript
const arr= ['유림',26] //이라는 배열이 있을 때,

type El = string|number  // 이렇게한다면 배열의 내용이 바뀔 때마다 재정의를 해야겠죠?
type El<T> = T extends (string|number)[] ? string|number : never
// 이걸 요렇게
type El<T> = T extends (infer E)[] ? E : never

const element:El<typeof arr> = 'hi'
```

## 동작 예시

```ts
function foo() {
  return { id: 1, name: "yurim" };
}

type FooReturn = ReturnType<typeof foo>;
// FooReturn = { id: number; name: string }
```

즉, `typeof foo`가 `() => { id: number; name: string }` 이고, `ReturnType`이 그 함수의 리턴값 타입을 뽑아낸 거죠.

---

## 응용

1. **비동기 함수**

```ts
async function fetchData() {
  return "data";
}

type Data = ReturnType<typeof fetchData>;
// Data = Promise<string>
```

2. **콜백에서 사용**

```ts
type Callback = (x: number) => boolean;
type R = ReturnType<Callback>;
// R = boolean
```

3. **함수 오버로드**

```ts
function test(x: number): number;
function test(x: string): string;
function test(x: any): any {
  return x;
}

type R = ReturnType<typeof test>;
// R = any (오버로드의 최종 구현체 기준)
```

---

## 주의할 점

* `ReturnType`은 함수 타입에만 쓸 수 있습니다.
  그냥 값이나 객체 타입을 넣으면 오류가 납니다.
* 오버로드된 함수는 **구현체의 리턴 타입**만 가져옵니다. (가장 구체적인 오버로드 시그니처들은 무시돼요.)
* `Promise`의 내부 값까지는 풀어주지 않아요. (필요하면 `Awaited<T>`를 같이 씁니다.)

```ts
type Inner = Awaited<ReturnType<typeof fetchData>>;
// Inner = string
```

---

즉, `ReturnType`은 **"이 함수가 뭘 돌려주는지 타입만 뽑아와!"** 하는 간단하지만 강력한 도구예요. 특히 큰 프로젝트에서 함수 시그니처를 여러 곳에서 공유할 때, 직접 리턴 타입을 써 넣는 대신 `ReturnType`을 써서 유지보수를 편하게 하는 데 많이 활용합니다.

INFO: 여기서

좋아. `ReturnType`이랑 `Parameters`를 중심으로, 같이 쓰면 실무에서 유용한 유틸리티들까지 한 번에 정리해줄게. 군더더기 없이 핵심만.

# 1) 기본기

```ts
type ReturnType<T extends (...args: any) => any> =
  T extends (...args: any) => infer R ? R : never;

type Parameters<T extends (...args: any) => any> =
  T extends (...args: infer P) => any ? P : never;
```

* `ReturnType<F>`: 함수 `F`가 **무엇을 반환하는지** 타입만 뽑음.
* `Parameters<F>`: 함수 `F`의 **매개변수 튜플**을 그대로 뽑음.

예시:

```ts
function foo(a: number, b: string) {
  return { id: a, name: b };
}

type R = ReturnType<typeof foo>;      // { id: number; name: string }
type P = Parameters<typeof foo>;      // [a: number, b: string]
```

# 2) 비동기와 함께

`ReturnType`은 프로미스 “껍데기”까지만 줌. 내용물은 `Awaited`로 벗겨라.

```ts
async function fetchUser() { return { id: "u1" } }

type R1 = ReturnType<typeof fetchUser>;            // Promise<{ id: string }>
type R2 = Awaited<ReturnType<typeof fetchUser>>;   // { id: string }
```

# 3) 오버로드 함수 주의점

오버로드가 여러 개여도 **구현체 시그니처의 반환/파라미터**만 가져온다.

```ts
function f(x: number): number;
function f(x: string): string;
function f(x: number | string) { return x }

type RF = ReturnType<typeof f>;   // number | string 아님 → any | unknown 아님 → 실제론 string | number가 아닌, 구현체에 따라 넓어질 수 있음(프로젝트 설정에 따라 any로 보일 수도)
type PF = Parameters<typeof f>;   // [x: number | string]
```

실무 팁: 오버로드에서 정확한 추출이 필요하면, 오버로드 대신 **제네릭 하나**로 표현하거나, 추출용으로 **오버로드별 시그니처 타입**을 따로 정의해 두고 그 타입에 `ReturnType`/`Parameters`를 적용하라.

# 4) `Parameters`로 재사용성 폭발

* **고차 함수 래핑**: 기존 함수의 인자를 그대로 받되, 반환만 바꾸고 싶을 때.

```ts
function wrap<F extends (...args: any[]) => any>(fn: F) {
  return (...args: Parameters<F>): ReturnType<F> {
    return fn(...args);
  }
}
```

* **컨트롤러/서비스 연결**: 서비스 시그니처를 컨트롤러에 그대로 투영.

```ts
type Svc = (id: string, expand?: boolean) => Promise<{ id: string }>;
type Controller = (...args: Parameters<Svc>) => Promise<Response>;
```

# 5) this 관련 유틸과 한 세트로 쓰기

* `ThisParameterType<F>`: 함수의 `this` 타입 추출
* `OmitThisParameter<F>`: `this` 제거한 호출 시그니처

```ts
function g(this: { token: string }, x: number) { return this.token + x }

type TThis = ThisParameterType<typeof g>;   // { token: string }
type GNoThis = OmitThisParameter<typeof g>; // (x: number) => string
```

메서드를 콜백으로 넘길 때 `bind` 없이 타입 안전하게 다루기 좋다.

# 6) 생성자 계열도 있다

* `ConstructorParameters<C>`: 클래스(생성자)의 파라미터 튜플
* `InstanceType<C>`: 생성 결과(인스턴스) 타입

```ts
class User { constructor(public id: string, public age: number) {} }

type CP = ConstructorParameters<typeof User>; // [id: string, age: number]
type IT = InstanceType<typeof User>;         // User
```

# 7) 실무에서 바로 쓰는 레시피

① **API 핸들러 타입 재사용**

```ts
// 실제 구현
export const getMe = async (token: string) => ({ id: "me" as const });

// 타입 노출
export type GetMeArgs = Parameters<typeof getMe>;           // [token: string]
export type GetMeResult = Awaited<ReturnType<typeof getMe>>;// { id: "me" }
```

② **미들웨어로 반환 타입 감싸기**

```ts
function withCache<F extends (...a: any[]) => Promise<any>>(fn: F) {
  return async (...a: Parameters<F>): Promise<ReturnType<F>> => {
    // 캐시 로직...
    return fn(...a); // 그대로 반환
  };
}
```

③ **폼 스키마와 서비스 시그니처 동기화**

```ts
type Submit = (form: { email: string; pwd: string }) => Promise<void>;

type FormValues = Parameters<Submit>[0];  // { email: string; pwd: string }
type SubmitResult = ReturnType<Submit>;   // Promise<void>
```

④ **이벤트 리스너 안전 포워딩**

```ts
type OnChange = (e: React.ChangeEvent<HTMLInputElement>) => void;
function Forward(onChange: OnChange) {
  return (e: Parameters<OnChange>[0]) => onChange(e);
}
```

# 8) `infer`로 커스텀 추출기 만들기

* \*\*Promise 안쪽만



INFO
좋아. 돌려 말 안 하고 바로 쓸모부터.

# 응용 포인트 (핵심 요약)

* **한 소스에서 타입을 “끌어다 쓰기.”** 함수/메서드/생성자 시그니처를 `ReturnType`/`Parameters`로 복제하지 말고 참조.
* **비동기·래핑·미들웨어에 강함.** `Awaited<ReturnType<...>>`, `(...args: Parameters<F>) => ...` 패턴으로 중복 제거.
* **오버로드·콜백·this 바인딩 문제 정돈.** `OmitThisParameter`, `ThisParameterType`와 조합.
* **SDK/레이어 간 계약 고정.** 컨트롤러↔서비스, API 라우터↔클라이언트 양끝을 한 타입 원천으로 묶음.

---

# 실무에서 바로 쓰는 패턴

## 1) API 라우터 ↔ 클라이언트 동기화

서버 핸들러가 타입의 “원천.” 클라이언트는 그걸 참조만.

```ts
// server/handlers/user.ts
export const getMe = async (token: string) => ({ id: "me", name: "Y" } as const);

// shared/types.ts
export type GetMeArgs   = Parameters<typeof getMe>;                 // [token: string]
export type GetMeResult = Awaited<ReturnType<typeof getMe>>;        // { id: "me"; name: "Y" }

// client/api.ts
export const getMeClient = (fetcher: (...a: any[]) => Promise<any>) =>
  async (...args: GetMeArgs): Promise<GetMeResult> =>
    fetcher("/me", { headers: { Authorization: args[0] } });
```

**효과:** 서버가 바뀌면 클라 타입이 자동 추적. “문서-구현-타입” 불일치 제거.

---

## 2) 미들웨어/데코레이터 래핑

캐시/리트라이/로그 등 공통관심사를 감싸도 시그니처 유지.

```ts
function withCache<F extends (...a: any[]) => Promise<any>>(fn: F) {
  return async (...a: Parameters<F>): Promise<ReturnType<F>> => {
    // ...cache
    return fn(...a);
  };
}
```

**포인트:** 인자·반환을 그대로 투명 전달 → 래핑이 타입을 망치지 않음.

---

## 3) React 폼/핸들러 안전 포워딩

RHForm, 이벤트 콜백, 컨트롤러-서비스 연결에서 특히 유용.

```ts
type OnChange = (e: React.ChangeEvent<HTMLInputElement>) => void;

function forwardChange(fn: OnChange) {
  return (e: Parameters<OnChange>[0]) => fn(e);
}
```

```ts
// RHF SubmitHandler<T> = (data: T) => any
type SubmitHandler<T> = (data: T) => unknown;
type FormValues<T extends SubmitHandler<any>> = Parameters<T>[0];

// 예: 서비스 시그니처를 폼 값으로 재사용
type Signup = (form: { email: string; pwd: string }) => Promise<void>;
type SignupFormValues = Parameters<Signup>[0];
```

---

## 4) 오버로드 정리(현실적 해법)

오버로드는 구현체 기준으로만 추출되기 쉬움. 정확한 추출이 필요하면 **제네릭 하나로 합치거나** “추출용 타입”을 별도로 노출.

```ts
// 추출용 타입만 노출
export type F_sig_num = (x: number) => number;
export type F_sig_str = (x: string) => string;

type Rn = ReturnType<F_sig_num>; // number
type Rs = ReturnType<F_sig_str>; // string
```

---

## 5) 생성자와 인스턴스

팩토리/DI 컨테이너에서 유용.

```ts
class User { constructor(public id: string, public age: number) {} }

type UserCtorArgs = ConstructorParameters<typeof User>; // [string, number]
type UserInstance = InstanceType<typeof User>;          // User
```

---

## 6) 액션/커맨드 맵에서 안전하게 선택

Redux/Zustand/커맨드 버스에 좋음.

```ts
const actions = {
  add:   (id: string, qty: number) => ({ type: "add",   id, qty }),
  clear: () => ({ type: "clear" as const }),
};

type AddArgs = Parameters<typeof actions.add>;        // [string, number]
type ClearRet = ReturnType<typeof actions.clear>;     // { type: "clear" }
```

---

# 더 잘 쓰는 요령 (함정 회피)

* **Promise 내부를 써야 한다면 항상 `Awaited<ReturnType<F>>`.**
* **오버로드가 많다면**: “추출 원천”을 **타입 별칭**으로 따로 만들어 거기서 뽑아라.
* **any 전염 주의**: 한 군데 `any`가 있으면 추론이 흐려짐. 가능하면 `unknown` → 좁히기.
* **배열/튜플 정확도**: `Parameters`는 튜플을 그대로 잡아준다. 가변 인자도 튜플로.

---

# 확장 아이디어 (커스텀 유틸리티)

## 1) 비동기 함수의 ‘내부 타입’만 뽑기

```ts
type UnwrapAsyncFn<F extends (...a: any) => any> =
  Awaited<ReturnType<F>>;
```

## 2) 배열/옵셔널/널러블 벗기기

```ts
type UnboxArray<T>   = T extends (infer U)[] ? U : T;
type NonNullableDeep<T> = T extends object
  ? { [K in keyof T]-?: NonNullableDeep<NonNullable<T[K]>> }
  : NonNullable<T>;
```

## 3) 콜백 1번째 인자 타입만 뽑기 (이벤트, 미들웨어에 유용)

```ts
type FirstArg<F extends (...a: any[]) => any> =
  Parameters<F>[0];
```

## 4) 함수 결과에서 특정 키만 고르기

```ts
type PickFromReturn<F extends (...a: any[]) => any, K extends keyof Awaited<ReturnType<F>>> =
  Pick<Awaited<ReturnType<F>>, K>;

// 예: API 결과 중 필요한 필드만
type MeNameOnly = PickFromReturn<typeof getMe, "name">;
```

## 5) 커링/부분 적용 생성기

```ts
type Tail<T extends any[]> = T extends [any, ...infer R] ? R : never;

function curry<F extends (a: any, ...rest: any[]) => any>(fn: F) {
  return (a: Parameters<F>[0]) =>
    (...rest: Tail<Parameters<F>>): ReturnType<F> =>
      fn(a, ...rest);
}
```

## 6) 라우트 테이블에서 핸들러 자동 타입 생성

```ts
const routes = {
  GET_ME: getMe,
  // ...
} as const;

type RouteArgs<K extends keyof typeof routes>    = Parameters<typeof routes[K]>;
type RouteResult<K extends keyof typeof routes>  = Awaited<ReturnType<typeof routes[K]>>;
```

---

# 체크리스트 (팀에 바로 적용)

1. **타입 원천 하나 정하기**
   서버 핸들러 or 서비스 함수를 “원천”으로 지정하고, 나머지는 `Parameters`/`ReturnType`으로만 참조.

2. **미들웨어/래퍼 만들 때 서명 보존**
   래퍼는 `(...a: Parameters<F>): ReturnType<F>` 패턴 고정.

3. **비동기 결과는 `Awaited`로 벗겨서 도메인 타입 노출**
   외부에 노출할 타입은 `Awaited<ReturnType<...>>` 형태로 export.

4. **오버로드 남발 금지 → 제네릭/분리된 시그니처 타입으로 관리**
   추출 정확도를 높이고, 리팩토링 시 타입 파급을 줄임.

5. **테이블/맵 기반 설계에 적극 활용**
   액션, 커맨드, 라우트, 서비스 레지스트리 등 사전 구조에서 안전 추출.

---

필요하면 네 프로젝트 코드(예: RHF 폼, Supabase 호출, 컨트롤러-서비스 레이어)에 위 패턴을 그대로 이식한 **맞춤형 리팩토링 스니펫**을 뽑아줄 수 있다.



돌려서 안 말함. 실무에서 `ReturnType`을 찾게 되는 순간들은 보통 “타입을 두 번 쓰다 통수 맞을 때”야. 이런 증상들이 원인.

# 언제 `ReturnType`이 필요해지나 (현실 시나리오)

1. **서버-클라 계약이 틀어진다**

* 증상: 서버 핸들러 반환 스키마를 바꿨는데, 클라 DTO는 옛날 타입이라 빌드 통과 후 런타임 오류.
* 해결: 서버 함수가 “타입의 원천”. 클라는 `Awaited<ReturnType<typeof handler>>`만 참조.

```ts
// server
export const getMe = async () => ({ id: "u1", name: "Y" as const });

// client
type Me = Awaited<ReturnType<typeof getMe>>; // { id: string; name: "Y" }
```

2. **미들웨어/래퍼를 씌우자 타입이 깨진다**

* 증상: 캐시/리트라이 래퍼 만들었더니 인자·반환 타입이 `any`로 퍼짐.
* 해결: 래퍼 시그니처를 보존.

```ts
function withCache<F extends (...a: any[]) => Promise<any>>(fn: F) {
  return (...a: Parameters<F>): ReturnType<F> => fn(...a);
}
```

3. **비동기 함수 “안쪽 타입”이 필요하다**

* 증상: 서비스는 `Promise<Result>`를 돌려주는데 폼/뷰는 `Result`만 필요 → 직접 중복 정의하다 드리프트.
* 해결: `Awaited<ReturnType<...>>`.

```ts
type Result = Awaited<ReturnType<typeof fetchUser>>;
```

4. **오버로드된 함수에서 정확한 반환 타입이 안 잡힌다**

* 증상: 오버로드가 많은 유틸을 감싸자 `ReturnType<typeof f>`가 애매하게 넓어짐.
* 해결: 추출용 “시그니처 타입”을 따로 만들거나 제네릭 한 방으로 통일.

```ts
type SigNum = (x: number) => number;
type R = ReturnType<SigNum>; // number
```

5. **React 핸들러 포워딩에서 이벤트 타입이 자꾸 틀린다**

* 증상: `onChange`를 감싸 전달하는데 `Event` 타입을 직접 때려 쓰다 깨짐.
* 해결: 콜백의 파라미터를 그대로 추출.

```ts
type OnChange = (e: React.ChangeEvent<HTMLInputElement>) => void;
const forward = (fn: OnChange) => (e: Parameters<OnChange>[0]) => fn(e);
```

6. **RHF/컨트롤러 폼 값과 서비스 입력 타입이 어긋난다**

* 증상: 서비스 인자 구조 변경 후 폼 타입은 그대로라 검증/제출이 엇나감.
* 해결: 폼 값 = 서비스 첫 인자를 참조.

```ts
type Signup = (form: { email: string; pwd: string }) => Promise<void>;
type FormValues = Parameters<Signup>[0];
```

7. **액션/커맨드 맵에서 특정 액션의 결과를 안전하게 쓰고 싶다**

* 증상: 맵에서 `actions[key]()`의 반환 타입을 매번 눈치게임.
* 해결: 키로 추출.

```ts
const actions = { clear: () => ({ type: "clear" as const }) } as const;
type Clear = ReturnType<typeof actions.clear>; // { type: "clear" }
```

8. **테스트에서 mock 함수 시그니처를 원본과 동기화하고 싶다**

* 증상: jest mock이 `(...args: any[]) => any`가 되어 기대 타입 검증 불가.
* 해결: mock 서명을 원본에서 복사.

```ts
type Svc = (id: string) => Promise<number>;
const mockSvc: (...a: Parameters<Svc>) => ReturnType<Svc> = async () => 1 as const;
```

9. **DI/팩토리에서 생성자/인스턴스 타입을 자동 추출하고 싶다**

* 증상: 클래스 인자/인스턴스 타입을 따로 선언하다가 틀어짐.
* 해결: `ConstructorParameters` + `InstanceType` 조합. (ReturnType 계열 문제의 사촌)

10. **레거시 util이 `any`를 퍼뜨린다**

* 증상: 중간 유틸이 `any` 반환 → 도미노로 타입 추론이 망가짐.
* 해결: 유틸 반환을 원본 함수의 `ReturnType<F>`로 고정해 오염 차단.

---

# 체크리스트 (도입 기준)

* 함수의 **출력**을 다른 레이어에서 “그대로” 쓰고 싶다 → `ReturnType`(+ `Awaited`).
* 함수의 **입력**을 그대로 재사용하고 싶다 → `Parameters`.
* 래핑/미들웨어를 만든다 → `(...a: Parameters<F>): ReturnType<F>` 패턴 고정.
* 오버로드가 많다 → 추출용 시그니처 타입을 따로 노출하거나 제네릭으로 단일화.
* 비동기 결과를 UI/검증 스키마에 연결 → 항상 `Awaited`를 곁들여라.

---

# 확장 적용 아이디어 (조금 더 자동화)

* **경로 테이블 자동 타입화**

```ts
const routes = { getMe, updateUser } as const;
type RouteResult<K extends keyof typeof routes> = Awaited<ReturnType<typeof routes[K]>>;
type RouteArgs<K extends keyof typeof routes>   = Parameters<typeof routes[K]>;
```

* **결과에서 필요한 키만 노출**

```ts
type PickFromReturn<F extends (...a: any[]) => any, K extends keyof Awaited<ReturnType<F>>> =
  Pick<Awaited<ReturnType<F>>, K>;
```

* **커링/부분적용에서도 시그니처 보존**

```ts
type Tail<T extends any[]> = T extends [any, ...infer R] ? R : never;
function curry<F extends (a: any, ...r: any[]) => any>(fn: F) {
  return (a: Parameters<F>[0]) => (...r: Tail<Parameters<F>>): ReturnType<F> => fn(a, ...r);
}
```

---

결론: `ReturnType`을 쓰게 되는 순간은 “한 소스에서 타입을 끌어다 쓰지 않아서 생긴 드리프트와 any 오염”을 체감했을 때다. 원천을 하나(핸들러/서비스)로 정하고, 나머지는 전부 `ReturnType`/`Parameters`로만 참조하라. 그러면 타입이 먼저 깨져서, 런타임이 덜 깨진다.
