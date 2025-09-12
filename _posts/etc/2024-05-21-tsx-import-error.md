---
layout: post
title: tsx import 오류 해결
summary: 
date: 2024-05-21 11:29:30 +09:00
categories: etc
tags: error typescript react
---

tsx 를 import 하려면 allowImportingTsExtensions 옵션이 허용되어야 한다는 뜻입니다.

```bash
An import path can only end with a '.tsx' extension when 'allowImportingTsExtensions' is enabled.
```

프로젝트의 tsconfig.json 파일에 allowImportingTsExtensions 옵션을 true 로 설정하여 허용해줍니다.

```json
compilerOptions : { 
    "allowImportingTsExtensions" : true
    // ...
}
```
