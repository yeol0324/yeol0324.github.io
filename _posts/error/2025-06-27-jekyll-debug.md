---
layout: error
title: "맥북에서 Jekyll 설치하며 만난 오류들, 이렇게 해결했다!"
date: 2025-06-27 14:30:24 +09:00
summary: "rbenv와 Ruby 맥북으로 고생하기..."
categories: javascript
tags: javascript Array deepdive 프론트엔드 V8 최적화
---


안녕하세요! 오늘은 맥북에서 Jekyll 블로그를 시작하려다 겪었던 난관들과 그 해결 과정을 상세히 공유해 보려 합니다. 사실 체념을 하고 맥북으로는 블로그 글을 쓰지 않고 있었습니다. 그래도 이제는 정말 해결해보고 싶었어요! 끝까지 파헤쳐보자는 마음으로 시작하게 됐습니다.

## 🤯 시작은 `Gem::FilePermissionError`

Jekyll은 Ruby 기반의 정적 사이트 생성 도구이죠! 지금 현재 제 블로그도 Jekyll로 작성이 되어있고 관련 글도 몇 개 작성했었는데요, Jekyll을 사용하려면 Ruby 환경 설정이 필수죠. 처음은 window에서 시작을 했고 맥북을 사게 돼서 맥북으로 옮겨왔습니다. 맥북에 rbenv로 설치를 하고 나서 💥 처음 `gem install bundler` 명령어를 입력하자마자 오류가 발생했습니다. 그 때 당시에도 해결해보려고 열심히 나름 노력은 했지만 외면하고 있다가 오늘 처음부터 시작을 해보았습니다.

오늘 제가 처음 받은 오류였습니다.

```
ERROR: While executing gem ... (Gem::FilePermissionError)
You don't have write permissions for the /Library/Ruby/Gems/2.6.0 directory.

```


> 📌 오류 원인 분석


permission 오류!! 이 오류는 정말 익숙합니다. 권한문제 !
이 오류는 맥북에 기본으로 설치된 **시스템 Ruby**의 특징 때문에 발생합니다. macOS는 시스템의 안정성과 보안을 위해 `/Library/Ruby/Gems` 같은 시스템 디렉토리에 일반 사용자가 임의로 파일을 쓰거나 변경할 수 없도록 권한을 제한한다고 합니다. 제가 `gem install`을 했을 때, rbenv가 아닌 이 시스템 Ruby 환경에서 설치를 시도해서 발생한 문제였습니다.

> 💡 해결 방법

가장 깔끔한 해결책은 **rbenv가 관리하는 Ruby 환경을 사용**하는 것입니다.

1.  **rbenv가 관리하는 Ruby 버전으로 전환:**
    ```bash
    rbenv global [원하는 Ruby 버전] # 예: rbenv global 3.2.3
    # 또는 특정 프로젝트 폴더에서만 사용하려면:
    # rbenv local [원하는 Ruby 버전]
    ```
    저는 이미 rbenv로 Ruby 3.1.4 (나중에는 3.2.3)를 설치해 두었기 때문에 해당 버전으로 전환했습니다.
2.  **`bundle install` 다시 시도:**
    `rbenv`를 통해 올바른 Ruby 환경으로 전환한 뒤 다시 설치를 시도했습니다.

---

## 💥 호환성 지옥

`bundler`와 `google-protobuf`, 그리고 `eventmachine`

권한 문제는 해결했지만, 새로운 버전 충돌 문제들이 줄줄이 나타났습니다. 여기부터가 정말 지옥이었습니다. 자바스크립트를 주 언어로 사용하는 저는 package.json 으로 몇번 맛보았었죠... 이제 나름 적응이 됐다고 생각했었는데, 여기는 정말 지옥이었어요. 😭

> 오류 1: `bundler`와 Ruby 버전 불일치

```

bundler requires Ruby version \>= 3.1.0. The current ruby version is 2.7.8.225.

```



>📌 오류 원인 분석

이는 설치하려는 **`bundler` 버전이 Ruby 3.1.0 이상을 요구**하는데, 당시 Ruby 버전이 **2.7.8**이었기 때문에 발생한 호환성 문제였습니다.



> 💡 해결 방법

1. `bundler` 구버전 설치 (임시방편)
    `bundler`는 하위 Ruby 버전을 지원하는 구 버전이 있습니다. 오류 메시지에서 안내해 준 대로 `gem install bundler -v 2.4.22`를 시도했습니다.
2. Ruby 버전 업그레이드 (권장)
    결과적으로 Jekyll 설치를 위해 Ruby 버전을 3.1.4 (이후 3.2.3)로 업그레이드하기로 했습니다. rbenv를 사용하면 매우 간단합니다.
    
    ```bash
    rbenv install 3.2.3 # 원하는 최신 안정 Ruby 3.x 버전
    rbenv global 3.2.3
    ```

> 오류 2: `google-protobuf`와 Ruby 버전 불일치

Ruby 버전을 3.1.4로 올린 후 다시 `bundle install`을 시도하자 이번에는 `google-protobuf`라는 Gem에서 문제가 발생했습니다.

```

google-protobuf requires Ruby version \>= 3.1, \< 3.5.dev. The current ruby version is 2.7.8.225.

```



> 📌 오류 원인 분석

이번에도 **Gem과 Ruby 버전 간의 호환성** 문제였습니다. `jekyll`의 의존성인 `google-protobuf`가 **Ruby 3.1 이상**을 요구하는데, 제가 작업하고 있는 환경이 2.7.8로 인식되면서 발생한 것이었습니다.



