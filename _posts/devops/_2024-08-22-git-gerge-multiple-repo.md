---
layout: post
title: 여러 레포지토리 하나로 합치기(subtree)
summary: 여러 자잘한 프로젝트들을 하나로 합치기
date: 2024-08-22 13:52:18 +09:00
categories: devops
tags: git
---

여러 레포지토리 하나로 합치기(Merge multiple repository)

먼저 할일은 부모 레포지토리 하나 생성 ( 폴더가 될 레포지토리 ) 
> 레포 생성 후 클론, 터미널에서 해당 디렉토리로 이동하여 리모트에 추가해주어야함 ( 권한 )

```bash
git clone <레포>
cd 부모 폴더
git remote add <별명> <레포>
```

subtree 명령어를 사용함

```bash
git subtree add --prefix=<부모 repo에 저장할 폴더 명> <자식 repo> <branch>
git push
```

subtree 로 부모 폴더에 복사하고 push 해주면 기존 레포는 삭제해도 됨!