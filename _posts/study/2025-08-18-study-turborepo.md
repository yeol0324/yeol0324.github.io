---
layout: post
title: "Turborepo 정복하기"
date: 2025-08-18 22:01:24 +09:00
summary: "Turborepo로 프로젝트 관리와 빌드 속도 최적화"
categories: study
tags: turborepo monorepo
---

## Monorepo

Monolithic Repositories, 단단히 짜여 하나로 되어 있는 레파지토리.
즉, 여러 프로젝트를 하나의 레포 안에서 함께 관리하는 방식입니다.

최근에 monorepo를 도입했다는 얘기를 정말 많이 듣는데, 저도 보면서 이런 생각이 들었어요.

<span class="h-box-yellow">"비슷한 프로젝트를 한 곳에 모아두면 기억하기도 쉽고 관리도 편하겠다!"</span>


그래서 제 프로젝트에도 모노레포를 도입해보기로 했습니다.

모노레포에는 Turborepo, Lerna, Nx 등 다양한 도구가 있는데, 저는 그중에 Vercel에서 개발하고 있는 **Turborepo**를 선택했습니다.
제 프로젝트들이 대부분 JavaScript 기반이라 호환도 잘 맞고, 무엇보다 강력한 캐싱과 증분 빌드 기능을 제공해서 빌드 속도가 정말 빠르다고 하더라고요.
게다가 점진적으로 마이그레이션이 가능하다는 점도 큰 장점이었습니다.

사실 이전 프로젝트가 Turborepo로 구성되어있었는데,  Turborepo를 잘 활용하지 못해 빌드가 10\~20분이나 걸려서 늘 답답했던 기억이 있어요.
이번에는 캐싱을 제대로 활용해 개선해서 해결해보면 좋겠다 싶어서 다시 선택하게 되었습니다.
이제 본격적으로 프로젝트를 구성하기 전에 먼저 Turborepo를 조금 더 깊게 뜯어보기로 했습니다. 🧐

## Turborepo 뜯어보기 🔍

*내부 아키텍처 · DAG 스케줄링 · 캐시 메커니즘 분석*

Turborepo는 단순히 모노레포 관리 툴이 아니라, **고성능 빌드 시스템**입니다. JavaScript/TypeScript용 고성능 빌드 시스템으로, 단일 프로젝트에도 적용할 수 있고 모노레포 확장에도 최적화되어 있습니다.

Rust로 작성된 코어 엔진을 기반으로, DAG 스케줄링·캐싱·병렬화를 통해 대규모 프로젝트에서도 빌드를 효율적으로 관리합니다.


### 실행 원리

`turbo run <task>`를 실행하면 이런 순서로 진행됩니다.

1. workspace 탐색

   `pnpm-workspace.yaml`, `package.json`의 workspaces 설정을 읽어 어떤 패키지가 있는지 파악

2. turbo.json 파이프라인 규칙 적용

   ```js
   {
     "pipeline": {
       "build": {
         "dependsOn": ["^build"],   // 부모 패키지 빌드 먼저
         "outputs": ["dist/**"]     // 결과물 캐시
       },
       "dev": {
         "cache": false,            // dev는 캐싱 안 함
         "persistent": true         // 서버 계속 실행
       }
     }
   }
   ```
   * 각 task의 의존성 (dependsOn)
   * 캐싱할 아웃풋 (outputs)
   * 병렬 실행 가능 여부


3. 의존성 그래프 구축

   * 패키지 간 관계를 DAG(Directed Acyclic Graph) 형태로 정리
   * `web → ui → utils`
     → `turbo run build` 실행 시 `utils/build → ui/build → web/build` 순서로 실행


4. task 실행 & 로그 관리

   * DAG 순서에 맞춰 `pnpm run <task>` 실행
   * 병렬 가능한 건 동시에 실행



## turbo run build 실제 흐름

Turbo 동작 방식을 이해하기위해 시뮬레이션으로 돌려본 실행 흐름을 로그로 정리해봤습니다.

* 콜드 캐시(최초 빌드)  전부 실행 후 캐시에 기록 →
* 변경 없음(풀 캐시 히트) 전부 스킵, 1초 이내 완료 →
* 부분 변경(ui만 수정) `ui`와 `web`만 리빌드, 나머지는 캐시 사용 →
* 리모트 캐시 활용 팀원이 빌드한 결과까지 가져와서 로컬에서도 바로 복원

💥 Turbo의 강력한 “정말 필요한 부분만 다시 빌드”


## turbo 설치 & 구조 살펴보기

저는 **pnpm**과 함께 사용했습니다.

```bash
pnpm dlx create-turbo@latest .
```

> 설치 명령어 뒤에 `.`을 붙이면 현재 위치에 바로 생성됩니다. (이미 파일이 있으면 덮어쓰니 주의!)

생성 후 주요 구조는 이렇습니다.

* apps/ → 실제 서비스 앱 (ex `apps/web`, `apps/docs`)
* packages/ → 여러 앱에서 공유할 코드 (ex `packages/ui`, `packages/tsconfig`)
* turbo.json → 파이프라인 규칙
* package.json (root) → 워크스페이스 관리
* tsconfig.json → 루트 타입스크립트 설정

동작 흐름은 간단합니다.

* `pnpm dev` → apps/\* 안의 프로젝트들을 동시에 실행
* `pnpm build` → 캐싱 기반으로 필요한 것만 빌드



### Turborepo의 실행 구조

겉으로는 `npx turbo run build` 같은 CLI 명령어를 사용하지만, 실제로는 **Node + Rust Core** 구조입니다.

