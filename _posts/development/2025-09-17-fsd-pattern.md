---
layout: post
title: FSD 드세요
summary: git branch 전략들
date: 2025-09-17 09:41:33 +09:00
categories: development
tags: fsd frontend Feature-Sliced-Design React_아키텍처_패턴 프로젝트_구조 ddd 도메인_주도_설계
---

## FSD 드세요!!!

프로젝트를 할 때마다 폴더 구조가 달라져서 혼란스러웠던 경험, 누구나 있으실 거예요. 명확한 기준이 없다 보니 프로젝트를 새로 맡은 사람은 물론, 만든 본인조차 잠깐 딴 일 했다 돌아오면 “이 파일 어디 있었지…?” 하게 돼요. 저도 그랬습니다. 그러다 FSD(Feature-Sliced Design) 라는 아키텍처를 알게 되었습니다.

FSD패턴을 공부하면서, 폴더 구조를 그때마다 다르게 기준을 두지 않고 도메인 중심으로 안정적이게 고정하는 방향으로 고민을 하게 되었습니다.


## FSD(Feature-Sliced Design) Pattern

FSD는 레이어(Layer) → 슬라이스(Slice) → 세그먼트(Segment) 3단계로 코드를 나눠서, 폴더 뎁스를 3단계 이내로 제한하고, 기능(도메인) 기준으로 관리하는 패턴입니다.
이 구조의 가장 큰 특징은 폴더의 깊이를 3단계로 제한한다는 점이에요.

흔히 발생하는 `../../../../` 무한 참조 문제나, 한 폴더에 파일이 몰려서 관리가 어려운 상황을 깔끔하게 정리할 수 있습니다.

## 핵심 철학

- 도메인 우선: 유저/게시글/코멘트 처럼 **현실의 개념(Entities)**으로 코드를 묶기.

- 단방향 의존성: shared → entities → features → widgets → pages → app 순으로 참조. 역방향은 금지!

### 레이어(Layer)

도메인에 가까울수록 아래, 화면/라우팅에 가까울수록 위
* **App**: 전역 설정, Provider, Router, Client 같은 HOC가 위치
* ~~Processes~~: 여러 페이지가 연결된 플로우(예: 회원가입 1 → 2 → 3 단계), 위젯으로 대체되어 사용하지 않음
* **Pages**: 브라우저 주소 단위로 분리된 컴포넌트, 라우팅에 따라 나뉘는 페이지
* **Widgets**: 여러 Feature를 묶은 단위로, 레이아웃 같은 틀을 담당
* **Features**: 사용자 행동 단위(로그인, 좋아요, API 호출 등)
* **Entities**: 데이터의 명사적 단위(유저, 게시물, 댓글). API를 통해 데이터를 조회
* **Shared**: 여러 곳에서 공유되는 유틸, 훅, 타입, 아이콘, 컴포넌트 등

### 각 세그먼트 쪼개기

각 레이어 아래 폴더를 세그먼트로 세분화합니다. 이름은 팀 취향을 따르되 보통 아래 4가지를 자주 사용합니다.

- ui/: 프레젠테이션 컴포넌트(스타일, 뷰 로직)

- model/: 상태, 셀렉터, 비즈니스 로직(RTK slice 등)

- api/: API 클라이언트, 쿼리/뮤테이션 정의

- lib/: 도메인 헬퍼, 유틸(순수 함수 선호)

## Examples

### 폴더 트리 예시(React + RTK 기준)
```
src/
  app/
    providers/
    router/
    index.tsx
  pages/
    posts/
      ui/Page.tsx
      index.ts
  widgets/
    post-list/
      ui/PostList.tsx
      model/usePostList.ts
      index.ts
  features/
    like-post/
      ui/LikeButton.tsx
      model/slice.ts
      api/likePost.ts
      index.ts
  entities/
    post/
      ui/PostCard.tsx
      model/postSlice.ts
      api/getPosts.ts
      lib/format.ts
      index.ts
    user/
      ...
  shared/
    ui/Button.tsx
    hooks/useDebounce.ts
    utils/date.ts
    icons/index.ts
    config/env.ts
```

각 폴더의 index.ts는 Public API(외부로 내보낼 것만 re-export)

외부에서 import할 땐 폴더 루트만 보도 “깊은 경로” 참조를 원천 차단합니다.

```tsx
// ❌
import PostCard from '@/entities/post/ui/PostCard';
import like from '@/features/like-post/model/slice';

// ✅
import { PostCard } from '@/entities/post';
import { LikeButton } from '@/features/like-post';
```

## 버튼

버튼의 껍데기(UI), 동작(행동), **내용물(데이터)**를 분리합니다.

- Shared: 공용 버튼 컴포넌트(모양·인터랙션)

- Features: 그 버튼이 수행할 행동(좋아요)

- Entities: 버튼이 보여줄 데이터(좋아요 수)

```tsx
<Shared.Button
  onClick={likeFeature.api.like}
  icon={shared.icon.fork}
  data={likeEntity.model.likeCount}
/>

```


이렇게 분리하면 역할과 책임이 명확히 분리되고, 서로 간의 불필요한 임포트를 막음으로써 재사용성은 높이고 의존성은 낮출 수 있습니다.~~(응높결낮 ㅎㅎ)~~

## 의존성 규칙을 코드로도 강제

ESLint로 깊은 경로 import 금지와 역방향 의존 금지를 걸어두면 협업할 때 더욱 편해집니다.

```// .eslintrc.js
module.exports = {
  rules: {
    'no-restricted-imports': [
      'error',
      {
        patterns: [
          // 내부 세그먼트로의 '깊은 경로' 차단
          '**/*/ui/*',
          '**/*/model/*',
          '**/*/api/*',
          '**/*/lib/*',
        ],
      },
    ],
  },
  settings: {
    'import/resolver': { typescript: {} },
  },
};

```

경로 별칭도 필수 ✨

```json // tsconfig.json
{
  "compilerOptions": {
    "baseUrl": "src",
    "paths": {
      "@/*": ["*"]
    }
  }
}
```

### 마이그레이션 

FSD의 또 다른 장점은 점증적 적용입니다. 하나씩 순서대로 적용하다보면 더 깊이 이해할 수 있습니다.

경로 별칭(@/*) 부터 잡아서 상대경로를 간소화 하기 →
shared entities features widgets pages app 순으로 얕게 폴더만 나누기 →
각 폴더 루트에 index.ts Public API를 만들고, 외부 import를 바꾸기 →
ESLint 깊은 경로 금지 규칙 추가, CI에서 체크 → api/model/ui/lib 세그먼트를 천천히 분리하며 테스트 진행하기

처음부터 완벽 분리하겠다는 마음보단 “경로 단절 + Public API” 두 가지만 먼저 적용 후 나머지는 시간에 맡겨봅시다.


### 마무리

폴더 구조는 취향 차이가 크지만, FSD는 “자유”가 아니라 “방향”을 제시한다고 생각합니다.

FSD 공식 문서는 큰 가이드라인만 제시하고, 세부 구현은 팀마다 다릅니다. 결국 실무에서 가장 중요한 건 **팀 합의와 컨벤션 정립**이에요. 두 가지만 지키면 나머지는 팀에 맞게 유연하게 바꿔도 충분합니다.

1)도메인 중심으로 묶기, 2) 단방향 의존을 지키기.


폴더 구조에 매번 고민하셨다면, 이제는 **FSD 드세요.**
프로젝트가 커질수록 FSD의 장점은 더 빛나게 됩니다.

