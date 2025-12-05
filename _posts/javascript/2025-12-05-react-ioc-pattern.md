---
layout: post
title: 컴포넌트의 주인 되기
summary: React IoC 패턴
date: 2025-12-05 14:30:24 +09:00
categories: javascript
tags: react javascript 프론트엔드
---

컴포넌트를 만들어 사용하다 보면 같은 기능이지만 다른 화면에서는 디자인이나 구조만 살짝 바뀌거나, 기능이 아주 조금 추가/변경되는 경우가 자주 있습니다. 이런 상황이 반복되면 props가 하나씩 추가되고 조건 분기가 하나씩 늘어나며 컴포넌트는 점점 복잡해집니다. 결국 읽고 쓰기 어렵고, 수정하기는 더 어려운 컴포넌트를 만들어낸 경험이 여러 번 있었습니다.

혼자 충분히 고민하고 판단하면서 개발할 수 있는 시간을 가지다 보니, 자연스럽게 하나의 질문이 생겼습니다.

“이 컴포넌트의 제어권은 어디에 두는 게 맞을까?”

명확한 기준 없이 기능을 추가하다 보니, 컴포넌트가 점점 사용자를 강제하고 있다는 느낌도 들었습니다. 그 시점부터 나만의 기준을 세워야겠다는 생각이 들었고, 여러 설계 방식과 패턴을 찾아보게 되었습니다. 그 과정에서 IoC(Inversion of Control, 제어 역전) 패턴들이 특히 인상 깊게 다가왔습니다.


### 다시 돌아본 컴파운드 컴포넌트 패턴