* **Node CLI (`@turbo`)**
  우리가 실행하는 건 Node 스크립트입니다. 이 부분은 명령어 파싱 → Rust 실행 파일 호출 역할을 합니다.

  ```js
  // node_modules/@turbo/bin/run.js
  #!/usr/bin/env node
  require('../dist/cli').run();
  ```

* **Rust Core (`turbo-engine`)**
  DAG 생성, 캐시 계산, 병렬 실행 등 성능이 중요한 부분은 Rust로 작성되어 있습니다.
  Node는 얇은 껍데기, 실질적인 엔진은 Rust!


### turbo.json 파이프라인 → DAG 변환

`turbo.json` 설정은 단순 key-value가 아니라 \*\*실행 그래프(DAG)\*\*로 해석됩니다.

```json
{
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"],
      "cache": true
    },
    "test": {
      "dependsOn": ["build"],
      "cache": true
    }
  }
}
```

* `dependsOn`:

  * `"^build"` → 상위 패키지의 build를 먼저 실행
  * `"build"` → 자기 자신 build 후 실행
* `outputs`: 캐싱 대상 경로
* `cache`: true면 결과물이 해시 기반으로 저장/복원

👉 이 설정을 기반으로 Rust 엔진이 DAG를 만듭니다.

###  DAG 스케줄링

Turborepo는 DAG를 만든 뒤 **위상 정렬(Topological Sort)** 알고리즘으로 task 실행 순서를 정합니다. Rust 내부 코드를 열어봤습니다.

```rust
fn schedule_tasks(dag: DAG) {
   let mut queue = VecDeque::new();
   for node in dag.nodes() {
      if node.in_degree == 0 {
         queue.push_back(node);
      }
   }
   while let Some(task) = queue.pop_front() {
      run_task(task); // 실제 실행
      for child in task.dependents {
         child.in_degree -= 1;
         if child.in_degree == 0 {
            queue.push_back(child);
         }
      }
   }
}
```

* 진입 차수(`in_degree`) 0인 노드 → 큐에 삽입
* 실행 후 자식 노드 차수 감소
* 차수가 0이 되면 실행 가능 상태로 전환

이 구조 덕분에, 의존 없는 task들은 **병렬 실행**되고, 필요한 순서는 보장됩니다.

### Task 실행 

(Node → Rust → Shell)

[참고](https://turborepo.com/docs/reference/run?utm_source=chatgpt.com)

각 노드는 `pnpm run build` 같은 커맨드를 실행해야 하죠.
Rust 코어는 Node로 내려보내지 않고, 직접 프로세스를 띄웁니다.

```rust
fn run_task(task: Task) {
   let status = Command::new("pnpm")
       .arg("run")
       .arg(&task.name)
       .status()
       .expect("failed to execute process");
   if !status.success() {
       panic!("Task failed: {}", task.name);
   }
}
```

즉, DAG 스케줄링 + 프로세스 실행이 Rust 엔진 안에서 일어나는 겁니다.

## 캐싱 메커니즘

Turbo의 캐싱은 단순 파일 해시가 아니라 **입력 조건 전체**를 해시 키로 삼습니다.

```ts
// pseudo code
function createCacheKey(task) {
  return hash([
    task.sources,          // 소스 파일 해시
    task.outputs,          // 산출물 경로
    task.env,              // 환경 변수
    task.lockfile,         // pnpm-lock.yaml
    task.dependencyHashes, // 상위 task 해시
  ]);
}
```
> https://github.com/vercel/turborepo/tree/main/crates/turborepo-cache

* 로컬 캐시: `node_modules/.cache/turbo`
* 원격 캐시: Vercel / S3 / Redis

결과물은 tarball로 묶여 저장되며, 다음 실행 시 동일 해시라면 **빌드 스킵** 후 복원됩니다.
 소스, 종속성, 환경변수 중 하나라도 바뀌면 캐시 무효화. 바뀐 게 없으면 그대로 복원해서 skipped로 표시돼요.


### 원격 캐시 (Remote Cache)

팀 단위 속도 향상의 핵심은 원격 캐시입니다.

* 빌드 완료 후 → 결과물 tarball 업로드 (해시 키 기반)
* 다른 환경에서 실행 시 → 해시 조회 → 있으면 바로 다운로드

(Remote Cache)

Vercel,S3 같은 저장소를 붙이면 다른 개발자가 빌드한 결과도 가져와 바로 복원 가능. 팀 단위로 “한 번 빌드 → 다 같이 재사용” 느낌이라 속도가 훨씬 빨라집니다.

```bash
$ turbo run build
• Remote cache enabled
• Restored ui:build from remote cache
```

CI/CD에서 빌드 시간을 획기적으로 줄일 수 있는 이유가 바로 이것입니다.


### 병렬 실행과 워커 풀

Turbo는 CPU 코어 수만큼 워커를 띄우고, DAG에서 독립적인 task를 병렬 실행합니다.

* `utils/build`와 `api/build` → 독립 → 동시에 실행
* `ui/build`는 `utils/build` 이후 실행
* `web/build`는 `ui/build` 이후 실행

`--parallel` 옵션을 주면 더 많은 병렬 실행을 강제할 수도 있습니다.

---


## 로그 구조 (JSON 기반)

터미널에서 보는 로그는 사람이 읽기 좋게 포맷된 버전이고, 실제 내부 로그는 JSON 포맷으로 출력할 수 있습니다.

```bash
$ turbo run build --log-order json
{
  "task": "utils#build",
  "status": "RUNNING",
  "cache": "MISS"
}
{
  "task": "utils#build",
  "status": "SUCCESS",
  "duration": "3.2s"
}
```

CI/CD에서는 이 로그를 활용해 실행 그래프 시각화도 할 수 있습니다.