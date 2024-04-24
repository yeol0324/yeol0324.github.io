---
layout: post
title: "jekyll github blog 커스텀하기 [3]"
summary: 카테고리 이전글 다음글 버튼 추가하기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: jekyll blog github-page
---

오늘은 포스트 하단에 nav 버튼을 추가해보겠습니다.

![](/assets/images/2024-03-04-github-blog-custom-3/01.png)

블로그에 이전/다음 글이 이어지는 경우가 많아서 포스트 하단마다 직접 버튼을 추가해 주고 있었습니다. 포스트마다 직접 추가하려고 하니 귀찮기도 하고 까먹을 때도 많아서 자동으로 포스트에 추가되도록 해보겠습니다!

먼저 _includes 폴더 안에 pagination.html 을 만들어 주고 다음과 같이 작성을 해줍니다.

[jekyll 문법 사용하기](https://yeol0324.github.io/blog/jekyll-use/) 참고!

```html
{% raw %}
{% assign cat = page.categories[0] %}
{% assign cat_list = site.categories[cat] %}
{% for post in cat_list %}
  {% if post.url == page.url %}
  	{% assign prevIndex = forloop.index0 | minus: 1 %}
  	{% assign nextIndex = forloop.index0 | plus: 1 %}
  	{% if forloop.first == false %}
  	  {% assign next_post = cat_list[prevIndex] %}
  	{% endif %}
  	{% if forloop.last == false %}
  	  {% assign prev_post = cat_list[nextIndex] %}
  	{% endif %}
  	{% break %}
  {% endif %}
{% endfor %}

{% if prev_post or next_post %}
  <nav class="pagination">
    {% if prev_post %}
    <a href="{{ prev_post.url }}" class="pagination-prev button">
      <div class="icon">&#10140;</div>
      <div class="wrap">
        <span>이전글</span>
        <div>{{ prev_post.title }}</div>
      </div>
    </a>
    {% endif %}
    {% if next_post %}
    <a href="{{ next_post.url }}" class="pagination-next button">
      <div class="wrap">
        <span>다음글</span>
        <div>{{ next_post.title }}</div> 
      </div>
      <div class="icon">&#10140;</div>
    </a>
    {% endif %}
  </nav>
{% endif %}
{% endraw %}
```
카테고리 내에서 이동을 하고 싶어서 이렇게 작성을 해보았습니다. <code>page.next.url</code> <code>page.previous.url</code> 을 사용할 수 있습니다.

전체에서 이동을 하고 싶다면 
저장이 되었다면 _layouts/post.html 파일에 들어가서 방금 만들어 준 html 을 넣어주겠습니다.
컴포넌트 방식과 동일하죠?

{% raw %}
```
{%- include pagination.html -%}
```
{% endraw %}

_layout.scss 에 디자인을 적용해 주었습니다.

``` scss
.pagination {
  @include flexbox(between, center);
  .button {
    width: 300px;
    background: #f8f9fa;
    color: $text-color;
    padding: 10px 0;
    cursor: pointer;
    span {
      font-size: 12px;
    }
    .icon {
      width: 30px;
      height: 30px;
      margin: 10px;
      color: $point-color;
      border: 1px solid $point-color;
      border-radius: 100px;
      transition: 0.4s;
      @include flexbox(center, center);
    }
    .wrap {
      * {
        max-width: 220px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }
    }
    &:hover {
      text-decoration: none !important;
      color: #808080;
    }
    &.pagination-prev {
      @include flexbox(start, center);
      .icon {
        transform: rotate(180deg);
      }
      .wrap {
        @include column-flexbox(center, start);
      }
    }
    &.pagination-next {
      @include flexbox(end, center);
      .wrap {
        @include column-flexbox(center, end);
      }
    }
    &:hover {
      &.pagination-prev {
        .icon {
          transform: rotate(180deg) translateX(4px);
        }
      }
      &.pagination-next {
        .icon {
          transform: translateX(4px);
        }
      }
    }
  }
}

```
위에서 사용한 include가 뭔지 궁금하다면? [scss 사용하기](https://yeol0324.github.io/blog/scss-use/)

[참고 문서](https://talk.jekyllrb.com/t/how-to-link-to-next-and-previous-posts-for-same-blog-category/629)