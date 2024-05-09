---
layout: post
title: "git 자동 push 기능 만들기"
summary: 
date: 2024-05-09 17:09:21 +09:00
categories: devops
tags: shell git
---

# 왜 이런걸 만들었지?
다양한 브랜치를 사용하고 있었는데, 배포 관련 이슈때문에 개발이 완료될 때마다 머지를 하고 빌드를 해서 푸시를 해야되는 일이 생겼습니다. 2개로 나눠서 진행하고 있어서 2가지를 다 운용하고 있다보니 깃 그래프가 과장 조금 보태서 10줄이 넘어간 것 같았습니다. 수동으로 하면 시간도 오래걸릴뿐더러 조금만 집중을 하지 않아도 바로 실수를 할 것 같은 불안감이 있었습니다.

배포 관련 이슈를 먼저 해결을 했어야했는데 깊이 알야봐야할 것 같아서 당장 눈앞의 불편함을 먼저 해결하기위해 만들었습니다.

# shell script 에서 git 사용
쉘 스크립트는 unix 커맨드를 사용할 수 있기때문에 터미널로 많은 작업을 반복해서 작업해야할 때 많이 사용했습니다. 때문에 당연히 git 명령어도 쓸 수 있어요! 이 방법을 고안해서 자동으로 저 귀찮은 작업을 스크립트로 만들었습니다.

```shell
# deploy.sh
git pull $1
git branch -D $1
git push origin -d $1
npm run $1:build
git fetch origin
git checkout -b $1
git push origin $1
git add -A
git commit -m "build files"
git push origin $1
```
스크립트를 실행할 때 스크립트 명 뒤에 붙이는 순서대로 shell script 에서 변수로 읽어옵니다. 총 2가지 브랜치에 해줬어야해서 실행할 때 변수를 통해서 진행하도록 만들었습니다.

# 실행하기

반복작업하기 싫고 귀찮은 게 싫어서 열심히 만든 스크립트를 또 실행할 때마다 경로 들어가서 파일명을 실행하기 귀찬잖아요! 저는 next.js 를 사용한 프로젝트에서 사용을 하고 있었습니다. package.json 에서 엄청난 명령어를 만들 수 있죠. package.json 의 scripts 에 작성을 했습니다.

package.json
```json
  "scripts": {
    "dev:dev": "env-cmd -e dev-development next dev",
    "dev:build": "env-cmd -e build-development next build",
    "dev:deploy": "sh deploy.sh dev",
    "prod:dev": "env-cmd -e dev-production next dev -p 3300",
    "prod:build": "env-cmd -e build-production next build",
    "prod:deploy": "sh deploy.sh prod",
    "lint": "next lint"
  },
```

터미널에서 npm run prod:deploy 를 실행해주면 깃 접속 빌드 혼자 열심히 돌아가는 스크립트 완성!✨

![shell script](/assets/images/20240509/shellscript.png)

배포 이슈도 해결해야는데 😅 해결할 게 한두개가 아니어서 행복한 일상을 보내는 중입니다 하하.