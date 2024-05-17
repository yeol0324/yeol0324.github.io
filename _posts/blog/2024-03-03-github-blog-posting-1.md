---
layout: post
title: 깃헙 블로그 포스팅 하기
summary: github blog posting 하기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: blog github-page markdown
---

깃헙 블로그를 운영하면서 가장 중요한 블로그 포스팅하는 방법을 정리해보겠습니다. 규칙을 지키지 않으면 열심히 작성한 글이 블로그에서 보이지 않는 엄청난﹒﹒﹒ 문제가 발생합니다.
~~저도 알고 싶지 않았어요. 🥹~~

간단한 규칙들이니 한번씩 꼭 확인해봅시다!

# 폴더 생성하기
처음 프로젝트를 생성할 때 자동으로 생성이 되었겠지만 한번 더 확인하겠습니다. 프로젝트 최상단에서 <span class="h-yellow">_posts</span> 디렉토리 안에 글을 작성해줘야합니다. 포스트 임시 저장할 곳이 필요하다면<span class="h-yellow">_draft</span> 디렉토리를 생성해서 보관을 할 수 있습니다.

# 파일명 규칙
가장 중요한 파일명 규칙입니다. 파일명은 <span class="h-yellow">yyyy-mm-dd-title</span> 로 작성을 해줘야합니다.
예시 : 2024-01-01-first-post.md

# 머릿말 작성하기
문서의 최상단에는 머릿말(Front Matter)이 들어갑니다. 제목, 날짜, 카테고리 등 다양한 정보를 YAML 형식으로 작성을 합니다. 머리말을 사용하여 페이지에 대한 변수를 설정할 수 있습니다.
```
---
layout: post
title: 깃헙 블로그 포스팅 하기
summary: github blog posting 하기
date: 2024-03-02 10:06:52 +0900
categories: blog
tags: blog github-page markdown
food: Pizza
---
```
지금 보시는 포스팅의 머릿말입니다.
- layout : 사용할 레이아웃 _layouts 디렉토리 안에 꼭 포함돼있어야함.
- title : 문서 제목
- date : 날짜 YYYY-MM-DD HH:MM:SS +/-TTTT 형식으로 작성
- categories: 포스터의 카테고리
- published : true/false 사용하여 글 비공개 설정
- <span class="h-yellow">food 와 같은 변수를 설정해서 사용할 수도 있습니다.</span>

머릿말 사용 예시
{% raw %}
```html
<!-- post.html -->
  <header class="post-header">
    {{page.categories}}
    <h1 class="post-title p-name" itemprop="name headline">
      {{ page.title | escape }}
    </h1>
    <h3 class="post-summary p-name" itemprop="name headline">
      {{ page.summary | escape }}
    </h3>
    <p class="post-meta">
      <time
        class="dt-published"
        datetime="{{ page.date | date_to_xmlschema }}"
        itemprop="datePublished"
      >
        {%- assign date_format = site.minima.date_format | default: "%b %-d, %Y"
        -%} 
        {{ page.date | date: date_format }}
      </time>
      {%- if page.author -%} •
      <span itemprop="author" itemscope itemtype="http://schema.org/Person"
        ><span class="p-author h-card" itemprop="name"
          >{{ page.author }}</span
        ></span
      >
      {%- endif -%}
    </p>
  </header>
```
{% endraw %}

# content 작성
머릿말 부분 아래부터는 포스트의 컨텐츠 영역입니다! 사용 중인 jekyll은 <span class="h-yellow">HTML</span>과 <span class="h-yellow">Markdown</span>을 지원하는데 각각 규칙에 맞게 작성을 해줍니다. HTML 은 태그를 항상 닫아야하고 Markdown 보다 지킬 것들이 많아 여간 귀찮은 일이 아닙니다. 저는 Markdown 으로 작성하는 것을 추천드립니다.
<!-- > <a href="{{base_path}}/etc/markdown-use/">Markdown 알아보기</a> -->

작성을 다 했거나 하는 도중 확인을 하고 싶다면 로컬에서 먼저 확인을 해줍니다.
```bash
bundle exec jekyll serve
# 또는 터미널에서 입력
bundle exec jekyll serve --livereload # 새로고침 없이 livereload
```

# 업로드 하기
마지막으로 포스트를 업로드하면 됩니다. 컨트롤 + s 로 저장만 한다고 바로 서버에 올라가는 게 아니죠! 깃헙 페이지 설정에서 main 브랜치에 푸시가 되면 자동으로 페이지 배포가 되도록 설정을 했었는데요, 포스트 글을 다 썻다면 git push 만 해주면 끝입니다.
[자동 배포 설정]({{base_path}}/blog/jekyll-github-blog-1#자동-배포-설정)

---
참고
- <https://jekyllrb-ko.github.io/docs/front-matter/>
- <https://jekyllrb.com/tutorials/convert-site-to-jekyll/#7-show-posts-on-a-page>