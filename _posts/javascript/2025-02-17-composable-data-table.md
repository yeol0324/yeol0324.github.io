---
layout: post
title: 재사용 가능한 데이터 테이블
summary: TanStack Table과 가상화
date: 2025-02-17 09:41:33 +09:00
categories: javascript
tags: frontend typescript javascript performance
---

관리자 대시보드를 개발하다 보면 필수인 데이터 테이블이 있습니다. 사용자 목록, 주문 내역, 상품 관리, 로그 조회 등등 각 페이지마다 비슷하지만 각각 다른 테이블들이 필요합니다.

처음에는 페이지마다 테이블을 복사해서 쓰다가 중복을 줄이기 위해 공통 테이블 컴포넌트 하나를 만들어 사용했습니다. 공통 컴포넌트를  하나 잘 만들어두먼 모든 페이지에서 사용할 수 있겠다고 생각했습니다.

하지만 프로젝트 요구사항이 점점 많아지고 바뀌면서 테이블 컴포넌트가 복잡해졌고 모든 기능을 넣어 만들었던 테이블 컴포넌트가 점점 복잡해졌습니다. 페이지마다 필요한 기능이 달랐기 때문에 컴포넌트에 옵션이 계속 늘어나고 하나를 고치면 다른 화면이 깨지는 문제가 많이 나타났습니다. 특히 10만 건 이상의 보안 로그처럼 데이터 규모가 큰 화면에서는 브라우저가 멈추는 현상도 발생했습니다.

이런 문제들을 어떻게 해결했는지와 재사용 가능한 테이블 컴포넌트를 어떻게 설계했는지 정리했습니다.

## 테이블 요구사항

프로젝트에서 필요한 테이블의 요구사항은 다양했습니다.

- 정렬 (여러 컬럼 동시 정렬 지원)
- 필터링 (텍스트, 날짜 범위, 셀렉트 등)
- 페이지네이션, 무한스크롤
- 행 선택 (단일/다중 선택, 전체 선택)
- 드래그로 컬럼 너비 조절

각 셀에는 데이터의 상태를 드롭다운으로 변경, 메모 입력 등의 인터랙션 요소들이 포함되어 있었습니다.  상세보기 팝업이나 처리 확인 팝업을 띄워야하는 경우도 있었습니다.

이런 요구사항을 각 페이지마다 구현하다보니 50% 이상이 중복된 코드가 되었고 옵션 추가나 수정이 있으면 적용되어있는 모든 파일을 수정해야했습니다. 또 각각 수정하다보니 데이터 테이블마다 UI/UX가 다른 곳들도 생겼습니다.

## 테이블 설계 원칙

재사용 가능한 시스템을 만들기 위해 4가지 원칙을 세웠습니다.

1) 책임은 하나만

각 기능을 분리된 훅으로 나눴습니다. 예를 들어 `useServerSorting`은 정렬 파라미터를 관리하고 `useRowPatch`는 행 수정 상태만 관리하는 식으로 각각 독립적인 책임을 두었습니다.

기능별로 훅을 만들어 두고 UI 구현은 테이블 컴포넌트에서 처리하도록 분리했습니다. 기능 단위로 분리해서 특정 기능의 버그가 다른 기능에 영향을 주지 않고, 문제 발생 시 원인을 빠르게 예측하고 해결할 수 있었습니다.

2) 기능 조합

페이지마다 필요한 기능이 다르기때문에 공통 테이블에 모든 기능을 넣어버리는 방식은 유지보수를 어렵게 만듭니다. 페이지는 필요한 훅만 선택해서 붙이고, 조회 파라미터만 조합해 API를 호출하도록 구성했습니다.

3) 선언적 컬럼 정의 

