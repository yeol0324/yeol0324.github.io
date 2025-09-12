---
layout: post
title: "Github Blog 만들기"
date: 2024-03-01 10:06:52 +0900
categories: development
tags: blog github-page
---

" 공부한 것들, 경험한 것들을 기록하기 "

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


# jekyll 셋팅하기
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
저는 블로그를 만들 폴더에서 진행하기때문에 jekyll new ./ 로 진행해주었습니다. 폴더를 만들고 그 안에 작업하려면 new ./{폴더명} 으로 입력하면 됩니다.

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


Github blog에 마지막 seo를 드디어 적용해봅시다!

# SEO?

SEO는 Search Engine Optimization 의 약자로 검색 엔진 최적화의 약자입니다. 구글, 네이버 등 검색엔진이 쉽게 검색할 수 있도록 하여 검색 결과에서 상위 노출이 되도록 하는 작업입니다. 아무리 좋은 글을 써도, 아무리 좋은 컨텐츠가 있어도 노출이 되지 않는다면 사용자가 접근을 할 수 있는 경로가 적어지겠죠. 저희의 블로그도 검색엔진에서 노출이 될 수 있도록 SEO 작업을 진행해보도록 하겠습니다.

# 검색엔진 등록 준비

검색엔진에 사이트 등록을 해야하는데 등록하기 전에 먼저 준비할 것들이 있습니다. 크롤링하는 로봇(크롤러)들이 사이트로 들어왔을 때 사이트의 정보, 즉 지도 역할을 하는 <code>sitemap</code>도 필요하고, 검색 엔진의 크롤러들에게 명령을 내리는 robots.txt 등 준비가 필요하니 하나씩 진행해보겠습니다.

## sitemap.xml

sitemap 에는 바로 앞에서 설명한 것처럼 사이트의 지도라고 볼 수 있습니다. 크롤러들이 컨텐츠를 빠짐없이 크롤링해가기 위해 새로운 컨텐츠가 추가될 때마다 사이트맵에 하나씩 등록을 해야합니다. 

