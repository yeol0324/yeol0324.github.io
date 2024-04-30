---
layout: post
title: "github blog 만들기 [3]"
summary: 블로그에 검색엔진에 등록하기
date: 2024-03-01 10:06:52 +0900
categories: blog
tags: jekyll blog github-page seo
sitemap:
    changefreq : daily
    priority : 0.8
published : true
---

Github blog가 이제는 형태를 갖추기 시작해서 미뤄놨던 seo를 드디어 적용하려고 합니다!

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
<urlset xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
        xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
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

```txt
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
layout: none
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
        <description>{{ post.content | strip_html | xml_escape }}</description>
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

sitemap.xml, robots.txt, feed.xml 작성이 끝났다면 커밋&푸시로 변경된 소스를 반영해줍니다. 이제 각 검색엔진에 등록을 해주겠습니다.

## GOOGLE
웹마스터도구
<https://search.google.com/search-console/welcome> 접속
![google_search_console](/assets/images/jekyll0github-blog-301.png)

블로그 url을 입력하고 본인 소유의 site 가 맞는지 인증 절차를 한번 거치게 됩니다. 인증 절차를 마친 후 먼저 sitemap 의 위치를 등록해주겠습니다. 왼쪽에 있는 메뉴 바 > Sitemaps 로 들어와서 sitemap 이 있는 주소를 입력해 줍니다. 최상단에 배치해두었으니 {블로그주소}/ 뒤에 sitemap.xml 만 입력해주면 되겠죠?



https://www.sitemaps.org/ko/protocol.html
https://www.hahwul.com/2020/10/21/minimize-feeds-in-jekyll/#description-%EA%B8%B8%EC%9D%B4-%EC%9E%90%EB%A5%B4%EA%B8%B0-truncate--truncatewords