컬럼 구성은 JSX 내부에서 작성하는 대신 컬럼을 선언적으로 정의하는 방식으로 구성했습니다. 이 방식은 [TanStack Table](https://tanstack.com/table/v8/docs/guide/cells)의 컬럼 정의 방식이기도 합니다.

컬럼 정의가 따로 되어있으면 테이블 로직과 셀 UI가 분리되어 컬럼의 역할을 한눈에 파악할 수 있고 컬럼을 추가하거나 제거할 때도 JSX가 아니라 배열 수정으로 유지보수가 편해집니다.

4) 확장 구조

공통 컴포넌트를 하나 만들어두고 사용할 땐 기능이 추가될 때마다 컴포넌트가 수정되고 그때마다 다른 화면이 같이 영향을 받았습니다. 규모가 커지고 기능이 많아질 수록 모든 기능을 미리 만들어두는 것보다 신규 기능을 쉽게 추가할 수 있는 구조가 중요했습니다. 셀 확장은 컬럼 정의에서, 테이블 기능 확장은 훅 추가로 하도록 했습니다.

- 새로운 셀 타입 추가

셀 UI는 컬럼 정의에서 작성하기 때문에 새로운 입력 방식이나 인터랙션이 필요해도 기존 테이블 로직을 수정할 필요가 없습니다. 예를 들어 상태값을 Chip 형태로 바꾸고 싶다면 컬럼의 Cell 선언 부분만 수정하면 됩니다.

```ts
const UserColumns=[
  {
    header: "상태",
    accessorKey: "status",
    cell: ({ row, getValue }) => (
      <StatusChip
        value={getValue()}
        onChange={(next) => updateStatus(row.original.id, next)}
      />
    ),
  },
]
```
셀 하나 추가 시에 기존 Table 컴포넌트 수정 없이 셀 단위 요구사항이 다른 컬럼에 영향을 주지 않도록 수정할 수 있습니다.

- 새로운 테이블 기능 추가

기능 단위로 훅을 분리했기 때문에 새로운 요구사항은 새로운 훅 추가로 해결할 수 있습니다. 컬럼 숨김, 고정 컬럼 같은 UI 기능은 정렬, 필터, 페이지네이션 등과 상관 없이 추가할 수 있도록 구성했습니다.

## TanStack Table

TanStack Table은 테이블 UI를 직접 제공하는 라이브러리가 아니고 정렬, 필터, 선택 같은 테이블 동작을 구현하는 데 필요한 구조를 제공하는 Headless 테이블 라이브러리입니다.

- Headless UI 구조

TanStack Table은 UI를 제공하지 않는 Headless 구조입니다. UI가 강제로 정해져 있지 않아서 프로젝트의 디자인(MUI 등)에 맞춰 DOM 구조, 스타일, 컴포넌트 직접 디자인을 구성할 수 있습니다.

- 타입 지원

컬럼과 데이터 구조가 타입으로 정의되어 있어 유지보수가 쉽습니다. 컬럼 구조 변경 시 바로 확인 가능하며 컬럼 accessor, cell에서 자동완성이 지원됩니다. 잘못된 필드 접근은 컴파일 단계에서 차단 되어 크고 복잡한 테이블에 안정성을 더해줍니다.

- 다양한 기능

TanStack Table은 정렬, 필터링, 페이지네이션, 컬럼 리사이징, 고정, row selection, grouping 등 다양한 기능을 필요한 화면에서만 선택적으로 적용할 수 있습니다.

- 가상화 적용이 쉬운 구조

테이블 동작 로직과 화면 렌더링이 분리되어 렌더링 구조를 직접 구성할 수 있습니다. 그래서 데이터가 많아졌을 때도 테이블 전체를 갈아엎는 게 아니라, 렌더링 방식만 교체하는 방식으로 확장할 수 있습니다.

## 커스텀 훅으로 기능 분리

테이블에서 자주 반복되는 기능을 컴포넌트 안에 모두 넣어버리면 기능이 늘어날수록 이벤트 처리와 재조회 타이밍이 뒤섞입니다. 정렬과 검색이 붙고 무한 스크롤까지 들어가면 어디에서 데이터를 다시 불러오는지 한눈에 보기 어려워지고 수정할 때도 영향 범위를 예측하기 어렵습니다.

