---
layout: post
title: "Github Blog 만들기 [1]"
summary: github blog 생성하기
date: 2024-03-01 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

GitHub Pages 블로그 서비스인 github.io 블로그를 만들어봅시다.

늘어나는 신기술, 개발 컨텐츠들이 끊임없이 쏟아지고 있습니다. 이 컨텐츠들을 접하며 항상 보기만 하고 넘겨서 기억에 남지도 않고 한번 휙 보고 말게 되는 것 같습니다. 또 한참 삽질한 것들도 대충 노션에만 남겨두기만 하니 같은 상황에 처했을 때 해결방법은 기억도 나지않고 찾기 힘든 것들이 너무 아쉬웠습니다.
앞으로는 신기술, 공부한 것들, 경험한 것들을 기록을 남겨보기위해 블로그를 시작하게 되었습니다.

_mac Os 기준으로 작성되었습니다_

# github repogitory 생성하기

우선 github에 가입을 해줍니다.

홈에 들어와서 페이지 우측 상단에 + 버튼을 눌러서 new repository 를 클릭해서 레파지토리를 만들 수 있는 페이지로 들어와줍니다.
Repository name 에 username.github.io 를 입력해 주고 create repository 를 클릭해서 레파지토리를 생성해 줍니다.
![](/assets/images/2024-03-02-jekyll-github-blog-1/01.png)

# github pages 자동 배포 설정하기

생성한 레파지토리의 페이지에서 settings 탭에 들어가서 pages 메뉴에서 Branch를 눌러 소스 푸시 되면 자동으로 배포를 할 브랜치를 선택하고 save 를 눌러 저장을 합니다. 저는 main브랜치로 선택했습니다.

# 소스 clone & 테스트 파일 작성 하기

생성한 레파지토리를 로컬에 클론받아주겠습니다. 생성한 레파지토리의 페이지에서 화면에 나오는 주소를 클론해주시면 됩니다
![](/assets/images/2024-03-02-jekyll-github-blog-1/03.png)
![](/assets/images/2024-03-02-jekyll-github-blog-1/02.png)

터미널로 진행할 때
'git clone url'
저는 vscode를 사용하고 있어서 vscode git 기능을 이용합니다. 코드를 편집하려면 코드 편집기에서 진행하는게 편해서 vscode 설치를 추천드립니다.
![](/assets/images/2024-03-02-jekyll-github-blog-1/04.png)
vscode로 진행할 떄
'clone Repository > url 입력 후 clone from GitHub' > open folder

그리고 test 를 위해 index.html 을 하나 만들어 주고 다음과 같이 입력을 해주겠습니다. vscode 에서는 ! 를 입력하면 html 기본 구조가 나와서 또 사용하기 편리합니다. test blog라고 작성하여 커밋 푸시를 해보겠습니다.
![](/assets/images/2024-03-02-jekyll-github-blog-1/05.png)

# 최종 확인하기

다시 github으로 돌아가서 actions탭에 들어가 보면 자동으로 빌드, 배포되고 있는 게 보이고 끝나면
`https://username.github.io/`링크로 접속해서 확인해볼 수 있습니다!
![](/assets/images/2024-03-02-jekyll-github-blog-1/06.png)
![](/assets/images/2024-03-02-jekyll-github-blog-1/07.png)

다음은 jekyll 셋팅으로 돌아오겠습니다.


참고 : <https://docs.github.com/en/pages/quickstart>
