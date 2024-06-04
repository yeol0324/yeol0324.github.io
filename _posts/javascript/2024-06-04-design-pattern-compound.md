---
layout: post
title: 리액트 디자인 패턴 - 컴파운드 컴포넌트 패턴
summary: 컴파운드 컴포넌트 패턴으로 재사용 가능한 컴포넌트 만들기
date: 2024-06-04 10:14:41 +09:00
categories: javascript
tags: react
---


여러분이 컴포넌트를 설계할 때 가장 고민하는 것은 무엇인가요? 저는 컴포넌트의 재사용성을 가장 중요하게 생각합니다. 컴포넌트를 기껏 만들어놨는데 디자인이나 특정 기능 때문에 다른 곳에서 사용할 수 없게 된다면 컴포넌트를 만드는 의미가 많이 사라지게 되죠. 또, 유사한 기능을 가진 컴포넌트를 생성했는데 디자인이나 UI가 바뀔 때마다 예외 처리를 해야 한다면 가독성이 떨어지게 됩니다. 제가 이런 고민을 할 때 알게 되어 가장 많이 사용한 **Compound component pattern** 을 소개해볼까 합니다.


# Compound Component

Compound Component Pattern은 '합성' 컴포넌트 패턴으로, 컴포넌트를 더 작은 하위 컴포넌트로 나누어 상태와 컨텍스트를 공유하고 하나의 동작을 할 수 있게 합니다. 이때 부모와 자식 컴포넌트 간의 상태 공유를 할 때 <span class="h-yellow">React Context API</span>를 사용합니다. 컴파운드 컴포넌트 패턴은 복잡한 UI 요소를 조립할 때 특히 유용합니다.


# 컴파운드 패턴 맛보기

설명으로만 보면 감이 잘 안 잡히죠? 먼저 간단한 카운터를 만들어 보면서 확인해보겠습니다!

## 컨텍스트 생성
```javascript
import { createContext, useContext, useState } from "react";

const CounterContext = createContext();
```

createContext 함수를 사용하여 CounterContext를 생성합니다. 컴포넌트 계층 구조에서 공유할 수 있는 전역 상태를 정의하는 데 사용됩니다.

## 컴포넌트 생성
**부모 컴포넌트**
```javascript
function Counter({ children }) {
  const [count, setCount] = useState(0);
  const increase = () => setCount((c) => c + 1);
  const decrease = () => setCount((c) => c - 1);

  return (
    <CounterContext.Provider value={{ count, increase, decrease }}>
      <span>{children}</span>
    </CounterContext.Provider>
  );
}
```

부모 컴포넌트인 Counter 컴포넌트는, 상태와 로직을 관리하는 역할을 합니다.
CounterContext.Provider는 value 속성을 통해 count, increase, decrease 값을 하위 컴포넌트와 공유합니다.

**자식(하위) 컴포넌트**
```javascript
function Count() {
  const { count } = useContext(CounterContext);
  return <span>{count}</span>;
}

function Label({ children }) {
  return <span>{children}</span>;
}

function Increase({ icon }) {
  const { increase } = useContext(CounterContext);
  return <button onClick={increase}>{icon}</button>;
}

function Decrease({ icon }) {
  const { decrease } = useContext(CounterContext);
  return <button onClick={decrease}>{icon}</button>;
}
```

useContext를 사용하여 CounterContext에서 데이터나 함수를 가져와서 사용합니다.

## 프로퍼티로 할당
```javascript
Counter.Count = Count;
Counter.Label = Label;
Counter.Increase = Increase;
Counter.Decrease = Decrease;

export default Counter;
```

Counter 컴포넌트에 자식 컴포넌트들을 프로퍼티로 할당합니다. 이를 통해 Counter 컴포넌트는 합성 컴포넌트 패턴을 사용하여 하위 컴포넌트들을 포함하게 됩니다.

## 사용 예시

컴파운드 컴포넌트 패턴으로 생성된 컴포넌트는 이렇게 사용할 수 있습니다.

```javascript
export default function App() {
  return (
    <div className="App">
      <Counter>
        This is the Count Value: <Counter.Count />
        <Counter.Label>카운터</Counter.Label>
        <Counter.Decrease icon={<span>Decrease</span>} />
        <Counter.Increase icon={<span>Increase</span>} />
      </Counter>
    </div>
  );
}
```
이 패턴을 사용하면 컴포넌트의 재사용성과 유연성을 높일 수 있습니다. 각 하위 컴포넌트가 독립적으로 동작하면서도 부모 컴포넌트와 상태를 공유하기 때문에, 다양한 UI 요구 사항을 쉽게 처리할 수 있습니다. 특히 컴포넌트를 사용하는 곳에서도 하위에 있는 컴포넌트와 위치를 한눈에 알아볼 수 있어 가독성이 좋아집니다.

# 컴파운드 패턴 응용

카운터 예제가 너무 간단해서 궁금증이 잘 풀리지 않으셨죠? 이번엔 자주 사용하는 폼 컴포넌트를 생성해보겠습니다. 유저의 정보를 입력받아 submit까지 하는 컴포넌트를 생성해볼까요? 이번엔 타입스크립트를 적용할 때는 어떻게 사용하는지, 또 컴포넌트 복사는 어떻게 하는지 함께 작업해보겠습니다.

