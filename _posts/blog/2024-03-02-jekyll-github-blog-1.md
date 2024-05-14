---
layout: post
title: "Github Blog 만들기 [1]"
summary: github blog 생성하기
date: 2024-03-01 10:06:52 +0900
categories: blog
tags: blog github-page
---

" 공부한 것들, 경험한 것들을 기록하기 "

GitHub Pages 블로그 서비스인 github.io 블로그 만들기 시리즈 입니다.

_mac Os 기준으로 작성되었습니다_

# GitHub Pages?

> GitHub Pages are public webpages hosted and published through GitHub. The quickest way to get up and running is by using the Jekyll Theme Chooser to load a pre-made theme. You can then modify your GitHub Pages' content and style.

GitHub 페이지는 GitHub를 통해 호스팅되고 게시되는 공개 웹페이지입니다. 시작하고 실행하는 가장 빠른 방법은 Jekyll 테마 선택기를 사용하여 미리 만들어진 테마를 로드하는 것입니다. 그런 다음 GitHub 페이지의 콘텐츠와 스타일을 수정할 수 있습니다.

예전에 퍼블리싱한 포트폴리오를 호스팅하기위해 GitHub Pages 서비스를 사용해 보았습니다. repository에 소스코드만 올려두고 Pages 설정만 조금 해주면 무료로 호스팅을 할 수 있어서 사용을 했었는데요, 많은 분들이 블로그로도 사용하고 있는 것을 보고 시작하게 되었습니다.

# Github Repogitory 생성

우선 github에 가입을 해줍니다.

로그인 후 나오는 메인 페이지에서 우측 상단에 있는 + 버튼을 클릭하면 여러가지 메뉴가 나오는데요,<br>
<code>new repository</code> 로 repogitory 생성 페이지로 이동합니다.
Repository name 에는 {username}.github.io 를 입력해 주고 create repository 를 클릭해서 레파지토리를 생성해 줍니다.

📍필수📍 자신의 <span class="h-yellow">github username</span> 으로 작성을 해야됩니다.

![](/assets/images/2024-03-02-jekyll-github-blog-1/01.png)

# 자동 배포 설정

생성한 레파지토리의 페이지에서 settings 탭에 들어가면 좌측에 pages 메뉴가 있습니다. pages 메뉴에서 Branch 아래에 토글 박스를 열면 브랜치 리스트를 확인할 수 있습니다. 푸시이벤트를 받아 자동으로 배포 할 브랜치를 선택하고 save 를 눌러 저장을 합니다. 브랜치를 하나도 생성하지 않았기 때문에 main 브랜치 하나만 있죠. main 브랜치로 선택했습니다.

![](/assets/images/2024-03-02-jekyll-github-blog-1/03.png)

# 프로젝트 클론

생성한 레파지토리를 로컬에 클론받아주겠습니다. 생성한 레파지토리의 페이지에서 화면에서 <>code 초록색 버튼을 클릭하면 레파지토리 주소를 복사할 수 있습니다.
복사한 주소로 레파지토리를 클론해주시면 됩니다.

터미널로 진행할 때
```shell 
git clone https://github.com/${username}/${username}.github.io
```

저는 vscode를 사용하고 있어서 vscode git 기능을 이용합니다. 코드를 편집하거나 블로그 작성 시에도 코드 편집기가 편하기때문에 편집기 설치를 추천드립니다.

vscode로 진행할 때
1. clone Repository
2. url 입력 후 clone from GitHub
3. open folder

# 테스트 파일 작성

이제 Github Pages를 사용할 준비는 다 됐습니다! test 를 위해 클론해서 생긴 폴더에 index.html 을 하나 만들어 주고 다음과 같이 입력을 해주겠습니다. vscode 에서는 ! 를 입력하면 html 기본 구조가 나와서 사용하기 편리합니다.

![](/assets/images/2024-03-02-jekyll-github-blog-1/05.png)
test blog라고 작성하여 커밋 푸시를 해보겠습니다.

```shell
 git add --all
 git commit -m "test commit"
 git push -u origin main
 ```

# 최종 확인하기

다시 github으로 돌아가서 actions탭에 들어가 보면 자동으로 빌드, 배포되고 있는 게 보이고 끝나면
`https://username.github.io/`링크로 접속해서 확인해볼 수 있습니다!

![](/assets/images/2024-03-02-jekyll-github-blog-1/06.png)

다음은 jekyll 셋팅으로 돌아오겠습니다.


참고
- <https://docs.github.com/en/pages/quickstart>
- <https://pages.github.com/>
