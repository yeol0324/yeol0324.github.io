---
layout: post
title: "github blog 만들기 [3]"
summary: 블로그에 seo 적용하기
date: 2024-03-01 10:06:52 +0900
categories: blog
tags: jekyll blog github-page seo
sitemap:
    changefreq : daily
    priority : 0.8
published : true
---

Github blog가 이제는 형태를 갖추기 시작해서 미뤄놨던 seo를 드디어 적용하려고 합니다! 구글, 네이버, 다음 검색엔진에 각각 등록을 할겁니다.
# 검색엔진 등록 준비

## sitemap 생성
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

## 머릿말 설정
머릿말에 sitemap 관련한 설정을 등록해주어야합니다. 각 post 상단에 작성하는 머릿말에 적어주겠습니다.
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
기본 설정은 _config.yml defaults: 에서 설정할 수 있습니다.
```
defaults:
  - scope:
      path: ""
    values:
      toc: true
      sitemap: 
        changefreq: daily
        priority: 0.8
```
## robots.txt 생성

robots.txt는 웹사이트에 웹 크롤러같은 로봇들의 접근을 제어하기 위한 규약이다.
robots.txt 파일은 크롤러가 액세스할 수 있는 URL을 검색엔진 크롤러에 알려준다.

프로젝트 루트 디렉토리에 robots.txt 파일을 생성한다
robots.txt 파일에 아래 코드를 붙여넣는다. 이 때 Sitemap 의 주소는 자신의 블로그 URL로 수정하면 된다.

검색 로봇들이 블로그로 들어왔을 때 지도가 어디있는지 알려주는 용도입니다.

```txt
User-agent: *
Allow: /
Sitemap: https://yeol0324.github.io/sitemap.xml
```

## feed.xml 작성하기
rss 제출용 feed.xml 도 작성을 해줍니다. 동일하게 루트 디렉토리에 생성해줍니다.
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
        <description>{{ post.content | strip_html | truncatewords: 200 | xml_escape }}</description>
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


# 검색엔진 등록

sitemap.xml, robots.txt, feed.xml 작성이 끝났다면 커밋&푸시로 변경된 소스를 반영해줍니다. 이제 각 검색엔진에 등록을 해주겠습니다.


https://www.hahwul.com/2020/10/21/minimize-feeds-in-jekyll/#description-%EA%B8%B8%EC%9D%B4-%EC%9E%90%EB%A5%B4%EA%B8%B0-truncate--truncatewords
https://yenarue.github.io/tip/2020/04/30/Search-SEO/