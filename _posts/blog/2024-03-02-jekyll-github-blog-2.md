---
layout: post
title: "github blog 만들기 [2]"
summary: jekyll 셋팅하기
date: 2024-03-01 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

_mac Os 기준으로 작성되었습니다_

이번에는 jekyll 을 사용해 블로그를 꾸며주겠습니다. jekyll 은 ruby기반의 프레임워크로, 어쩌고저쩌고. ruby 설치가 꼭 필요합니다.

_처음에 기존에 설치된 ruby로 설치를 했었는데 버전 2.7 이상부터 된다는 에러 메시지가 나왔습니다. 그래서 ruby부터 다시 설치를 진행해주었습니다. 여러분은 ruby 3.0 이상, 5.0미만 버전으로 설치하시길 추천드립니다._

```bash
ERROR: Error installing jekyll:
The last version of rouge (>= 3.0, < 5.0) to support your Ruby & RubyGems was 3.30.0. Try installing it with `gem install rouge -v 3.30.0` and then running the current command again
rouge requires Ruby version >= 2.7. The current ruby version is 2.6.4.104.
```

# ruby 설치하기

필요한 루비 버전을 쉽게 관리하고 컨트롤할 수 있는 rbenv를 통해서 설치를 해주었습니다.

```bash
brew update
brew install rbenv ruby-build
rbenv versions
rbenv install -l //설치 가능한 버전 확인
rbenv install 3.3.0 //3.3.0 버전 설치
rbenv local 3.3.0 //3.3.0 선택
ruby -v //루비 버전 확인
```

마지막으로 rbenv PATH를 추가하기 위해 본인의 쉘 설정 파일 (..zshrc, .bashrc) 을 열어 다음의 코드를 추가합니다.저는 zsh를 사용하니 .zshrc에 추가합니다.

```bash
vim ~/.zshrc
[[-d ~/.rbenv]] && \
 export PATH=${HOME}/.rbenv/bin:${PATH} && \
 eval "$(rbenv init -)"
```

코드를 추가한 후 !q로 빠져나와 source로 코드를 적용합니다.

```bash
source ~/.zshrc
```

그리고 gem install을 실행합니다.

```bash
gem install bundler

gem install jekyll
gem install jekyll bundler
gem install github-pages
```

깃 블로그 레파지토리를 클론한 폴더로 이동을 해줍니다. 클론 폴더에 파일이 있으면 에러가 발생하기 때문에 test 용 파일이 있다면 모두 지워준 후 진행하시면 됩니다.
터미널에서 다음을 입력해 줍니다
jekyll new ./{폴더명}
저는 블로그를 만들 폴더에서 진행하기떄문에 jekyll new ./ 로 진행해주었습니다.
[](/assets/images/2024-03-02-jekyll-github-blog-2/03.png)
파일을 정상적으로 비우고 진행을 하면 캡처본처럼 기본 테마가 설치 됩니다.

{{파일 설명}}

여기까지 과정을 마치셨다면
테마의 번들 설치 → 서버를 띄우기
과정이 남았습니다

```bash
bundle install
bundle exec jekyll serve
```

서버를 띄우는데 성공하면
서버 주소를 보여줍니다
[](/assets/images/2024-03-02-jekyll-github-blog-2/04.png)

[](/assets/images/2024-03-02-jekyll-github-blog-2/06.png)

해당 url 을 크롬에 (인터넷) 주소창에 입력하시면

이렇게 화면이 구성되어있는 것을 볼 수 있고 posts 글 하나를 볼 수가 있습니다.
프로젝트에 있는 \_posts 폴더 안에 있는 markdown이랑 똑같은 것을 볼 수가 있습니다.

git add .
git commit -m "메시지 입력"
git push

푸시를 완료하고 난 후 자신의 깃헙 블로그로 들어가보면 들어가면 적용된 것을 볼 수 있습니다!

[](/assets/images/2024-03-02-jekyll-github-blog-2/10.png)
[](/assets/images/2024-03-02-jekyll-github-blog-2/11.png)

원하는 테마 깃을 찾아 클론을 해줍니다.
https://github.com/ejjoo/jekyll-theme-monos.git
https://sighingnow.github.io/jekyll-gitbook/

수정할 때마다 hot reload 를 사용하고 싶다면 다음을 입력해 줍니다

```
bundle exec jekyll serve --livereload
```
다음글 : [태그 모음 추가하기](https://yeol0324.github.io/blog/jekyll-github-blog-3/)

참고 https://jekyllrb.com/docs/posts/
