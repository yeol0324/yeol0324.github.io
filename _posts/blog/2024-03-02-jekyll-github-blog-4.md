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
```
 ---
 ---
 <?xml version="1.0" encoding="UTF-8"?>
 <urlset 
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
     xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd" 
     xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   {% for post in site.posts %}
     <url>
       <loc>{{ site.url }}{{ post.url }}</loc>
       {% if post.lastmod == null %}
         <lastmod>{{ post.date | date_to_xmlschema }}</lastmod>
       {% else %}
         <lastmod>{{ post.lastmod | date_to_xmlschema }}</lastmod>
       {% endif %}
    
       {% if post.sitemap.changefreq == null %}
         <changefreq>daily</changefreq>
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