> 💡 해결 방법

이 문제는 Ruby 버전을 3.1.4 (또는 3.2.3)로 **확실히 전환한 후** 다시 `bundle install`을 시도함으로써 해결되었습니다. rbenv로 Ruby 버전을 전환하고 터미널을 다시 시작하거나 `source ~/.zshrc` 등으로 환경을 재설정하는 것이 중요했습니다.

> 오류 3: 고질적인 `eventmachine` 빌드 실패

가장 오랜 시간 저를 괴롭혔던 오류입니다. 몇 번을 다시 설치하고 삭제하고 권한 찾고 업데이트 해보고 아주 모든 짓을 다했습니다. `jekyll` 4.x 버전까지 올렸는데도 계속해서 `eventmachine-1.2.7`이라는 Gem에서 빌드 실패 오류가 발생했습니다.

```

ERROR: Failed to build gem native extension.
......
make: \*\*\* [binder.o] Error 1

````


> 📌 오류 원인 분석

`eventmachine-1.2.7`은 Ruby 2.x 시절에 주로 사용되던 오래된 Gem입니다. 이 Gem은 C++ 코드를 포함하고 있어 설치 시 사용자의 시스템에서 컴파일(빌드)되어야 하는데, Ruby 3.x 버전의 내부 API 변경 사항과 호환되지 않아 컴파일에 실패하는 것이었습니다. `binder.cpp` 파일 컴파일 오류는 이 호환성 문제로 인해 발생한 것입니다.

`xcode-select --install`로 Command Line Tools를 재설치하고, Homebrew로 OpenSSL 경로를 명시해 줘도 해결되지 않았던 이유도 여기에 있었습니다. 기본적인 빌드 도구는 갖춰졌지만, **Gem 자체의 소스 코드가 최신 Ruby 버전에 맞지 않았던 것**입니다.


## 💡 해결 방법

`eventmachine-1.2.7`을 Ruby 3.x에서 빌드하는 것은 거의 불가능 이라고 생각했어요. 따라서 이 Gem에 대한 의존성을 우회하는 방법을 선택했습니다. 이런 버전 문제는 내 문제가 아니라는 것을 일찍 알고, 그에 대응하는 방법을 찾는 것이 답입니다.

* **`eventmachine` 의존성 우회 (Jekyll Serve의 Live Reload 포기):**
    `eventmachine`은 주로 `jekyll serve` 명령의 실시간 브라우저 리로드(Live Reload) 기능을 위해 `em-websocket`을 통해 사용됩니다. 만약 이 라이브 리로드 기능이 필수가 아니라면, `em-websocket`의 설치 자체를 막아서 `eventmachine`의 문제를 우회할 수 있습니다.

    `Gemfile`을 열어 **`jekyll-feed` 그룹 내부에 다음 한 줄을 추가**했습니다.

    ```ruby
    # Gemfile
    source "[https://rubygems.org](https://rubygems.org)"

    # ... (생략) ...

    group :jekyll_plugins do
      gem "jekyll-feed", "~> 0.17"
      # em-websocket의 설치를 의도적으로 막는 라인
      gem 'em-websocket', '>= 99.0', require: false
    end

    # ... (생략) ...
    ```

    * `gem 'em-websocket', '>= 99.0'`: `em-websocket` 99.0 버전 이상을 찾으라고 지시하여, 실제로는 존재하지 않는 버전을 요구함으로써 Bundler가 이 Gem을 설치할 수 없게 만듭니다.
    * `require: false`: 만약 다른 Gem이 `em-websocket`을 필요로 하더라도 Ruby가 자동으로 로드하지 않도록 합니다.

    이후 `Gemfile.lock`과 Bundler 캐시를 정리한 뒤 다시 `bundle install`을 실행했습니다.

    ```bash
    rm Gemfile.lock
    bundle cache clean --all
    bundle install
    ```

---

## 🎉 드디어 `bundle install`

수많은 오류를 만난 끝에, `em-websocket`의 의존성을 우회하는 방법으로 마침내 `bundle install`을 성공했습니다!

이제 Jekyll 사이트를 로컬에서 실행할 수 있습니다. 프로젝트 디렉토리로 이동하여 다음 명령어를 입력해줍니다.

```bash
bundle exec jekyll serve
````


## 마무리 🥺🎊

Jekyll 설치는 간단해 보이지만, Ruby 버전 관리, Gem 의존성, 그리고 시스템 환경 설정이 얽히면서 생각보다 복잡한 오류에 직면할 수 있습니다. 저처럼 `eventmachine`과 같은 오래된 Gem이 최신 Ruby 환경에서 컴파일되지 않는 문제는 자주 발생하곤 합니다.

이 문제를 해결 하고 나서 다시 한번 마음으로 되뇌이는 문장들

1.  **오류 메시지는 항상 자세히 읽기**
 - 모든 해결 방법은 오류 메시지에 들어있다. 👀
2.  **`rbenv`와 같은 버전 관리 도구를 적극적으로 활용하기**
 - 저는 이제 nvm  없으면 node 사용 못해요!
3.  **`Gemfile`과 `Gemfile.lock`을 이해하고 적절히 수정하는 것.**
 - 처음부터 이쪽 파일을 봤다면 이렇게까지 오래 걸릴 일은 아니었는데...

 
이 글이 Jekyll 설치 과정에서 어려움을 겪는 다른 분들에게 작은 도움이 되기를 바랍니다. 

```