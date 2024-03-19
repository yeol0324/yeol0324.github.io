---
layout: post
title: "jekyll github blog 만들기"
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

ERROR: Error installing jekyll:
The last version of rouge (>= 3.0, < 5.0) to support your Ruby & RubyGems was 3.30.0. Try installing it with `gem install rouge -v 3.30.0` and then running the current command again
rouge requires Ruby version >= 2.7. The current ruby version is 2.6.4.104.

brew update
brew install rbenv ruby-build
rbenv versions
rbenv install -l
rbenv install 3.3.0
rbenv local 3.3.0
Ruby -v

마지막으로 rbenv PATH를 추가하기 위해 본인의 쉘 설정 파일 (..zshrc, .bashrc) 을 열어 다음의 코드를 추가합니다. 저는 zsh를 사용하니 .zshrc에 추가합니다.
vim ~/.zshrc
[[-d ~/.rbenv]] && \
 export PATH=${HOME}/.rbenv/bin:${PATH} && \
 eval "$(rbenv init -)"
코드를 추가하셨다면 source로 코드를 적용합니다.
source ~/.zshrc
그리고 다시 gem install을 수행해봅니다.
gem install bundler

gem install jekyll
gem install jekyll bundler
gem install github-pages
sass's executable "sass" conflicts with sass-embedded
Overwrite the executable? [yN] 저는 -y 를 해주었습니다.

깃 블로그 레파지토리를 클론한 폴더로 이동을 해줍니다.
클론 폴더에 파일이 있으면 에러가 발생합니다.

저는 기존에 테스트 한 파일이 있어서 삭제를 해줍니다
터미널에서 다음을 입력해 줍니다

jekyll new ./{폴더명}
저는 블로그를 만들 폴더로 진행하기떄문에 jekyll new ./ 로 진행해주었습니다.

파일을 정상적으로 비우고 진행을 하면 캡처본처럼 기본 테마가 설치 됩니다.

{{파일 설명}}

여기까지 과정을 마치셨다면
테마의 번들 설치 → 서버를 띄우기
과정이 남았습니다
bundle install
bundle exec jekyll serve
서버를 띄우는데 성공하면
서버 주소를 보여줍니다

해당 url 을 크롬에 (인터넷) 주소창에 입력하시면

이렇게 화면이 구성되어있는 것을 볼 수 있고 posts 글 하나를 볼 수가 있습니다.
프로젝트에 있는 \_posts 폴더 안에 있는 markdown이랑 똑같은 것을 볼 수가 있습니다.

git add .
git commit -m "메시지 입력"
git push

푸시를 완료하고 난 후 자신의 깃에 들어가보면

깃 블로그 사이트로 들어가면 적용된 것을 볼 수 있ㅅ습니다!

원하는 테마 깃을 찾아 클론을 해줍니다.
https://github.com/ejjoo/jekyll-theme-monos.git
https://sighingnow.github.io/jekyll-gitbook/

수정할 때마다 hot reload 를 사용하고 싶다면 다음을 입력해 줍니다
Pass the --livereload option to serve to automatically refresh the page with each change you make to the source files: bundle exec jekyll serve --livereload

정적인 html 로 이루어져있는 사이트와 같이 /폴더명/파일명 이 곧 주소가 됩니다.
파일은 기본적으로 markdown 을 사용하며 html 도 지원하고 있습니다.
예시
.
├── about.md # => http://example.com/about.html
├── documentation # folder containing pages
│ └── doc1.md # => http://example.com/documentation/doc1.html
├── design # folder containing pages
│ └── draft.md # => http://example.com/design/draft.html

Post 를 사용하려면 다음 파일명 규칙을 지켜야합니다.
YYYY-MM-DD-title.MARKUP
예시
2011-12-31-new-years-eve-is-awesome.md
2012-09-12-how-to-write-a-blog.md

## 모든 블로그 게시물 파일은 일반적으로 레이아웃 이나 기타 메타데이터를 설정하는 데 사용되는 머리말 로 시작해야 합니다 . 간단한 예에서는 비어 있을 수 있습니다.

layout: post
title: "Welcome to Jekyll!"

---

# Welcome

**Hello world**, this is my first Jekyll blog post.

I hope you like it!

———커스텀하기
bundle info --path minima 기본 테마 설치된 폴더를 찾아줍니다

cp -r minima-2.5.1/ /Users/leeyurim/Documents/Work/test/
빈 폴더로 복사를 해주었습니다.

참고 https://jekyllrb.com/docs/posts/