[jekyll-sitemap](https://github.com/jekyll/jekyll-sitemap)을 사용하는 방법과, xml을 직접 생성하는 방법이 있습니다.

### jekyll-sitemap

먼저 Gemfile 과 _congif.yml 에 사용할 플러그인을 적어주고, 터미널에서 명령어를 입력해 프로젝트에 플러그인을 적용 시켜줍니다.

```bash
# Gemfile
gem 'jekyll-sitemap'

# _config.yml
plugins:
  - jekyll-sitemap

# 터미널
bundle
gem install jekyll-sitemap
```

_site 폴더 아래에 sitemap.xml 파일이 생성되면 완성입니다! 저는 처음에 실행했을 때에는 생성이 되지 않아서 git push를 해서 한번 빌드&배포 과정을 진행해주었더니 정상 작동이 되었습니다. 배포를 해주었으면, {블로그주소}/sitemap.xml 로 이동해서 sitemap 생성과 적용이 잘 되었는지 확인해줍니다.

### 직접 작성
{%raw%}
```
---
layout: null
sitemap:
  exclude: 'yes'
---
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  {% for post in site.posts %}
  {% unless post.published == false %}
    <url>
      <loc>{{ site.url }}{{ post.url }}</loc>
      {% if post.lastmod == null %}
        <lastmod>{{ post.date | date_to_xmlschema }}</lastmod>
      {% else %}
        <lastmod>{{ post.lastmod | date_to_xmlschema }}</lastmod>
      {% endif %}

      {% if post.sitemap.changefreq == null %}
        <changefreq>weekly</changefreq>
      {% else %}
        <changefreq>{{ post.sitemap.changefreq }}</changefreq>
      {% endif %}

      {% if post.sitemap.priority == null %}
          <priority>0.5</priority>
      {% else %}
        <priority>{{ post.sitemap.priority }}</priority>
      {% endif %}
    </url>
    {% endunless %}
  {% endfor %}
</urlset>
```
{%endraw%}

동일하게 {블로그주소}/sitemap.xml 로 이동해서 sitemap 생성과 적용이 잘 되었는지 확인해줍니다.

## 머릿말 설정

머릿말에 sitemap 설정을 등록해주어야합니다. 각 post 상단에 작성하는 머릿말에 적어주겠습니다.
```
---
layout: post
title: "github blog 만들기 [3]"
...
sitemap:
    changefreq : daily
    priority : 0.8
---
```

post 마다 작성해주는 방법도 있지만, 포스트를 쓸 때마다 작성을 하기가 정말 귀찮죠... 저는 default 로 설정을 해주었습니다. 
기본 설정은 _config.yml <span class="h-yellow">defaults:</span> 에서 설정할 수 있습니다.

```bash
defaults:
  - scope:
      path: ""
    values:
      toc: true
      # --- 추가 ---
      sitemap: 
        changefreq: daily
        priority: 0.8
```
여기서 설정한 sitemap 설정을 살펴보겠습니다.
- <code>changefreq</code> : 스크랩 주기 always, hourly, daily 등이 있습니다.
- <code>priority</code> : 스크랩 우선순위 0.0 에서 1.0 사이의 값을 부여합니다.

## robots.txt 생성

robots.txt는 웹사이트에 웹 크롤러같은 로봇들의 접근을 제어하기 위한 규약입니다. 크롤러가 액세스할 수 있는 URL을 검색엔진 크롤러에 알려주거나 허용을 해주는 용도입니다.

프로젝트 루트 디렉토리에 robots.txt 파일을 생성하고 아래 코드를 입력합니다. 이 때 Sitemap 의 주소는 자신의 블로그 URL로 수정하면 됩니다.

```text
User-agent: *
Allow: /
Sitemap: https://yeol0324.github.io/sitemap.xml
```
- <code>User-agent</code> : 크롤링 규칙이 적용될 크롤러 지정
- <code>Allow</code> : / 부터 상대 경로로 크롤링을 허용할 경로
- <code>Disallow</code> : / 부터 상대 경로로 크롤링을 제한할 경로
- <code>Sitemap</code> : 사이트맵이 위치한 경로의 전체 url

특정 크롤러만 허용을 해줄 경우, User-agent : Googlebot 형식으로 입력을 할 수 있습니다.
> 구글: Googlebot, 네이버: Yeti, 다음: Daum, 빙: Bingbot 등...

## feed.xml

RSS는 검색 가능성을 높이기 위해
Daum, Naver 검색엔진에 등록할 때도 사용할 rss 제출용 feed.xml 도 작성을 해두겠습니다. sitemap과 동일하게 [jekyll-feed](https://github.com/jekyll/jekyll-feed)을 사용하는 방법과, xml을 직접 생성하는 방법이 있습니다. 동일하게 루트 디렉토리에 생성해줍니다.

### jekyll-feed

```bash
# Gemfile
gem 'jekyll-feed'

# _config.yml
plugins:
  - jekyll-feed

# 터미널
bundle
gem install jekyll-feed
```
_site 디렉토리 안에 feed.xml 이 생성되는 것을 확인할 수 있습니다.

### 직접 작성

{%raw%}
```
---
layout: null
---
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{{ site.title | xml_escape }}</title>
    <description>{{ site.description | xml_escape }}</description>
    <link>{{ site.url }}{{ site.baseurl }}/</link>
    <atom:link href="{{ "/feed.xml" | prepend: site.baseurl | prepend: site.url }}" rel="self" type="application/rss+xml"/>
    <pubDate>{{ site.time | date_to_rfc822 }}</pubDate>
    <lastBuildDate>{{ site.time | date_to_rfc822 }}</lastBuildDate>
    {% for post in site.posts limit:30 %}
      <item>
      <title>{{ post.title | xml_escape }}</title>
        <description>{{ post.content | strip_html |  xml_escape }}</description>
        <pubDate>{{ post.date | date_to_rfc822 }}</pubDate>
        <link>{{ post.url | prepend: site.baseurl | prepend: site.url }}</link>
        <guid isPermaLink="true">{{ post.url | prepend: site.baseurl | prepend: site.url }}</guid>
        {% for tag in post.tags %}
        <category>{{ tag | xml_escape }}</category>
        {% endfor %}
        {% for cat in post.categories %}
        <category>{{ cat | xml_escape }}</category>
        {% endfor %}
      </item>
    {% endfor %}
  </channel>
</rss>
```
{%endraw%}

동일하게 {블로그주소}/feed.xml 로 이동해서 feed 생성과 적용이 잘 되었는지 확인해줍니다.

# 검색엔진 등록

sitemap.xml, robots.txt, feed.xml 작성이 끝났다면 커밋&푸시로 변경된 소스를 반영해줍니다. 이제 각 검색엔진에 ( 저는 Google, Naver ) 에 등록을 하겠습니다.

## GOOGLE
Google Search Console에서 진행을 합니다. [google_search_console](https://search.google.com/search-console/welcome) <br/><br/>
![google_search_console](/assets/images/jekyll0github-blog-301.png)<br/><br/>
처음 접속한다면 위의 화면처럼 나오는데요, 먼저 블로그 url을 입력하고 본인 소유의 site 가 맞는지 인증 절차를 한번 거치게 됩니다.

### sitemap 등록
sitemap 의 위치를 등록해주겠습니다. 왼쪽에 있는 메뉴 바 > Sitemaps 로 들어와서 sitemap 이 있는 주소를 입력해 줍니다. 최상단에 배치해두었으니 {블로그주소}/ 뒤에 sitemap.xml 만 입력해주면 되겠죠? sitemap.xml 리스트가 나오고 성공으로 나왔습니다!
> sitemap url 오류가 나오는 경우, _config.yml 에서 url 설정을 헀는지 꼭 확인해보기

### 색인 생성
페이지 색인 생성을 해주겠습니다. 왼쪽에 있는 메뉴 바 > URL 검사를 클릭, 상단 검색창에 자신의 블로그 URL 을 입력합니다. 검사를 마친후, "URL이 Google에 등록되어 있지 않음" 으로 뜬다면 색인 생성 요청을 해줍니다. 1~2일 정도 소요되는데요 색인 생성이 완료되면 "URL이 Google에 등록되어 있음" 으로 메시지가 바뀝니다.

## Naver
Naver Search Advisor 에서 진행을 합니다. [naver_search_advisor](https://searchadvisor.naver.com/)
사용이 처음이라면 웹마스터도구 사용하기로 동의를 먼저 해준 후, 웹마스터 도구 > 사이트 관리 > 사이트 등록 으로 이동합니다.
사이트 등록에 블로그 URL 을 등록을 해주고 동일하게 본인 소유가 맞는지 인증을 진행합니다.

### Sitemap/RSS 등록
사이트 등록 페이지에 등록된 블로그 URL 을 클릭해 관리 페이지에서 진행합니다.

왼쪽에 있는 요청 > 사이트맵 제출에서 google과 동일하게 {블로그주소}/sitemap.xml 을 입력해줍니다.
왼쪽에 있는 요청 > RSS 제출에서 {블로그주소}/feed.xml 을 입력해줍니다.
> 제출할 때 오류가 나오는 경우, _config.yml 에서 url 설정을 헀는지 꼭 확인해보기

### robots 수집 요청
미리 작성을 해두었던 robots.txt도 확인을 해보겠습니다.

왼쪽에 있는 검증 > robots.txt로 들어가서 수집 요청을 하고, {블로그주소}/robots.txt를 입력해 검증을 해보겠습니다.

# 마무리

고생하셨습니다. 검색엔진에 등록을 마쳤습니다. 👏

각각 등록이 잘 되었는지 확인 한번씩 해보겠습니다.
![네이버검색엔진검사결과](/assets/images/jekyll0github-blog-302.png)

짠 ✨

네이버는 간단 체크 기능으로 등록이 제대로 됐는지 확인해볼 수 있습니다.

google에서도 url 검사로 블로그 주소를 입력해서 확인을 하고, 이제 기다리는 시간만 남았습니다. 


로봇들아 열일해줘 🤖

참고
- <https://docs.github.com/en/pages/quickstart>
- <https://pages.github.com/>
- <https://jekyllrb.com/docs/posts/>
- <https://jekyllrb.com/docs/step-by-step/01-setup/>
- <https://www.hahwul.com/2020/10/21/minimize-feeds-in-jekyll/#description-%EA%B8%B8%EC%9D%B4-%EC%9E%90%EB%A5%B4%EA%B8%B0-truncate--truncatewords>