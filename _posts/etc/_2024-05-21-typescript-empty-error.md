---
layout: post
title: --isolatedModules 오류 해결
summary: 
date: 2024-05-21 11:21:16 +09:00
categories: etc
tags: error typescript
---

ts(typescript) 파일을 빈파일로 추가하면 발생하는 에러입니다. 파일에 <span class="h-yellow">export {}<span> 을 써줍니다.

```bash
'index.tsx' cannot be compiled under '--isolatedModules' because it is considered a global script file. Add an import, export, or an empty 'export {}' statement to make it a module.
```