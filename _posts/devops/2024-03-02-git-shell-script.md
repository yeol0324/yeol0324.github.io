---
layout: post
title: "package.json 에서 script로 git 사용하기"
date: 2024-03-02 10:06:52 +0900
categories: devops
tags: s3 cors presignedUrl
---
deploy.sh
```shell
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
package.json
```json
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "local:dev": "env-cmd -e dev-local next dev",
    "local:build": "env-cmd -e build-local next build",
    "dev:dev": "env-cmd -e dev-development next dev",
    "dev:build": "env-cmd -e build-development next build",
    "dev:deploy": "sh deploy.sh dev",
    "qa:dev": "env-cmd -e dev-qa next dev",
    "qa:build": "env-cmd -e build-qa next build",
    "qa:deploy": "sh deploy.sh qa",
    "prod:dev": "env-cmd -e dev-production next dev -p 3300",
    "prod:build": "env-cmd -e build-production next build",
    "prod:deploy": "sh deploy.sh prod",
    "lint": "next lint"
  },
```