[작년에 작성했던](https://yeol0324.github.io/javascript/design-pattern-compound/) 컴파운드 컴포넌트 패턴 글을 다시 읽어보며 당시에는 재사용성에 대한 고민이 가장 컸다는 걸 다시 느꼈습니다. Compound Component Pattern은 상태와 로직/UI 구조를 분리하는 첫 전환점이었고, 당시에는 컴포넌트 설계 방식과 시각을 바꾸는 계기가 되었습니다.

이후 다시 돌아보니 문제는 재사용성 자체가 아니라, 컴포넌트의 제어권을 어디에 두고 있었는지에 대한 고민이 부족했던 것 같습니다. 그리고 그 관점을 정리해 준 것이 IoC 패턴들이었습니다.

### 렌더링 IoC

IoC(Inversion of Control)는 컴포넌트가 모든 결정을 직접 내리지 않고, 일부 제어를 외부에 위임하는 설계 방식입니다. React에서는 주로 렌더링 방식이나 상태 변경 로직을 외부에서 제어할 수 있도록 구성함으로써 IoC를 구현합니다.

#### Render Props 패턴

Render Props 패턴은 렌더링 함수를 props로 전달하는 방식입니다. 컴포넌트는 데이터나 기본 구조만 제공하고, 실제 렌더링 결과는 사용하는 쪽에서 결정합니다.

구조는 동일하지만 아이템 표현 방식이 달라야 할 때 간단하게 대응할 수 있기 때문에 특히 리스트나 테이블 같은 반복 UI에서 유용합니다.

```tsx
interface ListProps<T> {
  data: T[];
  renderItem: (item: T) => React.ReactNode;
}

function List<T>({ data, renderItem }: ListProps<T>) {
  return (
    <ul>
      {data.map((item, index) => (
        <li key={index}>{renderItem(item)}</li>
      ))}
    </ul>
  );
}
```

위 컴포넌트는 리스트의 기본 구조만 책임지고, 각 아이템을 어떻게 렌더링할지는 `renderItem`을 통해 외부에 위임합니다.

```tsx
<List
  data={users}
  renderItem={(user) => (
    <div>
      <strong>{user.name}</strong>
      <span>{user.score}</span>
    </div>
  )}
/>
```

이처럼 데이터 구조는 동일하지만 화면마다 다른 표현이 필요한 경우, Render Props 패턴은 props를 불필요하게 늘리지 않고도 유연한 렌더링을 가능하게 합니다.

다만 render 함수가 커질수록 가독성이 급격히 떨어집니다. 조건이 많아지면 render props 자체가 복잡해집니다. 함수 형태로 렌더링할 경우 Hook 사용 제약도 발생합니다.

결과적으로 Render Props 패턴은 간단한 반복 UI에는 효과적이지만, 복잡한 UI 설계의 해답이 되기는 어렵다는 결론에 이르렀습니다. 빠르고 가벼운 제어권 위임이 필요한 상황에 적합한 패턴입니다.

#### 합성 컴포넌트 패턴 (Compound Component Pattern)

합성 컴포넌트 패턴은 단순히 컴포넌트를 잘게 나누는 패턴이 아닙니다. 이 패턴의 핵심은 UI 구조에 대한 결정권을 컴포넌트 사용자가 갖도록 하는 것입니다.

이 패턴에서는 상태와 로직을 Context Provider에 두고, UI 구성은 children 조합으로 외부에서 결정합니다. Counter 예제를 통해 보면 이 특징이 명확하게 드러납니다.
```tsx
const CounterContext = React.createContext<{
  count: number;
  increment: () => void;
  decrement: () => void;
} | null>(null);

function Counter({ children }: { children: React.ReactNode }) {
  const [count, setCount] = React.useState(0);

  return (
    <CounterContext.Provider
      value={{
        count,
        increment: () => setCount((c) => c + 1),
        decrement: () => setCount((c) => c - 1),
      }}
    >
      {children}
    </CounterContext.Provider>
  );
}
```
상태와 로직은 Counter 내부에서 관리하고, UI는 하위 컴포넌트들이 Context를 통해 필요한 값만 사용합니다.
```tsx
Counter.Count = function () {
  const context = React.useContext(CounterContext);
  return <span>{context?.count}</span>;
};

Counter.Increase = function () {
  const context = React.useContext(CounterContext);
  return <button onClick={context?.increment}>+</button>;
};

Counter.Decrease = function () {
  const context = React.useContext(CounterContext);
  return <button onClick={context?.decrement}>-</button>;
};
```
이렇게 정의된 컴포넌트는 사용하는 쪽에서 UI 구조를 자유롭게 조합할 수 있습니다.
```tsx
<Counter>
  <Counter.Decrease />
  <Counter.Count />
  <Counter.Increase />
</Counter>
```
버튼의 위치나 배치가 바뀌더라도 Counter 내부의 상태와 로직은 전혀 수정할 필요가 없습니다. 컴포넌트는 기능 단위가 되고, 구조는 사용자 책임이 됩니다.

이 방식의 가장 큰 장점은 UI 변경이 발생하더라도 컴포넌트 내부를 수정할 필요가 없다는 점입니다. 상태와 로직은 부모 컴포넌트나 Context에 고정되어 있고, UI 구조는 사용하는 쪽에서 조합하기 때문에 구성 요소의 위치나 배치가 바뀌더라도 기존 로직을 그대로 재사용할 수 있습니다. 또한 `Counter.Increase`, `Counter.Count`와 같은 형태의 API는 컴포넌트의 사용법을 코드 자체로 설명해 주기 때문에, 별도의 문서 없이도 구조와 의도를 파악하기 쉽습니다. UI 구조가 JSX에 그대로 드러나 가독성이 좋아진다는 점도 분명한 장점입니다.

반면 이 패턴은 Context와 Provider를 전제로 하기 때문에 구조적인 복잡도가 증가할 수 있습니다. 하나의 기능을 사용하기 위해 여러 하위 컴포넌트를 함께 조합해야 하다 보니, 단순한 상황에서는 오히려 사용성이 떨어질 수 있습니다. 특히 UI 변경 가능성이 크지 않은 간단한 컴포넌트에 적용할 경우, 필요 이상의 설계가 될 가능성도 있습니다.

이러한 이유로 합성 컴포넌트 패턴은 기본적으로 적용해야 할 설계 방식이라기보다는, UI 구조 변경 가능성이 높고 조합의 자유도가 중요한 컴포넌트에 선택적으로 적용하는 것이 적절한 패턴이라고 느꼈습니다. 이 지점에서 패턴을 사용하는 목적은 ‘적용했다’는 사실 자체가 아니라, 문제의 성격에 맞는 책임과 제어권을 분리하는 데 있다는 점을 분명하게 인식하게 되었습니다.


### 상태 관리 IoC

렌더링뿐 아니라 상태 관리 역시 IoC의 중요한 적용 대상입니다.

#### Controlled Props 패턴

Controlled Component 패턴은 가장 널리 사용되는 IoC 방식 중 하나로, 상태 값을 컴포넌트 내부에서 관리하지 않고 `value`와 `onChange` 같은 props를 통해 외부에서 제어하는 방식입니다. 입력값 하나를 다루는 단순한 컴포넌트에서는 직관적인 선택입니다.

그러나 관리해야 할 상태가 늘어나기 시작하면 구조적인 부담이 점점 커집니다. 상태가 하나 추가될 때마다 그에 대응하는 콜백도 함께 필요해지고, 그 결과 컴포넌트가 받아야 하는 props의 수 역시 빠르게 증가합니다. 이런 형태는 컴포넌트 뿐만 아니라, 사용하는 쪽에서도 비슷한 상태 관리 코드와 핸들러가 반복되기 쉬운 구조로 이어집니다.

예를 들어, 프로젝트에서 자주 사용하는 검색/필터 컴포넌트를 컨트롤드 패턴으로만 설계했을 때를 생각해볼 수 있습니다.
```tsx
interface SearchFilterProps {
  keyword: string;
  status: "all" | "active" | "inactive";
  startDate: string;
  endDate: string;

  onKeywordChange: (value: string) => void;
  onStatusChange: (value: "all" | "active" | "inactive") => void;
  onStartDateChange: (value: string) => void;
  onEndDateChange: (value: string) => void;
}

function SearchFilter(props: SearchFilterProps) {
  const {
    keyword,
    status,
    startDate,
    endDate,
    onKeywordChange,
    onStatusChange,
    onStartDateChange,
    onEndDateChange,
  } = props;

  return (
    <div>
      <input
        placeholder="검색어"
        value={keyword}
        onChange={(e) => onKeywordChange(e.target.value)}
      />
      <select
        value={status}
        onChange={(e) =>
          onStatusChange(e.target.value as "all" | "active" | "inactive")
        }
      >
        <option value="all">전체</option>
        <option value="active">활성</option>
        <option value="inactive">비활성</option>
      </select>
      <input
        type="date"
        value={startDate}
        onChange={(e) => onStartDateChange(e.target.value)}
      />
      <input
        type="date"
        value={endDate}
        onChange={(e) => onEndDateChange(e.target.value)}
      />
    </div>
  );
}
```
이 컴포넌트를 사용하는 쪽에서는 모든 상태와 콜백을 직접 관리해야 합니다.
```tsx
function UserListPage() {
  const [keyword, setKeyword] = useState("");
  const [status, setStatus] = useState<"all" | "active" | "inactive">("all");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  // 이 부분이 페이지마다 거의 비슷한 형태로 반복되기 쉽습니다.
  return (
    <SearchFilter
      keyword={keyword}
      status={status}
      startDate={startDate}
      endDate={endDate}
      onKeywordChange={setKeyword}
      onStatusChange={setStatus}
      onStartDateChange={setStartDate}
      onEndDateChange={setEndDate}
    />
  );
}
```
컴포넌트 입장에서는 props가 많아지고,
사용하는 쪽에서는 비슷한 형태의 상태 선언과 핸들러가 계속 반복됩니다.
페이지가 여러 개일수록 이런 패턴이 그대로 복제되면서 중복 로직이 쌓이기 쉬운 구조가 됩니다.

이 지점에서 “상태를 전부 외부로 빼는 것”만으로는 충분하지 않고,
어떤 수준까지 제어권을 외부에 줄지 더 세밀하게 설계할 필요가 있다는 생각을 하게 되었습니다.
#### Props Getter 패턴

Props Getter 패턴은 Controlled Props의 단점을 보완하기 위한 방식입니다. 상태와 기본 동작을 커스텀 훅으로 묶고, 컴포넌트는 그 결과만 사용합니다. 사용자는 필요한 콜백만 선택적으로 오버라이드할 수 있습니다.

문장 리스트를 필터링하는 기능을 예로 들어 보겠습니다.
레벨, 즐겨찾기 여부, 검색 키워드를 기준으로 여러 페이지에서 비슷한 필터 UI를 사용한다고 가정합니다.
```tsx
type Level = "ALL" | "BEGINNER" | "INTERMEDIATE" | "ADVANCED";

interface SentenceFilterState {
  level: Level;
  onlyFavorite: boolean;
  keyword: string;
}

interface UseSentenceFilterOptions {
  defaultLevel?: Level;
  onChange?: (next: SentenceFilterState) => void;
}

export function useSentenceFilter(options: UseSentenceFilterOptions = {}) {
  const { defaultLevel = "ALL", onChange } = options;

  const [filters, setFilters] = React.useState<SentenceFilterState>({
    level: defaultLevel,
    onlyFavorite: false,
    keyword: "",
  });

  const update = (partial: Partial<SentenceFilterState>) => {
    setFilters((prev) => {
      const next = { ...prev, ...partial };
      onChange?.(next); // 공통 동작 callback
      return next;
    });
  };

  return {
    filters,
    setLevel: (level: Level) => update({ level }),
    toggleFavorite: () => update({ onlyFavorite: !filters.onlyFavorite }),
    setKeyword: (keyword: string) => update({ keyword }),
  };
}
```
`SentenceFilter` 컴포넌트는 이 훅을 그대로 사용해서 UI만 책임을 갖습니다.
```tsx
interface SentenceFilterProps extends UseSentenceFilterOptions {}

export function SentenceFilter(props: SentenceFilterProps) {
  const { filters, setLevel, toggleFavorite, setKeyword } = useSentenceFilter(props);

  return (
    <div>
      <select
        value={filters.level}
        onChange={(e) => setLevel(e.target.value as Level)}
      >
        <option value="ALL">전체</option>
        <option value="BEGINNER">Beginner</option>
        <option value="INTERMEDIATE">Intermediate</option>
        <option value="ADVANCED">Advanced</option>
      </select>

      <button onClick={toggleFavorite}>
        {filters.onlyFavorite ? "즐겨찾기" : "전체 보기"}
      </button>

      <input
        placeholder="키워드 검색"
        value={filters.keyword}
        onChange={(e) => setKeyword(e.target.value)}
      />
    </div>
  );
}
```
페이지에서는 공통 로직은 훅이 맡기고, 필요한 부분만 오버라이드할 수 있습니다.
```tsx
function SentencesPage() {
  const [query, setQuery] = React.useState<SentenceFilterState | null>(null);

  const handleFilterChange = (next: SentenceFilterState) => {
    setQuery(next);
    // 이 페이지에서만 필요한 추가 동작
    // trackFilterChange("sentences", next);
  };

  return (
    <div>
      <SentenceFilter defaultLevel="INTERMEDIATE" onChange={handleFilterChange} />
      {/* query 상태를 기반으로 리스트 요청 */}
      {/* <SentenceList filters={query} /> */}
    </div>
  );
}

```
이 방식의 장점은 분명하게 드러납니다.

여러 페이지에서 반복되던 필터 상태 관리 로직을 하나의 커스텀 훅으로 모을 수 있기 때문에, 상태 선언과 기본 동작이 자연스럽게 한곳에 정리됩니다. 공통으로 필요한 동작은 `useSentenceFilter` 내부에서 처리하고, 화면마다 필요한 경우에만 `onChange` 같은 콜백을 선택적으로 오버라이드할 수 있어 중복 코드를 줄이는 데 효과적입니다. 그 결과 `SentenceFilter` 컴포넌트를 사용할 때 요구되는 props의 수가 최소한으로 유지되며, 컴포넌트 사용성 역시 이전보다 개선됩니다.

다만 이 패턴 역시 한계를 완전히 해결해 주는 것은 아닙니다. 구조적으로 많이 정리되었지만, 여전히 콜백을 중심으로 확장하는 방식이기 때문에 컴포넌트가 복잡해질수록 콜백의 종류가 늘어나는 문제 자체를 근본적으로 제거하지는 못합니다.

#### State Reducer 패턴

State Reducer 패턴은 IoC를 가장 강하게 적용한 방식입니다. 컴포넌트는 액션만 정의하고, 상태 전이 규칙은 reducer를 통해 외부에서 결정합니다.

예를 들어, “녹음 연습 세션”을 관리하는 컴포넌트를 생각해볼 수 있습니다. 기본적으로는 IDLE → RECORDING → REVIEW 같은 흐름을 갖지만, 어떤 화면에서는 하루 연습 횟수 제한이 필요하고, 어떤 화면에서는 자유롭게 반복 연습을 허용할 수 있습니다. 이때 State Reducer 패턴을 사용하면, 컴포넌트는 공통 액션만 정의하고 “연습 정책”은 외부에서 교체할 수 있습니다.

```tsx
type PracticeStatus = "IDLE" | "RECORDING" | "REVIEW";

type PracticeAction =
  | { type: "START_RECORD" }
  | { type: "STOP_RECORD" }
  | { type: "RESET" };

interface PracticeState {
  status: PracticeStatus;
  attemptCount: number;
}

// 내부 리듀서
function basePracticeReducer(
  state: PracticeState,
  action: PracticeAction
): PracticeState {
  switch (action.type) {
    case "START_RECORD":
      return { ...state, status: "RECORDING" };
    case "STOP_RECORD":
      return {
        ...state,
        status: "REVIEW",
        attemptCount: state.attemptCount + 1,
      };
    case "RESET":
      return { ...state, status: "IDLE" };
    default:
      return state;
  }
}

// 외부에서 주입할 수 있는 리듀서 타입
type PracticeReducer = (
  state: PracticeState,
  action: PracticeAction,
  next: typeof basePracticeReducer
) => PracticeState;

interface PracticeSessionProps {
  reducer?: PracticeReducer;
}

export function PracticeSession({ reducer }: PracticeSessionProps) {
  const composedReducer = React.useCallback(
    (state: PracticeState, action: PracticeAction) => {
      if (!reducer) return basePracticeReducer(state, action);
      return reducer(state, action, basePracticeReducer);
    },
    [reducer]
  );

  const [state, dispatch] = React.useReducer(composedReducer, {
    status: "IDLE",
    attemptCount: 0,
  });

  return (
    <div>
      <p>상태: {state.status}</p>
      <p>시도 횟수: {state.attemptCount}</p>

      {state.status === "IDLE" && (
        <button onClick={() => dispatch({ type: "START_RECORD" })}>
          녹음 시작
        </button>
      )}

      {state.status === "RECORDING" && (
        <button onClick={() => dispatch({ type: "STOP_RECORD" })}>
          녹음 종료
        </button>
      )}

      {state.status === "REVIEW" && (
        <button onClick={() => dispatch({ type: "RESET" })}>
          다시 연습
        </button>
      )}
    </div>
  );
}
```
위 컴포넌트는 액션(START_RECORD, STOP_RECORD, RESET)만 공개하고, 상태 전이 규칙은 `basePracticeReducer`에 숨깁니다. 이제 특정 페이지에서만 “하루 최대 3회까지만 연습 허용” 같은 정책을 적용하고 싶다면, 외부 reducer를 통해 필요한 액션만 오버라이드할 수 있습니다.

```tsx
// 하루 최대 3번까지만 STOP_RECORD 허용
const limitedPracticeReducer: PracticeReducer = (
  state,
  action,
  next
) => {
  if (action.type === "STOP_RECORD" && state.attemptCount >= 3) {
    // 추가 정책: 토스트 노출, 경고 로그 등
    // showToast("오늘 연습은 여기까지입니다.");
    return state; // 상태 변화 차단
  }

  return next(state, action); // 나머지 기본 로직 사용
};

export function DailyLimitedPracticePage() {
  return (
    <div>
      <h2>하루 3회 제한 연습</h2>
      <PracticeSession reducer={limitedPracticeReducer} />
    </div>
  );
}
```

특히 외부 reducer와 내부 reducer를 결합하는 구조는, 필요한 액션만 오버라이드하고 나머지는 기본 동작을 재사용할 수 있다는 점에서 인상 깊었습니다. 이는 단순한 확장이 아니라, 행동에 대한 정책을 교체하는 설계에 가깝습니다.

이 패턴의 특징은 reducer를 주입하는 것만으로 컴포넌트의 동작을 변경할 수 있기 때문에 컴포넌트 API가 매우 단순해진다는 점입니다. 컴포넌트는 더 이상 여러 상태 값이나 콜백을 외부로 노출하지 않고, 공통 액션과 기본 동작만을 유지합니다. 이로 인해 내부 상태 구조나 전이 로직이 변경되더라도, 액션과 reducer 인터페이스만 유지된다면 사용하는 쪽의 코드는 거의 영향을 받지 않습니다.

반면 이러한 유연성은 그만큼의 복잡도를 동반합니다. reducer를 통해 상태 흐름을 이해해야 하고, 내부 reducer와 외부 reducer의 역할을 구분해야 하기 때문에 개념 난이도와 러닝 커브는 상대적으로 높은 편입니다. 따라서 State Reducer 패턴은 단순한 UI 컴포넌트보다는, 규칙이 자주 바뀌거나 정책 단위로 동작을 교체해야 하는 복잡한 컴포넌트나 라이브러리 수준의 컴포넌트에 적합한 선택이라고 느꼈습니다.

### 마무리하며

IoC 패턴들 정리
- Render Props: 빠른 렌더링 유연성
- Compound Component: UI 구조에 대한 제어권 위임
- Controlled / Props Getter: 상태 제어의 단계적 확장
- State Reducer: 동작 정책 자체의 위임

어떤 패턴이 더 좋은 패턴인지는 중요하지 않습니다. 이제 대신 이 컴포넌트에서 가장 쉽게 변할 가능성이 있는 것은 무엇인가? 라는 고민을 먼저 하게 되었습니다. UI 구조인지, 상태 값인지, 아니면 동작 규칙인지에 따라 선택해야 할 패턴은 달라집니다. 이번 정리를 통해 패턴을 사용한다는 것이 코드를 복잡하게 만드는 일이 아니라, 책임과 제어권의 경계를 명확히 정하는 일이라는 점을 분명히 알게 되었습니다.

리액트에는 수많은 패턴이 존재하지만, 그 모든 것을 정확하게 기억하고 있을 수는 없습니다. 중요한 것은 다양한 레퍼런스를 쌓고, 각 패턴이 어떤 문제를 해결하기 위해 등장했는지를 이해하며 준비해 두는 과정이라고 생각합니다.

앞으로도 새로운 패턴들을 계속 접하게 될 것이고, 그중 많은 것들은 까먹을 수도 있습니다. 그럼에도 불구하고, 필요한 순간에 적절한 설계 방식을 떠올리고 선택할 수 있는 개발자가 되고 싶습니다. 이번 IoC 패턴 정리는 그 방향으로 나아가기 위한 하나의 준비 과정이되었습니다.

### 참조
- <https://kentcdodds.com/blog/the-state-reducer-pattern>
- <https://tech.kakaoent.com/front-end/2022/221110-ioc-pattern>