컨텍스트 생성
```javascript
import React, {
  createContext,
  useContext,
  useState,
  ReactNode,
  ChangeEvent,
  FC,
} from "react";

interface FormData {
  name: string;
  email: string;
  password: string;
}

// 컨텍스트 생성
interface UserFormContextType {
  formData: FormData;
  updateField: (field: keyof FormData, value: string) => void;
}
const UserFormContext = createContext<UserFormContextType | null>(null);

interface UserFormProps {
  children: ReactNode;
}
type UserFormComponentType = FC<UserFormProps> & {
  Field: FC<FieldProps>;
  Label: FC<LabelProps>;
  Input: FC<React.InputHTMLAttributes<HTMLInputElement>>;
  SubmitButton: FC<SubmitButtonProps>;
};

// 부모 컴포넌트 코드
const UserForm: UserFormComponentType = ({ children }) => {
  const [formData, setFormData] = useState<FormData>({
    name: "",
    email: "",
    password: "",
  });

  const updateField = (field: keyof FormData, value: string) => {
    setFormData({
      ...formData,
      [field]: value,
    });
  };

  return (
    <UserFormContext.Provider value={{ formData, updateField }}>
      <form>{children}</form>
    </UserFormContext.Provider>
  );
};

interface FieldProps {
  name: keyof FormData;
  children: ReactNode;
}
const Field: FC<FieldProps> = ({ name, children }) => {
  const context = useContext(UserFormContext);

  if (!context) {
    throw new Error("UserForm이 없습니다.");
  }

  const { formData, updateField } = context;

  return React.cloneElement(children as React.ReactElement, {
    value: formData[name],
    onChange: (e: ChangeEvent<HTMLInputElement>) =>
      updateField(name, e.target.value),
  });
};
```
## cloneElement

여기서! cloneElement를 사용한 이유는 무엇일까요?
form 안에는 많은 input 태그가 들어있습니다. input의 type만 해도 많은 종류가 있죠. 타입마다 하나씩 컴포넌트를 만들게 된다면... 어디서 사용할지도 모르는 엄청나게 많은 인풋을 생성하게 되겠죠? 또 키값마다 스타일을 줘야한다면,<br>
사용하는 곳에서 ```<span class="form-key">이름 : </span>```과 같은 코드의 중복이 많이 생길 것입니다.
React 요소를 복제하여 새로운 props를 추가하거나 기존 props를 덮어씌울 수 있게 해주는 함수인 React.cloneElement를 사용하여 전달받은 props로 생성을 해줍니다.

```javascript
interface LabelProps {
  htmlFor: string;
  children: ReactNode;
}

const Label: FC<LabelProps> = ({ htmlFor, children }) => (
  <label htmlFor={htmlFor}>{children}</label>
);
const Input: FC<React.InputHTMLAttributes<HTMLInputElement>> = (props) => (
  <input {...props} />
);
javascript
interface SubmitButtonProps {
  children: ReactNode;
}

const SubmitButton: FC<SubmitButtonProps> = ({ children }) => {
  const context = useContext(UserFormContext);

  if (!context) {
    throw new Error("UserForm 이 없습니다.");
  }

  const { formData } = context;

  const handleSubmit = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    console.log("data:", formData);
  };

  return (
    <button type="submit" onClick={handleSubmit}>
      {children}
    </button>
  );
};

UserForm.Field = Field;
UserForm.Label = Label;
UserForm.Input = Input;
UserForm.SubmitButton = SubmitButton;

export { UserForm };
```

# 사용 예시
```javascript
import React from "react";
import { UserForm } from "./UserForm"; // 파일 경로에 맞게 수정

const MyFormComponent = () => (
  <UserForm>
    <UserForm.Field name="name">
      <UserForm.Label htmlFor="name">Name:</UserForm.Label>
      <UserForm.Input id="name" type="text" />
    </UserForm.Field>
    <UserForm.Field name="email">
      <UserForm.Label htmlFor="email">Email:</UserForm.Label>
      <UserForm.Input id="email" type="email" />
    </UserForm.Field>
    <UserForm.Field name="password">
      <UserForm.Label htmlFor="password">Password:</UserForm.Label>
      <UserForm.Input id="password" type="password" />
    </UserForm.Field>
    <UserForm.SubmitButton>Submit</UserForm.SubmitButton>
  </UserForm>
);

export default MyFormComponent;
```
MyFormComponent는 UserForm을 사용하여 입력 필드들과 제출 버튼을 렌더링합니다.
UserForm.Field, UserForm.Label, UserForm.Input, UserForm.SubmitButton을 사용하여 폼을 구성합니다.

# 마무리

컴포넌트를 설계할 때, 재사용성만 고려하다 보니 점점 props가 늘어나고 예외처리만 늘어나기 마련이었습니다. 길고 복잡한 코드를 보면서 이게 최선이라고 생각하며 다른 사람들이 보기에 이해하기 어려운 컴포넌트를 만들었습니다.

클린 코드, 수많은 디자인 패턴에 관한 글을 읽어도, '이걸 어떻게 적용할까? 반복적인 코드만 공통으로 만들면 되지.' 하고 안일한 생각을 가지고 있던 시간이 너무 부끄러워졌습니다.

컴파운드 컴포넌트를 알게 되어 React를 더욱 깊게 이해하게 됐습니다.

공부하고 알아가야 할 것이 많겠지만, 앞으로는 적절한 상황에서 적절한 디자인 패턴을 사용하고 더 나은 코드를 사용하기 위한 고민을 효율적으로 할 수 있을 것 같습니다.



- <https://www.patterns.dev/react/compound-pattern>
- <https://patterns-dev-kr.github.io/design-patterns/compound-pattern/>