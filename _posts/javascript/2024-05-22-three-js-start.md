---
layout: post
title: Three.js 시작하기
description: react에서 Three.js를 사용해서 object를 만들어보자! 
date: 2024-05-22 10:58:31 +09:00
categories: javascript
tags: threejs interactive javascript
---

회사에서도 AR 구현 테스트를 할 때 Three.js를 사용해봤습니다. 이곳저곳에서 많은 관심을 보였고, 이를 통해 만들어진 웹도 자주 접하게 되었습니다. 저도 계속 관심은 있었지만, 제대로 사용해보지는 못했었네요. 이번 기회에 Three.js를 사용해 공부해보겠습니다.

[Three.js](https://threejs.org/)사이트에 접속하면 이 라이브러리로 만든 프로젝트들을 볼 수 있는데, 정말 멋지고 신기했습니다. 어떻게 동작하는지 알아보고 기술을 익혀서, 머릿속에만 있던 프로젝트를 얼른 완성시키고 싶어요. 😳

# threeJs

Three.js는 웹에서 3D 그래픽스를 쉽게 만들 수 있는 자바스크립트 라이브러리입니다. WebGL을 기반으로 3D 애니메이션, 모델링, 렌더링 작업을 단순화하여 3D를 쉽게 생성할 수 있습니다. Three.js를 통해 애니메이션이나 3D 장면이 추가된 인터랙티브한 웹을 만들 수 있습니다.

# 설치

npm 으로 모튤을 설치합니다. typescript를 사용하시는 분이면 three의 type도 설치를 해줍니다!
```bash
npm install three
npm i --save-dev @types/three # for 타입스크립트
```

리액트에서 Three.js를 더 쉽게 사용할 수 있게 해주는 [react-three-fiber](https://docs.pmnd.rs/react-three-fiber/getting-started/introduction) 라이브러리도 있습니다. 저는 리액트에서 프로젝트를 진행할 예정이지만, Three.js를 더 자세히 알아보기 위해 Three.js를 설치했습니다.

# Init

제일 먼저 기본 시작 셋팅을 하겠습니다. Three.js는 기본적으로 캔버스에 렌더링되기 때문에, 캔버스 엘리먼트가 꼭 필요합니다. 

```javascript
import { useEffect } from "react";
import * as THREE from "three";
export default function ThreePage({}) {
  const initThree = () => {
    const scene = new THREE.Scene();
  };
  useEffect(() => {
    initThree();
  });
  return (
    <>
      <canvas id="canvas"></canvas>
    </>
  );
}
```
1. THREE import 해오기
2. canvas태그 생성
3. init 함수 생성
4. THree Scene 생성

# Scene 생성

initThree() 함수 안에서 씬 생성 이후부터 작성합니다.

three.js로 무언가를 만드려면 scene, camera, renderer 는 필수입니다!

## scene
```javascript
// scene 생성
const scene = new THREE.Scene();
// scene 설정
scene.background = new THREE.Color("skyblue");
```

Scene은 3D 장면을 구성하고 관리하는 기본 컨테이너입니다. 렌더링할 항목과 위치를 설정하여 물체, 조명, 카메라등을 배치할 수 있습니다.

scene.background 와 같이 조명, 안개(fog), 배경색 등 장면의 전역 상태를 설정 수도 있습니다.

## camera
```javascript
// 카메라 생성
const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
// 카메라 설정 (좌표 : x, y, z )
camera.position.set(0, 0, 2);
```
- PerspectiveCamera : 사람의 눈으로 보는 방식 사용. (x, y ,z) 좌표로 3D 장면 렌더링 시 좋음.
- OrthographicCamera : z 좌표가 없음. 2D 장면과 UI 요소를 렌더링하는 데 좋음.
- ArrayCamera : 미리 설정해놓은 카메라로 장면을 효율적으로 렌더릴할 때 사용. VR 구현 시 좋음.

카메라의 종류는 엄청 다양합니다! (공식 문서에는 더 있어요.) 저는 3D를 구현할 거라서 PerspectiveCamera를 사용했습니다.

PerspectiveCamera의 파라미터는 4가지(순서대로 fov, aspect, near, far)로 구성되어있습니다.
 
- fov : 카메라 시야각. 높아질 수록 더 넓은 범위를 볼 수 있음. Default 50.
- aspect : 카메라 가로 세로 비율. 비율과 렌더링 canvas가 맞지 않으면 찌그러짐. Default 1.
- near : 카메라기준 렌더링 할 가장 가까운 거리. Default 0.1.
- far : 카메라기준 렌더링 할 가장 먼 거리. Default 2000.

near보다 가까운 물체거나, far보다 먼 물체라면 화면에 렌더링 되지 않습니다. 이를 조정하여 앱 성능 향상을 고려할 수 있습니다.

## renderer
```javascript
// 렌더러 생성
const renderer = new THREE.WebGLRenderer({ canvas });
// 렌더러 설정
renderer.setSize(canvas.width, canvas.height);
```

Three.js의 Renderer는 앞서 설명한 Scene과 Camera를 사용해 3D 장면을 실제로 렌더링해주는 역할을 합니다. GPU를 사용해 3D 장면을 이미지로 변환하고, 이를 웹 페이지의 canvas 엘리먼트에 그립니다. 주로 WebGLRenderer를 사용합니다.

renderer.render(scene, camera) 메서드를 호출하면, Scene을 Camera의 시점에서 렌더링하여 canvas 엘리먼트에 출력합니다.

# 물체 추가하기

이제 기본적인 셋팅은 다 끝났으니 생성한 scene에 물체를 생성해서 렌더링을 해볼까요? 네모난 큐브 모양 물체를 만들어서 화면에 그려보겠습니다.

```javascript
// 큐브 생성
const geometry = new THREE.BoxGeometry(1, 1, 1);

// 재질 생성 (색상 지정)
const material = new THREE.MeshBasicMaterial({ color: "orange" });

// 메쉬 생성 (큐브 + 재질)
const cube = new THREE.Mesh(geometry, material);

// 씬에 메쉬를 추가
scene.add(cube);
```

- Geometry : 3D 객체의 형태와 구조를 정의하는데 사용하며 다양한 종류가 있습니다. 육면체, 사각형, 원통형, 그리고 직접 그려 구현하는 모형까지 있습니다. 차차 알아보도록 하고 BoxGeometry를 사용하여 큐브 모양 물체를 만들어 봅시다. BoxGeometry(x, y, z) 순서대로 좌표를 찍어 생성할 수 있는데 1,1,1로 정육각형을 만들었습니다.

- Material : 객체의 질감이나 재질 등을 정의하는 데 사용하고, 다양한 종류가 있습니다. 빛의 영향을 받지 않는 기본적인 재질인 MeshBasicMaterial, 표면이 부드럽고 빛을 반사하는 MeshLambertMaterial등 다양한 재질이 있습니다. 속성으로 색, 거칠기, 투명도, 굴절등 다양한 속성을 추가할 수 있습니다.

- Mesh : Geometry와 Material를 합쳐 3D 객체를 생성합니다.


# scene 렌더링
씬에다가 큐브까지 생성을 해서 추가해주었는데 왜 아무 것도 렌더링되지 않았을까요? 우리는 아직 아무것도 렌더링하지 않았습니다...!
renderer.render(scene, camera);로 화면에 렌더링 추가를 해줍시다.

init 함수 제일 하단에 추가를 하면 하늘색 화면에 주황색 정육면체가 보이면 잘 따라오신 겁니다. 여기에 간단한 애니메이션도 추가해보겠습니다.

requestAnimationFrame라는 함수를 사용할 건데요. 화면 새로 고침 빈도에 맞춰 실행되면서 (1초에 60번정도), 큐브에 애니메이션을 추가해줄 거예요. 

```info
setInterval은 설정한 시간 간격마다 콜백 함수를 호출하는 방면 화면
새로고침 빈도에 맞춰 실행되는 requestAnimationFrame 함수를 사용하면
더욱 부드러운 애니메이션 구현이 가능합니다.
```

```javascript
function animate() {
    requestAnimationFrame(animate);

    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    renderer.render(scene, camera);
}

animate();
```
함수가 호출될 때마다 물체를 움직이고 재렌더링을 해서 화면에 다시 그려줍니다.


# 3D 불러오기

이번엔 3D GLF 파일을 불러서 렌더링을 해보겠습니다.

자료는 [sketchfab](https://sketchfab.com/)에서 다운로드를 했습니다. 가입 후 검색 필터에 Downloadable을 선택하면 다운로드할 수 있는 무료 파일을 다운로드 받을 수 있습니다. 저는 [눈사람](https://sketchfab.com/3d-models/snow-man-0a7fb227e2c147178c576bdb6c1c5ea7#download)으로 했어요.

## GLTFLoader
three에서 지원하는 GLTF loader를 사용해서 렌더링할 거예요. 먼저 import를 해줍니다.

```javascript
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
```

위에서 생성했던 InitThree 함수에서 계속 진행했습니다. scene.add(cube) 코드는 잠시 주석으로 막아둡시다.

그리고 animate() 함수 위에 추가해주었습니다.

```javascript
// 눈사람 모델 로드
const loader = new GLTFLoader();
const url = `${process.env.PUBLIC_URL}/snow_man.glb`;
const snowman = await loader.loadAsync(url);

snowman.scene.position.set(0, 0, 0);

// Scene에 추가
scene.add(snowman.scene);
```

파일을 구하는 데도 한참 걸리고 열심히 추가했는데... 눈사람이 흙사람이 되어서 렌더링되었습니다. 😓 왜 그림자만 렌더링되는지 찾아보니, Three.js에서 3D 모델이 제대로 렌더링되기 위해서는 조명 설정과 모델의 재질 설정이 중요하다고 합니다.

그래서 눈사람 모델을 로드하고 추가하기 이전에 햇빛 같은 조명(Directional Light)과 모든 방향에서 균일하게 비추는 빛(Ambient Light)을 추가했습니다.

```javascript
// 조명 추가
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
light.castShadow = true;// 그림자 설정

const ambientLight = new THREE.AmbientLight(0x404040); // 약간의 주변광 추가
scene.add(ambientLight);
```
밝아진 눈사람이 나왔습니다!! ☃️


# 응용
아까 추가해봤던 큐브는 삭제하고, 눈이 쌓인 것처럼 하얀색 바닥을 추가해주겠습니다.

# 컨트롤

진짜 마지막 입니다. 처음 시작에는 어떤 것부터 해야하나 막막했는데 역시 __keep going!__

하나 시작하니 계속 욕심이 생기네요. 마우스로 화면을 돌리면서 확인할 수 있게 컨트롤을 추가해보겠습니다. [OrbitControls](https://threejs.org/docs/#examples/ko/controls/OrbitControls)를 사용할 거예요.

```javascript
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
```

설치를 위해 npm 으로 접속했더니 

```warning
three-js exposes real modules now via three/examples/jsm/... for example to import Orbit, do import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
```

이제는 사용하지 않고 바로 three 라이브러리에서 사용할 수 있다고 합니다!

공식 문서에서는 이렇게 설명하고 있습니다:
> 모든 속성들이 three 모듈에서 바로 불러와지는 것은 아닙니다. ("bare import"라고도 불리는). 다른 자주 쓰이는 라이브러리들, controls, loaders, post-processing effects 같은 것들은 examples/jsm 의 하위폴더에서 불러와야 합니다. 더 자세한 내용을 알아보려면, 아래 내용을 참고하세요.

이런 안내를 보고 귀찮아지겠다고 생각했는데, 실제로는 훨씬 수월해졌습니다. 😁

그리고 이제 animate() 함수를 실행하기 전에 control을 추가하기만 하면, 캔버스를 확대 축소하거나 마우스 드래그로 시야를 자유자재로 변경할 수 있습니다.


```javascript
// control 추가
const controls = new OrbitControls(camera, renderer.domElement);
controls.update();
```

# 응용

하늘색 화면에 눈사람만 둥둥 떠다니니 너무 허전해서 주변을 꾸며주고 마무리 하겠습니다. (처음에 만든 cube는 지웠어요.)

## 바닥 불러오기

PlaneGeometry 를 사용하여 눈이 쌓인 것 같은 흰 바닥을 만들어줍니다.
```javascript
// 바닥 생성 및 Scene에 추가
const geometry = new THREE.PlaneGeometry(10, 10);
const material = new THREE.MeshBasicMaterial({ color: "#fff" });
const ground = new THREE.Mesh(geometry, material);
ground.rotation.x = -Math.PI / 2;
scene.add(ground);
```
rotation.x = -Math.PI / 2; 속성을 주어 가로로 눕혀지게 만들고 scene에 추가해주었습니다.

## 물체 여러개 추가하기

눈사람 주변에 눈이 떠있도록 하고 싶어서 눈 메쉬를 만들고 포지션을 설정한 후, 추가하고 위치를 바꿔서 다시 추가하는 식으로 작업했더니 마지막에 추가한 메쉬만 화면에 렌더링 되더라고요.

똑같은 geometry를 여러 개 추가하고 싶으면 각 메쉬를 여러 개 만들어줘야 합니다. 하지만 하나씩 일일이 언제 만들고 있습니까... 🤨 (귀찮아) 그래서 메쉬를 생성하는 함수를 만들고, 위치만 추가하여 여러 개의 눈을 생성했습니다.

이번에는 MeshToonMaterial을 사용해봤는데요, 이 재질은 만화적인 느낌을 표현할 수 있다고 합니다. 학습용 프로젝트를 할 때 가장 도움되는 것은 속성이나 여러 가지 메서드를 호출해보는 것입니다. 됐다! 하고 그냥 넘어가는 게 아니라 저처럼 이것저것 꼭 적용해보고 시도해보세요!

```javascript
// 눈 생성 및 scene 에 추가
const snowGeometry = new THREE.SphereGeometry(0.03, 0.03, 36);
const snowMaterial = new THREE.MeshToonMaterial({
  color: 0xffffff,
});

const createSnow = (x: number, y: number, z: number) => {
  const snow = new THREE.Mesh(snowGeometry, snowMaterial);
  snow.position.set(x, y, z);
  scene.add(snow);
};

createSnow(0.5, 0.5, 0.1);
createSnow(0.2, 0.5, 0.3);
createSnow(-0.2, 0.7, 0.2);
createSnow(-0.5, 0.3, -0.3);
createSnow(0.2, 0.3, -0.1);
createSnow(0.2, 0.3, 0.3);
createSnow(-0.2, 0.3, 0);
```

# 결과물

짜잔 🎉☃︎❄️

![result](/assets/images/20240522/result01.png)

프로젝트를 직접 만들어 보면서 공식 문서를 참고하는 것이 가장 빠르게 습득하는 방법인 것 같아요. 그렇게 하다 보면 욕심도 생기고, 하고 싶은 것도 많아져서 이것저것 찾아보다 보면 자연스럽게 많이 알게 되고 이해도 더 쉽게 됩니다. 다음에는 좌표에 대해 좀 더 알아봐야겠습니다. 옆에 조형물들을 추가하는데 좌표 설정이 너무 헷갈려서 시간이 제일 오래 걸렸던 것 같아요. three.js를 수월하게 사용할 수 있는 멋진 내가 될 때까지 파이팅! 😎

## 최종 코드
```javascript
import { useEffect } from "react";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
export default function ThreePage({}) {
  const initThree = async () => {
    const canvas = document.getElementById("canvas") as HTMLCanvasElement;

    // Canvas 크기 설정
    canvas.width = 500;
    canvas.height = 500;

    // Scene 만들기
    const scene = new THREE.Scene();
    scene.background = new THREE.Color("skyblue");
    scene.fog = new THREE.Fog(0xcccccc, 10, 15);

    // Renderer 생성 및 크기 설정
    const renderer = new THREE.WebGLRenderer({ canvas });
    renderer.setSize(canvas.width, canvas.height);

    // 카메라 생성 및 위치 설정
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 10);
    camera.position.set(0, 0, 2);

    // 바닥 생성 및 Scene에 추가
    const geometry = new THREE.PlaneGeometry(10, 10);
    const material = new THREE.MeshBasicMaterial({ color: "#fff" });
    const ground = new THREE.Mesh(geometry, material);
    ground.rotation.x = -Math.PI / 2;
    scene.add(ground);

    // 조명 추가
    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 5, 5);
    light.castShadow = true;
    scene.add(light);

    const ambientLight = new THREE.AmbientLight(0x404040); // 약간의 주변광 추가
    scene.add(ambientLight);

    // 눈사람 모델 로드
    const loader = new GLTFLoader();
    const url = `${process.env.PUBLIC_URL}/snow_man.glb`;
    const snowman = await loader.loadAsync(url);

    snowman.scene.position.set(0, 0, 0);

    // Scene에 추가
    scene.add(snowman.scene);

    // 조형물 생성 및 scene 에 추가
    const coneGeometry = new THREE.ConeGeometry(0.1, 0.3, 4);
    const coneMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });

    // 여러 개의 조형물을 다른 위치에 추가
    const conePositions = [
      { x: 0.4, y: 0.1, z: 0.3 },
      { x: 0.2, y: 0.1, z: 0 },
      { x: -0.2, y: 0.1, z: 0.2 },
      { x: -0.3, y: 0.1, z: -0.2 },
    ];

    conePositions.forEach((pos) => {
      const cone = new THREE.Mesh(coneGeometry, coneMaterial);
      cone.position.set(pos.x, pos.y, pos.z); // 원하는 위치로 조절
      scene.add(cone);
    });

    // 눈 생성 및 scene 에 추가
    const snowGeometry = new THREE.SphereGeometry(0.03, 0.03, 36);
    const snowMaterial = new THREE.MeshToonMaterial({
      color: 0xffffff,
    });

    const createSnow = (x: number, y: number, z: number) => {
      const snow = new THREE.Mesh(snowGeometry, snowMaterial);
      snow.position.set(x, y, z);
      scene.add(snow);
    };

    createSnow(0.5, 0.5, 0.1);
    createSnow(0.2, 0.5, 0.3);
    createSnow(-0.2, 0.7, 0.2);
    createSnow(-0.5, 0.3, -0.3);
    createSnow(0.2, 0.3, -0.1);
    createSnow(0.2, 0.3, 0.3);
    createSnow(-0.2, 0.3, 0);

    // control 추가
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.update();

    const animate = () => {
      requestAnimationFrame(animate);

      snowman.scene.rotation.y += 0.01;
      // controls.update();

      renderer.render(scene, camera);
    };

    animate();
    // 초기 렌더링 호출
    renderer.render(scene, camera);
  };

  useEffect(() => {
    initThree();
  }, []);

  return (
    <>
      <canvas
        id="canvas"
        style={{ display: "block", width: "500px", height: "500px" }}
      ></canvas>
    </>
  );
}
```