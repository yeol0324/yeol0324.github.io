---
layout: post
title: three.js에 텍스트 생성하기
summary: three.js textGeometry 사용해서 텍스트 생성하기
date: 2024-06-05 15:14:45 +09:00
categories: javascript
tags: threejs interactive javascript
---

three.js 네번째 작성 글입니다.

three.js에 텍스트 메쉬를 생성하여 글씨를 렌더링해볼까요? 미리 알아두셔야 할 점은 three.js에 기본으로 내장되어 있는 폰트는 한국어를 지원하지 않습니다.  🥲 ~~왜 안 해 줘 . . .~~ 그리고 three.js 공식 문서를 보다 보면 한국어로 선택했을 때 사라지는 문서가 많습니다. 오늘 사용할 [textGeometry](https://threejs.org/docs/#examples/en/geometries/TextGeometry) 문서도 사라집니다. 영어로 봐야 되는 것 참고해 주세요. 그래도 크롬 번역이 있어서 정말 다행이에요. ㉻㉻

# TextGeometry

> 텍스트를 단일 지오메트리로 생성하기 위한 클래스입니다. 텍스트 문자열과 로드된 폰트 및 지오메트리의 상위 ExtrudeGeometry에 대한 설정으로 구성된 매개변수 세트를 제공하여 구성됩니다.

사용자로부터 텍스트와 폰트, 그리고 3D 표현 방식을 정의하여 텍스트 지오메트리를 생성할 수 있습니다! 중요한 것은 폰트가 없으면 텍스트가 로드되지 않는 것입니다.

# 사용 전 준비

TextGeometry, FontLoader, FontData 그리고 사용 할 폰트를 import 해줍시다.

```javascript
import { TextGeometry } from "three/examples/jsm/geometries/TextGeometry";
import { FontLoader, FontData } from "three/examples/jsm/loaders/FontLoader";
import helvetiker_regular from "three/examples/fonts/helvetiker_regular.typeface.json";
```

폰트는 [여기]([textGeometry](https://threejs.org/docs/#examples/en/geometries/TextGeometry)) 서 골라도 되고 파일을 [typeface](https://gero3.github.io/facetype.js/)로 변환하여 사용해도 됩니다.

# Mesh 생성

기본적으로 scene, camera 등은 생성이 된 상태로 시작하겠습니다. TextGeometry도 기본 BoxGeometry처럼 사용하면 됩니다. 처음에 강조했던 폰트와 함께 TextGeometry 생성후, material 로 재질을 생성해준 후 three.mesh를 만들어줍니다. 

```javascript
const loader = new FontLoader();
const font = loader.parse(helvetiker_regular as unknown as FontData);

const textGeometry = new TextGeometry(string, {
    font: font,
    size: 5,
    ...
});
const material = new THREE.MeshStandardMaterial({ color: 0xffffff });
const textMesh = new THREE.Mesh(textGeometry, material);
```
TextGeometry의 첫 번째 인수로 생성하고 싶은 텍스트를, 두 번째로 parameters와 함께 생성해줍니다.

TextGeometry의 parameters를 하나씩 보자면,
```
  font: font,             - 로드할 폰트
  size: 3,                - 텍스트 크기
  height: 5,              - 텍스트 깊이
  curveSegments: 12,      - 곡선 세그먼트 수
  bevelEnabled: true,     - 가장자리 둥글게 설정
  bevelThickness: 1,      - 가장자리 두께
  bevelSize: 1,           - 가장자리 크기
  bevelOffset: 0,         - 가장자리 오프셋
  bevelSegments: 5        - 가장자리 세그먼트 수
```

마지막으로 textMesh를 씬에 추가해주면 끝!

```javascript
textMesh.position.set(0, 10, 0);
scene.add(textMesh);
```

- <https://threejs.org/docs/#examples/en/geometries/TextGeometry>