그래서 저는 페이지에서 사용할 테이블을 만들 때 데이터 흐름을 하나의 훅으로 모으되, 각 책임을 유지하는 방식으로 정리했습니다.  특정 API에 종속된 UI 컴포넌트를 만들기보다는 페이지에서 데이터를 조립하고 테이블은 렌더링만 하게 두고 싶었습니다.

테이블 UI는 rows만 받아서 렌더링하고 정렬과 검색은 서버에서 처리하도록, 훅은 데이터를 직접 가공하지 않고 재조회에 필요한 파라미터만 관리하는 역할로 제한했습니다. 파라미터가 바뀌면 무한 스크롤 상태를 초기화한 뒤 다시 조회하도록 하고, 편집은 원본 데이터를 바로 수정하지 않고 patch layer로 분리해 관리했습니다. 공통 테이블은 UI만 담당하고, 실제 조회와 상태 조합은 화면별 훅으로 분리했습니다. 그래서 테이블은 바뀌어도 훅은 각 화면에 맞게 독립적으로 사용할 수 있었습니다.

```tsx
export const useTableQuery = <T, F extends Record<string, unknown>>(
  options: UseTableQueryOptionsType<T, F>
) => {
  const { params, actions } = useTableParams<F>({
    initialFilters: options.initialFilters,
  });

  const remote = useRemoteTableData<T, F>({ fetchFn: options.fetchFn });

  const autoFetch = options.autoFetch ?? true;

  useEffect(() => {
    if (!autoFetch) return;
    remote.refetch(params);
  }, [autoFetch, params, remote]);

  return {
    // result
    ...remote,

    // params
    ...params,

    // actions
    refetch: () => remote.refetch(params),
    ...actions,
  };
};
```

훅 안에서 의미가 섞이지 않도록 경계선을 지키는 것입니다. 예를 들어 작은 훅에서 조건 분기가 늘어나기 시작하면 상태가 이미 가공된 의미를 가지기 시작한 신호라고 보고, 파라미터나 상태를 더 쪼갤 수 있는지 다시 점검했습니다.

## Cell 컴포넌트 분리

컬럼 정의는 어떤 셀을 어떻게 렌더링할지만 선언하고 실제 UI, 인터랙션은 셀 컴포넌트로 분리했습니다. 테이블은 레이아웃, 가상화 같은 테이블 동작을 담당하고, 각 셀의 입력이나 선택 같은 동작은 셀 컴포넌트에 책임을 두었습니다.

### Interactive cell

테이블 셀은 텍스트만 보여주는 용이 아니라 입력, 선택, 버튼, 팝업 등의 인터랙션이 필요했습니다. 이때 TanStack Table의 cell 콜백은 렌더 과정에서 자주 호출되기 때문에, cell 함수 내부에서 훅을 직접 호출하거나 로직을 크게 늘리지 않도록 했습니다.

cell은 어떤 셀 컴포넌트를 보여줄지만 결정하고, 셀 컴포넌트는 입력 UI와 로컬 상태인 편집 중 값, 열림 여부 등만 관리하도록 했습니다. 저장 요청, optimistic 반영, 서버 응답 동기화, 실패 시 롤백처럼 데이터 일관성이 필요한 로직은 셀 밖으로 분리해 한 곳에서 관리했습니다.

```tsx
export const SelectCell = <T extends string,>({
  value,
  options,
  disabled = false,
  onChange,
}: SelectCellProps<T>) => {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value as T)}
      disabled={disabled}
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  );
};

export const columns: ColumnDef<User>[] = [
  {
    accessorKey: "email",
    header: "이메일",
    cell: ({ getValue }) => {
      const value = getValue<string>();
      return <span>{value ?? ""}</span>;
    },
  },
  {
    accessorKey: "confirm",
    header: "확인",
    cell: ({ getValue }) => {
      const value = getValue<string>();
      return (
        <SelectCell
          value={value}
          options={confrimState}
          onChange={
            // 변경 이벤트 전달
          }
        />
      );
    },
  },
];

```

