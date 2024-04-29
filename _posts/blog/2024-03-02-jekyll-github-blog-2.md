---
layout: post
title: "Github Blog 만들기 [2]"
summary: jekyll 셋팅하기
date: 2024-03-01 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

_mac Os 기준으로 작성되었습니다_

# jekyll?

>Jekyll is a static site generator. It takes text written in your favorite markup language and uses layouts to create a static website. You can tweak the site’s look and feel, URLs, the data displayed on the page, and more.

Jekyll은 정적 사이트 생성기입니다. 선호하는 마크업 언어로 작성된 텍스트를 사용하고 레이아웃을 사용하여 정적 웹 사이트를 만듭니다. 사이트의 모양과 느낌, URL, 페이지에 표시되는 데이터 등을 조정할 수 있습니다.

Github Pages 시작하기 설명에도 jekyll 테마를 선택해서 사용하는 방법을 추천하고 있습니다. jekyll을 사용해 블로그를 꾸며보겠습니다. jekyll은 ruby기반의 프레임워크로 ruby 설치가 꼭 필요합니다.

# 진행중 발생한 이슈

_처음에 기존에 설치된 ruby로 설치를 했었는데 버전 2.7 이상부터 된다는 에러 메시지가 나왔습니다. 그래서 ruby부터 다시 설치를 진행해주었습니다. ruby 3.0 이상, 5.0미만 버전으로 설치하시길 추천드립니다._

```bash
ERROR: Error installing jekyll:
The last version of rouge (>= 3.0, < 5.0) to support your Ruby & RubyGems was 3.30.0. Try installing it with `gem install rouge -v 3.30.0` and then running the current command again
rouge requires Ruby version >= 2.7. The current ruby version is 2.6.4.104.
```

_test용으로 만든 html이 폴더에 들어있어서 jekyll을 기본으로 다운로드 받을 때 생긴 오류. 폴더를 완전히 비우고 다시 실행하면 캡처본처럼 기본 테마가 설치 됩니다._

```bash
Conflict: /Users/leeyurim/Documents/yeol0324.github.io exists and is not empty.
Ensure /Users/leeyurim/Documents/yeol0324.github.io is empty or else try again with `--force` to proceed and overwrite any files.
```


# ruby 설치하기

필요한 루비 버전을 쉽게 관리하고 컨트롤할 수 있는 rbenv를 통해서 설치를 해주었습니다.<br>
**window 에서는 rbenv를 사용할 수 없고 [RubyInstaller](https://rubyinstaller.org/downloads/) 를 사용한다고 합니다.**
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
# install jekyll

터미널에서 깃 블로그 폴더로 이동을 하고 gem install을 실행합니다.

```bash
gem install bundler
gem install jekyll
gem install jekyll bundler
gem install github-pages
```

 클론 폴더에 파일이 있으면 에러가 발생하기 때문에 test 용 파일이 있다면 모두 지워준 후 진행하시면 됩니다.
터미널에서 다음을 입력해 줍니다

```bash
jekyll new ./
```
저는 블로그를 만들 폴더에서 진행하기떄문에 jekyll new ./ 로 진행해주었습니다. 폴더를 만들고 그 안에 작업하려면 new ./{폴더명} 으로 입력하면 됩니다.

# jekyll 서버 실행

여기까지 과정을 마치셨다면 거의 다 왔습니다. 서버를 띄우기, 테마 번들 설치만 남았습니다.


```bash
bundle install
bundle exec jekyll serve
```

서버를 띄우는데 성공하면 빌드 결과가 쭈욱 나오다가 jekyll 로컬 서버 주소를 알려줍니다.<br/>
<span class="h-yellow">Server address: http://127.0.0.1:4000/</span><br/>
http://127.0.0.1:4000/ 또는 http://localhost:4000/ 을 크롬에 (인터넷) 주소창에 입력하면 내 블로그가 실행이 됩니다!

![](/assets/images/2024-03-02-jekyll-github-blog-2/06.png)

>수정할 때마다 hot reload 를 사용하고 싶다면 <span class="h-yellow">--livereload</span>를 붙여 서버를 실행해 줍니다.
```
bundle exec jekyll serve --livereload
```

# 배포하기


프로젝트에 있는 \_posts 폴더 안에 있는 markdown이랑 똑같은 것을 볼 수가 있습니다.

```
 git add --all
 git commit -m "commit message"
 git push -u origin main
```
![](/assets/images/2024-03-02-jekyll-github-blog-2/10.png)

main 브랜치에 푸시 이벤트를 걸어 배포를 하도록 설정을 해두었으니([참고 : 블로그 만들기 1]({{base_path}}/blog/jekyll-github-blog-1/#자동-배포-설정)), 커밋 푸시를 완료하고 난 후 자신의 깃헙 블로그 `https://username.github.io/` 로 들어가보면 들어가면 적용된 것을 볼 수 있습니다!


참고 
- <https://jekyllrb.com/docs/posts/>
- <https://jekyllrb.com/docs/step-by-step/01-setup/>