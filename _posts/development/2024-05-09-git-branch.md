---
layout: post
title: 우리가 쓴 깃 전략과 git flow들
summary: git branch 전략들
date: 2024-05-09 09:41:33 +09:00
categories: development
tags: git
---

깃 사용법, 브랜치 전략 등이 왜 필요할까요? 저는 팀에 처음 합류됐을 때 깃 관리때문에 사건이 많이 일어났습니다. 그래서 저희가 깃 브랜치 전략을 만들게 된 이유와 현재 사용하고 있는 전략을 정리해보고 여러가지 브랜치 전략들을 알아보고 비교해보려고 합니다.

# 무지성 Git 사용

팀에 합류됐을 때, 인력 구성도 완전하지 못하고(대거 퇴사가 있었다고 함) 한명씩 투입되고 있던 시기였습니다. 진행하고 있는 서비스가 총 3개인 프로젝트였고 교사, 학생, 학부모, 서버, 안드로이드 이렇게 총 5개로 레파지토리가 나누어져있었습니다. 형상관리는 gitlab을 사용을 하고 있었지만 개발자가 몇 명 없고 초기 개발 단계다보니 branch 전략은 아예 없었고 무지성으로 풀 푸시 풀 푸시··· 충돌나면 알아서 백업해서 다시 푸시··· git을 사용하는 의미도 없던 시절이 있었습니다. 사람이 너무 바쁘다는 핑계로 더 좋은 방법을 찾아보지 못했던 것 같습니다. 문제는 상용 서비스 오픈이 얼마 남지 않았을 때였습니다. 다들 작업량이 많았고 충돌나면 짜증이 나겠죠. 한분이 코드를 합치는 중에 전 작업자의 코드를 다 날려버리는 사건이 있었습니다. 저희는 이 사태를 계속 지속할 수 가 없었고 소 잃고 외양간 고치기라도 시작을 했습니다.

# brach 전략의 도입

먼저 규칙은 무조건 브랜치를 따서 작업을 하자! 였습니다. 브랜치를 따서 작업을 하지 않으면 코드가 충돌이 났을 때 pull, push 둘다 못하는 상황도 발생하는데, 브랜치를 따서 작업을 하면 리베이스를 하든 머지 컴플릭트를 하나씩 잡아주는 것은 할 수 있습니다.
이렇게 브랜치에 다들 적응이 돼서 회의를통해 저희만의 브랜치 전략을 만들어서 사용을 했습니다.

먼저 기준 브랜치 ( release ) 와 개발 브랜치 ( devqa ) 총 2개로 나누어 관리를 했습니다.

<span class="h-yellow">main : 원격 서버 기본 브랜치</span><br>
기본 브랜치에는 많은 제약이 있어 ( squash commit 등 ) main 은 사용하지 않음.

<span class="h-yellow">release : 상용 배포 브랜치</span><br>
배포되는 대상 브랜치, Merge Request의 대상

<span class="h-yellow">devqa : 개발 운용 브랜치</span><br>
개발브랜치 각 개발자들의 개발 결과물을 개발서버에 배포할때 사용<br>
** 항상 통합배포 이후 리셋이 되며, release에서 브랜치 생성 

# 우리만의 flow

그래서 우리가 정한 flow 는 이렇습니다.

1. 메인 원격 저장소에서 개인 Fork 생성
2. 개인 Fork 에서 기능별, 이슈별 Branch 생성 (branch: release 기준으로 생성)
3. 메인 원격 저장소(branch: devqa)에 머지
4. QA 완료 후 메인 원격 저장소(branch: release)에 브랜치 머지리퀘스트 생성
5. 메인 원격 저장소(branch: release) 브랜치 내가 포크뜬 브랜치에 rebase

일반적으로 알려진 flow 들과는 많이 다르지만 저희 배포 프로세스에 맞게 회의를 통해 정해졌습니다. 당장 Git Flow 도입하자! Gitlab Flow 도입하자! 하는 것보다는 필요에 의해서 회의를 하고 직접 규칙을 만들어 놓으니 실천하기도 좀 더 수월했던 것 같습니다.

# 알려진 Git 전략들
google 검색어 탐색을 통해 확인해봐도 git flow 에 대한 관심도가 제일 많은 것 같습니다. 아예 무지하던 시절의 저도 git flow는 들어봤었으니까요.
![](/assets/images/20240509/git-google.png)

