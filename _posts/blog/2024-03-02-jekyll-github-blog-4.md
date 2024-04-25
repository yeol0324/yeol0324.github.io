---
layout: post
title: "github blog 만들기 [4]"
summary: 블로그에 seo 적용하기
date: 2024-03-01 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
published : false
---

Github blog가 이제는 형태를 갖추기 시작해서 미뤄놨던 seo를 드디어 적용하려고 합니다! 구글, 네이버, 다음 검색엔진에 각각 등록을 할겁니다.
Gemfile
gem 'jekyll-sitemap'
_config.yml
plugins:
  - jekyll-sitemap
터미널
bundle
gem install jekyll-sitemap

_site 폴더 아래에 sitemap.xml 파일이 생성
git push 를 해서 배포를 한 후 {블로그주소}/sitemap.xml 을 들어가보니 생성되어 있었다!

