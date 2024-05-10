---
layout: post
title: jekyll 블로그 코드 블럭 커스텀하기
summary: jekyll blog custom blocks
date: 2024-05-10 14:33:03 +09:00
categories: blog
tags: blog
---

블로그 글을 작성할 때 error 또는 warning 로그를 상자에 담아서 표현하고 싶었습니다. 오류 같은 느낌이 나도록 만들고 싶었는데 할 때마다 만들어 주기는 너무 귀찮잖아요?! 그리고 사용할 때마다 html 태그로 감싸고 클래스를 부여하는 것도 여간 귀찮은 일이 아닙니다. markup 문법에 기본으로 있는 ``` 이것을 ```  사용해서 코드 블럭을 만드는 것처럼 ```error 이렇게 사용하면 얼마나 편한가요!

# markdown code block 구조
마크다운으로 생성이 된 코드 블럭이 어떻게 생겼는지 알아야 style을 줄 수 있겠죠? html 개발자 도구를 사용해서 html 을 열어봤습니다.
```html
<code class="language-plaintext highlighter-rouge">이것을</code>


<pre class="highlight">
    <code>
        <span class="nx">console</span><span class="p">.</span><span class="nf">log</span><span class="p">(</span><span class="dl">'</span><span class="s1">hello</span><span class="dl">'</span><span class="p">)</span>
    </code>
</pre>

<pre>
    <code class="language-error">console.log('hello')</code>
</pre>
```

code 태그 안에 쓰거나 언어를 명시하지 않은 곳에는 code태그에만 담겨있고, markup에서 지원하는 언어는 pre 태그에 class가 자동으로 붙고 없는 언어는 안 붙어있는 것이 보입니다.
제가 지금 필요한 것은 딱 마지막 부분이죠! 바로 css를 추가하러 가봅시다

# style 추가 🌈
_base.scss 파일에 Code formatting 구역에 작성을 해주었습니다. 기본 테마를 최대한 건들지 않고 커스텀하려고 해요.
```scss
pre {
  padding: 8px 12px;
  overflow-x: auto;

  > code {
    border: 0;
    padding-right: 0;
    padding-left: 0;
  }
  &:not([class]) {
    border: 0;
    padding-right: 0;
    padding-left: 0;
    background: none;
    code {
      @include relative-font-size(0.9375);
      display: block;
      border: 1px solid $grey-color-light;
      border-radius: 3px;
      background-color: #eef;
      padding: 8px 12px;
      overflow-x: auto;
      &.language-error {
        color: #da1415;
        border-color: #da1415;
        background-color: #fbe8e8;
      }
      &.language-warning {
        color: #efc100;
        border-color: #efc100;
        background-color: #fcf9e7;
      }
      &.language-info {
          color: #2d61e5;
          border-color: #2d61e5;
          background-color: #ebf0fd;
      }
    }
  }
}
```
&:not([class]) 부분부터 추가를 해주었습니다. 제일 안쪽에는 language-${language} 로 원하는 것을 만들어 주시면 됩니다. 색은 [OpenBMC Web UI Style Guide](https://openbmc.github.io/webui-vue/guide/components/toasts/#additional-options)를 참고했습니다.

# ✨ 결과물 ✨
```error
console.log('error')
```
```warning
console.log('warning')
```
```info
console.log('info')
```