## Git Flow
먼저 가장 많이 알려지고 관심도가 높은 [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)를 보겠습니다.
브랜치는 총 5개로 이루어져있습니다.

__Main Branches__<br/>
<span class="h-yellow">Master</span> : 출시 가능 버전 상태<br/>
<span class="h-yellow">Develop</span> : 출시 버전 개발<br/>

__Supporting Branches__<br/>
<span class="h-yellow">Feature</span> : 추가되는 기능을 개발 (from develop)<br/>
<span class="h-yellow">Release</span> : 출시 버전 준비 (from develop)<br/>
<span class="h-yellow">Hotfix</span> : 출시 후 발생한 버그 수정 ( from maseter )<br/>

때에 따라서 다양한 브랜치로 나누어져있습니다. 먼저 없어지지 않는 두 개의 브랜치를 메인으로 진행합니다. 출시 가능 버전 상태인 Master 브랜치에서 develop 브랜치를 생성후, 이후 출시할 버전의 개발을 진행하고 develop에 merge 를 해줍니다. 중간중간 들어오는 신규 기능들은 develop에서 feature를 생성 후 기능 개발 후 다시 develop에 합쳐줍니다. 기능 개발이 모두 merge가 되었다면 develop 브랜치에서 release 브랜치를 생성합니다. release에서 QA 를 진행하면서 출시 버전을 준비하는데, 여기서 발견된 버그들은 release에 바로 수정을 합니다. 마지막으로 출시 버전 준비가 끝났다면 master 로 merge 후 release tag를 생성합니다. master 에 merge 되는 시점이 곧 서비스 배포라고 볼 수 있습니다. 그래서 자동배포를 구현할 때 master에 이벤트를 감지해서 자동으로 빌드 배포를 설정을 해두는 것이죠!

![](/assets/images/20240509/git-flow.png)


## Github Flow

[Github flow](https://docs.github.com/en/get-started/using-github/github-flow)는 브랜치가 2개만 존재합니다. 

<span class="h-yellow">Main</span> : 언제든 출시 가능한 상태. QA가 완료된 상태의 코드만 merge함<br/>
<span class="h-yellow">other</span> : 기능 개발 등 자유, 명시적인 브랜치명과 커밋메시지 ( from Main )

2개라고 했지만 항상 출시가 가능한 안정적인 기준인 main 브랜치와, 개발할 브랜치로 나누어져있습니다. main에서 새로운 브랜치를 생성합니다. 여기서 개발 브랜치명과 그 커밋 메시지는 누군가 봤을 때 한번에 확인이 가능하도록 자세히 쓰는 것이 핵심입니다. 생성한 브랜치에서 개발이 완료되면 PR( Pull Request ) 생성합니다. PR 리뷰까지 완료 후 Main에 merge, 사용한 브랜치는 삭제합니다. GitHub 웹이나 Desktop 앱에서 GitHub Flow를 사용하기 쉽도록 지원한하니 확인해보셔도 좋을 것 같습니다.


# 최종 요약
Git Flow
· 배포 주기가 잦지 않은 큰 프로젝트<br/>
· git에 많이 익숙해져있을 때
· 배포가 잦지 않을 때

GitHub Flow

· 브랜치가 main 뿐이고 간단함<br/>
· git에 익숙하지 않은 사람이 많을 때<br/>
· 규모가 작은 프로젝트<br/>
· 기능 배포나 빨리 대응해야하는 이슈가 많을 때<br/>

다양한 브랜치 전략을 알아보니 정말 처음에 쓰고 있던 방식은 git을 사용하는 게 아닌 코드 저장소로만 사용을 했던 것 같네요. 지금 당장은 불편한 게 없어서 지금 사용 방법으로 한동안 진행이 될 것 같습니다. Git Flow는 언젠가 한번 꼭 사용해보고 싶었는데 회사 밖에서 사용해볼 수 있을 것 같습니다. 😅

그래도 새로운 프로젝트가 시작되거나 여럿이 작업을 해야하는 상황에 더 좋은 방식을 선택할 수 있게, 언제든 새로운 정책을 만나면 적응할 수 있게 한 계단 성장한 것 같습니다.



---
- <https://nvie.com/posts/a-successful-git-branching-model/>
- <https://docs.github.com/en/get-started/using-github/github-flow>
- <https://techblog.woowahan.com/2553/>