페이지별 요구사항은 onChange, onCommit, actions 같은 핸들러를 props로 주입하고 저장은 화면 훅에서 관리할 수 있었습니다.

### ActionCell

액션 버튼은 대부분 상세보기, 삭제, 차단처럼 행 단위 작업이 필요했습니다. 반복되는 패턴을 위해 ActionCell을 공통으로 만들고, 페이지에서 필요한 액션만 전달하도록 구성했습니다.
액션의 실제 처리는 상위 레이어에서 관리하고, 셀은 버튼 렌더링과 클릭 이벤트 전달에 집중하도록 분리했습니다.

이렇게 테이블마다 흩어져 있던 셀 로직을 모아 셀 컴포넌트 단위로 재사용할 수 있었습니다.


## Optimistic Update

업무용 테이블에서는 한 번 수정하고 끝나는 경우가 거의 없습니다. 사용자한테 화면이 자주 멈추거나 버벅인다고 연락을 받고 확인해보면 상태를 바꾸고 다음 행을 수정하고 메모를 적는 등의 이어지는 업무를 할 때가 대부분이었습니다. 그래서 수정 동작은 화면에 먼저 반영하고 실패했을 때만 되돌리는 행 단위 optimistic 훅을 만들어 적용했습니다.

```tsx
const useOptimisticRow = <T extends { id: IdType }, PatchType>({ setRows, requestUpdate }: any) => {
  const update = async ({ id, patch }: { id: IdType; patch: PatchType }) => {
    setRows((prev: T[]) => prev.map((r) => (r.id === id ? { ...r, ...patch } : r)));
    await requestUpdate({ id, patch }); 
  };
  return { update  };
};

const { update } = useOptimisticRow<User, Pick<User, "status">>({
  setRows,
  requestUpdate: ({ id, patch }) => api.updateUser(id, patch),
});
const onChangeStatus = (rowId: string, nextStatus: User["status"]) => {
  update({ id: rowId, patch: { status: nextStatus } });
};
const columns=[
  cell: ({ row, getValue }) => (
      <SelectCell
      value={getValue()}
      onChange={(next) => onChangeStatus(row.original.id, next)}
    />
  )
]
```

## 10만 건 데이터 가상화

보안 로그 페이지에서 확인 하는 데이터는 평균 10만 건 이상이었습니다. 전체 데이터를 스크롤로 확인하고 싶어했는데, 데이터가 쌓일 수록 화면이 느려지면서 브라우저가 멈추는 문제가 발생했습니다. 100,000개 행 전체가 로드된다면 DOM에 100,000개 행이 생성되어있는 것입니다. 렌더링, 레이아웃, 페인트에 사용되는 메모리가 그만큼 많아지기 때문에 DOM의 개수는 브라우저의 성능과 관련이 있습니다.

가상화는 이 문제를 DOM 개수 자체를 줄여서 해결합니다.

### 가상화

