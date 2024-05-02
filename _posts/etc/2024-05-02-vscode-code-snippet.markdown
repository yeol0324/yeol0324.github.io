---
layout: post
title: "vscode 자동완성 만들기"
summary: vscode code snipet
date: 2024-03-02 10:06:52 +0900
categories: etc
tags: vscode
---

snippet은 효율성을 중시하는( ~~귀찮고 반복적인 것을 싫어하는~~ ) 사람에게 없어서는 안될 기능입니다. 같은 포맷을 항상 입력해야되거나, 반복되는 작업을 하다보면 더 하기 싫어지는 경우가 많죠... vscode 에서 snippet 을 알아보고 필요한 snippet을 생성해보려고 합니다.

# Snippet?

> 스니펫(snippet)은 재사용 가능한 소스 코드, 기계어, 텍스트의 작은 부분을 일컫는 프로그래밍 용어이다. 사용자가 루틴 편집 조작 중 반복 타이핑을 회피할 수 있게 도와준다. [위키백과](https://ko.wikipedia.org/wiki/%EC%8A%A4%EB%8B%88%ED%8E%AB)
> 반복해서 자주 사용하는 코드를 저장해두고 반복 작업을 없애줄 수 있는 정말 없으면 안 되는 기능입니다!

vscode에서는 일부 지원하는 것들이 있는데, 예를들면 html 파일에서 ! 하나를 입력했을 때 나오는 html 템플릿 등이 있습니다.
![vscode_snippet](/assets/images/20240502/01.png)

꼭 필요한 코드들은 이미 vscode에 잘 되어있어서 필요성을 못느꼈었는데 jekyll로 블로그를 쓰다보니 상단에 머릿말을 쓰는게 은근이 귀찮더라고요!? 저만 그랬나요 😅 그래서 vscode에서 snippet을 추가하는 방법을 같이 알아보려고 합니다.

# vscode snippet 사용

먼저 설정을 햊ㄴㅇ
Code > preferences > Congifure User Snippets 클릭 또는 cmd + shift + p 단축키를 사용하여 Configure User Snippets 을 검색 해줍니다.
그리고 사용할 언어를 선택해주면 되는데, 저는 블로그 머릿말 템플릿을 만들 거기 때문에 markdown을 선택했습니다. 언어를 선택하면 언어.json 파일이 새창으로 뜨는데 여기에서 사용하고 싶은 snippet을 등록해주면 끝 ❗️ 아주 간단하죠.

# snippet 생성

예시를 한번 살펴보겠습니다.

```json
// Example:
"Print to console": {  // snippets 이름
	"prefix": "front", // 해당 snippet의 단어 트리거, 이 문자와 일치하면 수행됩니다.
	"body": [ // 불러오고 싶은 형식을 작성해줍니다.
		"---",
		"layout: post",
		"title: $1",
		"summary: $2",
		"date: $CURRENT_YEAR-$CURRENT_MONTH$CURRENT_DATE $CURRENT_TIMEZONE_OFFSET",
		"categories: $TM_DIRECTORY",
		"tags: $3",
		"---",
	],
	"description": "Log output to console" // 코드 조각에 대한 설명
}
```

"body": 불러오고 싶은 형태로 내용을 채워넣는다. vscode snippet에 적용되는 변수, 문법도 있습니다.
파일
TM_FILENAME현재 문서의 파일 이름
TM_FILENAME_BASE확장자가 없는 현재 문서의 파일 이름
TM_DIRECTORY현재 문서의 디렉토리

날짜
CURRENT_YEAR 현재 연도
CURRENT_MONTH 두 자리 숫자의 월(예: '02')
CURRENT_DATE 두 자리 숫자로 된 날짜(예: '08')
CURRENT_TIMEZONE_OFFSET 현재 UTC 시간대 오프셋은 +HH:MM또는 입니다 -HH:MM(예 -07:00: ).

변환
"${TM*FILENAME/[\\.]/*/g}" ${TM*FILENAME}의 .을 * 로 변경

탭 이동
$1, $2, $2...
$number 형식으로 써두어서 snippet이 나왔을 때 tab으로 이동할 수 있도록 순서를 만들어 줄 수도 있습니다.

[자세히 보러가기](https://code.visualstudio.com/docs/editor/userdefinedsnippets#_using-textmate-snippets)

![my_snippet](/assets/images/20240502/02.png)

---

참고

- <https://code.visualstudio.com/docs/editor/userdefinedsnippets#_create-your-own-snippets>
