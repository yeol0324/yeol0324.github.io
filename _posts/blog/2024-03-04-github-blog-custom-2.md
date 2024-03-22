---
layout: post
title: "jekyll github blog 커스텀하기 - 2"
summary: post에 toc 추가하기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

- Gemfile
  gem 'jekyll-toc' 추가하기
  터미널에 bundle install 입력해서 Gemfile 을 실행합니다.
- \_config.yml
  사이트의 섹션 에 jekyll-toc을 추가
  plugins:
  - jekyll-toc

## post 에 서 설정하거나

layout: post
title: "Welcome to Jekyll!"
toc: true

---

default로 설정해둘 수 있음

# the internal "default list".

defaults:

- scope:
  path: ""
  values:
  toc: true

\_layouts/post.html
{% raw %}{{ content | toc }}{% endraw %}

참고 https://github.com/toshimaru/jekyll-toc