virtualization(가상화)은 화면에 보이는 행만 렌더링하고, 나머지는 스크롤 위치에 맞춰 필요해질 때만 렌더링하는 방식입니다. [react-window](https://react-window.vercel.app/), [react-virtuoso](https://virtuoso.dev/), [@tanstack/virtual](https://tanstack.com/virtual/latest)등 다양한 가상화 라이브러리가 사용되고 있습니다. 저는 TanStack Table을 사용하고 있기도 하고, id 기반 key로 DOM 안정성을 보장하기 좋아서 @tanstack/react-virtual을 선택했습니다.

구조는 TanStack Table로 행/셀 모델을 만들고, 실제 렌더링은 @tanstack/react-virtual이 담당하도록 분리했습니다.

```tsx
const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() });
const rows = table.getRowModel().rows;
const parentRef = useRef<HTMLDivElement | null>(null);
const virtual = useVirtualizer({
  count: rows.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => rowHeight,
  getItemKey: (i) => rows[i]?.id ?? i,
});

return (
  <div ref={parentRef}>
    <div>
      {virtual.getVirtualItems().map((vr) => (
        <div key={vr.key}>
          {rows[vr.index]!.getVisibleCells().map((c) =>
          <div key={c.id}>{flexRender(c.column.columnDef.cell, c.getContext())}</div>
          )}
        </div>
      ))}
    </div>
  </div>
);
```

가상화 테이블에서 Header는 Row와 분리되기 때문에 보통 스크롤 영역 밖에 고정해두고, Body만 가상화 렌더링하는 형태로 구성했습니다. Header와 Body의 컬럼 너비가 틀어지지 않도록 TanStack Table의 header.getSize() / cell.column.getSize() 값을 기준으로 동일하게 width를 적용해 동기화할 수 있습니다. 컬럼 리사이징이 있는 경우에도 헤더만 커지고 바디는 그대로라 화면이 깨지는 일이 없도록 헤더/바디가 동일한 사이즈를 가지게 하는 것이 핵심이었습니다.

### 가상화 적용 시 주의할점

가상화는 DOM을 계속 재활용하면서 행을 교체 렌더링하는 방식으로, 테이블처럼 인터랙션이 많은 UI에서는 문제가 생길 수 있어서 주의해야합니다.

- index 사용 금지

정렬, 필터, 페이지 변경 등의 이유로 index는 계속 바뀝니다. key를 index로 두니 클릭한 행과 실제 데이터가 엇갈리거나, 인터랙션에서 버그가 발생했습니다. @tanstack/react-virtual에서 제공하는 getItemKey를 사용해 선택, 편집 상태를 전부 rowId 기준으로 관리했습니다. 화면이 바뀌거나 데이터 순서가 바뀌었을 때 상태가 다른 row로 이동하는 문제를 방지할 수 있었습니다.

- 임시 입력값 유지

가상화 테이블에서 입력 셀을 만들 때 입력 중인데 스크롤하면 값이 사라지는 문제가 있습니다. 가상화는 스크롤할 때 DOM을 교체하는 방식이기 때문에 input value가 있었는데? 스크롤을 하면 사라집니다!

저는 이 문제를 막기 위해 변경된 값들만 따로 모아서 관리했습니다. 원본 데이터는 서버에서 내려온 값, 편집 중인 값은 훅으로 별도 입력값을 보관하고 저장 성공 시에 원본과 동기화되도록 했습니다.

## 마무리
관리자 대시보드에서 테이블은 단순히 데이터 목록을 보는 용도가 아니라 그 데이터를 수정하거나 분류하는 등 업무의 중심이었습니다. 처음에는 모든 기능을 한 컴포넌트에 넣어 공통화했지만, 화면마다 요구사항이 달라질수록 옵션과 분기가 늘어 유지보수가 어려워졌습니다.

가장 고민했던 건 테이블의 책임을 어디까지로 둘지, 그리고 상태와 데이터를 어떻게 나눌지였습니다. 정렬, 필터, 페이지네이션 같은 상태는 테이블 내부에 묶기보다 화면에서 관리하고, 테이블은 렌더링에 집중하도록 역할을 나눴습니다. 그래서 공통 테이블을 한 컴포넌트로 만들기보다 컬럼/셀/기능을 조립할 수 있는 구조가 더 좋아보였습니다. 공통으로 묶을 부분과 화면마다 다르게 가져갈 부분을 균형 있게 책임을 분리하니 변경 대응이 훨씬 쉬웠습니다.

컴포넌트를 잘 만든다는 건 UI를 예쁘게 만드는 게 다가 아닙니다. 기능이 늘어나고 요구사항이 바뀔 것을 전제로 구조를 유지할 수 있게 설계하는 것이 더 중요하다는 걸 배운 경험이었습니다.