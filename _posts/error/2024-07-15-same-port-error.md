---
layout: post
title: 포트 사용 불가 문제
summary: 죽지도 않고 살아남는 인스턴스 ~0~
date: 2024-07-15 16:41:07 +09:00
categories: error
tags: error node
---

주말이 지나고 와서, 또는 오랜만에 켠 노트북에서 npm run start으로 어플리케이션을 실행했을 때 정말 자주 겪었던 이슈입니다. 또,  여러가지 프로젝트 담당자가 계속 자리에 찾아와서 동시에 켜고 있었을 때도... 자주 만났던 친구입니다.

nest.js로 서버 코드도 어떻게 돌아가는지 공부하고 싶어서 실행을 했는데 오랜만에 만난 에러 바로 해결 방법을 정리합니다. ✍️

```error

node:internal/errors:496
    ErrorCaptureStackTrace(err);
    ^

Error: listen EADDRINUSE: address already in use :::3000
    at __node_internal_captureLargerStackTrace (node:internal/errors:496:5)
    at __node_internal_uvExceptionWithHostPort (node:internal/errors:593:12)
    at Server.setupListenHandle [as _listen2] (node:net:1817:16)
    at listenInCluster (node:net:1865:12)
    at Server.listen (node:net:1953:7)
    at ExpressAdapter.listen (/Users/leeyurim/Documents/WebRTC/server/node_modules/@nestjs/platform-express/adapters/express-adapter.js:95:32)
    at /Users/leeyurim/Documents/WebRTC/server/node_modules/@nestjs/core/nest-application.js:180:30
    at new Promise (<anonymous>)
    at NestApplication.listen (/Users/leeyurim/Documents/WebRTC/server/node_modules/@nestjs/core/nest-application.js:170:16)
    at bootstrap (/Users/leeyurim/Documents/WebRTC/server/src/main.ts:6:3) {
  code: 'EADDRINUSE',
  errno: -48,
  syscall: 'listen',
  address: '::',
  port: 3000
}
```

이미 다른 애플리케이션이 동일한 포트를 사용하거나 이전에 실행된 애플리케이션 인스턴스가 종료되지 않고 여전히 사용 중인 경우 발생하는 오류입니다. 해당 오류에서는 3000번 포트를 사용하고 있네요. 실행 중인 포트에 바인딩할 수 없어요! 그래서 동일한 포트를 사용 중인 프로세스를 찾아서 kill 🔨 하면 됩니다.

## 사용 중인 프로세스 찾기
```shell
lsof -i :3000
```
lsof -i 명령어를 사용하고 찾을 포트를 입력해 줍니다. 그럼 다음과 같이 해당 포트를 사용하고 있는 프로세스를 찾을 수 있는데, 이 프로세스 아이디를 가지고 kill 명령어를 해주면 실행 중인 프로세스가 종료됩니다.

```shell
COMMAND   PID     USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
node    28751 leeyurim   24u  IPv6 0xdf0c81a53d2ad815      0t0  TCP *:hbci (LISTEN)
```

```shell
kill -9 28751
```
해당 명령어를 실행 후 lsof 명령어로 다시 찾아보면 깨끗하게 아무것도 나오지 않는 것을 확인해 볼 수 있습니다.

그럼 오늘도 오류 없는 하루 보내세요. ☀️
