---
layout: post
title: Three.js 시작하기
description: react에서 Three.js를 사용해서 object를 만들어보자! 
date: 2024-05-22 10:58:31 +09:00
categories: javascript
tags: threejs interactive javascript
---

회사에서도 AR이 구현 테스트를할 때 Three.js를 찍어먹기 해봤습니다. 이곳저곳에서 관심도 많이 보이고, 이를통해 만들어진 웹도 자주 접하게 됐습니다. 저도 계속 관심은 있는 상태로 한번 제대로 사용해보고 싶다는 생각만 하고 실천을 못했었네요. 이번 기회에 Three.js를 한번 사용해보며 공부해보겠습니다.

[Three.js](https://threejs.org/)로 접속을 하면 이 라이브러리를 사용해서 만든 프로젝트들을 볼 수 있는데 너무 이쁘고 신기했습니다. 어떻게 동작이 되는지 알아보고 기술을 익혀서 머리로만 생각하고 있는 프로젝트를 얼른 완성시키고 싶어요. 😳

# threeJs

Three.js는 웹에서 3D 그래픽스를 쉽게 만들 수 있는 자바스크립트 라이브러리입니다. WebGL 기반으로 3D 애니메이션, 모델링, 렌더링 작업을 단순화하여 3D를 쉽게 생성할 수 있습니다. Three.js를 통해서 애니메이션이나 3D 장면이 추가 된 인터랙티브한 웹을 만들 수 있습니다.

# 설치

npm 으로 모튤을 설치합니다. typescript를 사용하시는 분이면 three의 type도 설치를 해줍니다!
```bash
npm install three
npm i --save-dev @types/three # for 타입스크립트
```

리액트에서 three.js를 더 쉽게 사용할 수 있게 제공하는 <span class="h-yellow">react-three-fiber</span> 라이브러리도 있습니다. 저는 리액트에서 프로젝트를 진행할 예정이지만 Three.js를 더 자세히 알아보기위해서 Three.js를 설치했습니다.

# Init

ThreeJs는 기본적으로 canvas태그에 렌더링되기때문에 canvas태그가 꼭 필요합니다. canvas태그와 함께 씬 생성을 하겠습니다.

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


# Scene 만들기

initThree() 함수 안에서 씬 생성 이후부터 작성합니다.

three.js로 무언가를 만드려면 scene, camera, renderer 는 필수입니다!

```javascript
// scene 만들기
const scene = new THREE.Scene();

// scene 배경 설정
scene.background = new THREE.Color("skyblue");

// threeJs 렌더링 설정
const renderer = new THREE.WebGLRenderer({ canvas });
renderer.setSize(canvas.width, canvas.height);

// 카메라(Camera) 생성
const camera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);

// 카메라 위치 설정 (x, y, z 좌표)
camera.position.set(0, 0, 5);
```

첫 번째 속성은 field of view(시야각)입니다. FOV(시야각)는 해당 시점의 화면이 보여지는 정도를 나타냅니다. 값은 각도 값으로 설정합니다.

두 번째 속성은 aspect ratio(종횡비)입니다. 대부분의 경우 요소의 높이와 너비에 맞추어 표시하게 할텐데, 그렇지 않으면 와이드스크린에 옛날 영화를 트는 것처럼 이미지가 틀어져 보일 것입니다.

다음 두 속성은 near 와 far 절단면입니다. 무슨 뜻인가 하면, far 값 보다 멀리 있는 요소나 near 값보다 가까이 있는 오브젝트는 렌더링 되지 않는다는 뜻입니다. 지금 시점에서 이것까지 고려할 필요는 없지만, 앱 성능 향상을 위해 사용할 수 있습니다.

다음은 renderer입니다. 마법이 일어나는 곳입니다. 같이 사용하는 WebGLRenderer와 더불어, three.js는 다른 몇가지 renderer를 사용하는데, 오래된 브라우저 혹은 모종의 사유로 WebGL을 지원 안할때의 대비용으로 사용하는 것입니다.

renderer 인스턴스를 생성함과 동시에, 렌더링할 곳의 크기를 설정해줘야 합니다. 렌더링할 구역의 높이와 너비를 설정하는 것은 좋은 방법입니다. 이 경우, 높이와 너비는 각각 브라우저 윈도우의 크기가 됩니다. 성능 개선을 중시하는 앱의 경우, setSize를 사용하거나 window.innerWidth/2, window.innerHeight/2를 사용해서 화면 크기의 절반으로 구현할 수도 있습니다.

사이즈는 그대로 유지하고 싶지만 더 낮은 해상도로 렌더링하고 싶을 경우, setSize의 updateStyle (세 번째 인자)를 false로 불러오면 됩니다. setSize(window.innerWidth/2, window.innerHeight/2, false)처럼 사용하면 <canvas>가 100%의 높이, 너비로 되어있다는 기준 하에 절반의 해상도로 렌더링 될 것입니다.

마지막으로 제일 중요한 renderer 엘리먼트를 HTML 문서 안에 넣었습니다. 이는<canvas> 엘리먼트로, renderer가 scene을 나타내는 구역입니다.


# cube 추가하기

```javascript
 // 큐브(Geometry) 생성
const geometry = new THREE.BoxGeometry(1, 1, 1);

// 재질(Material) 생성 (색상 지정)
const material = new THREE.MeshBasicMaterial({ color: "orange" });

// 메쉬(Mesh) 생성 (큐브와 재질을 결합)
const cube = new THREE.Mesh(geometry, material);

// 위에서 생성한 메쉬 추가
scene.add(cube);
```
큐브를 만드려면, BoxGeometry가 필요합니다. 여기에는 큐브에 필요한 모든 꼭짓점 (vertices) 와 면(faces)이 포함돼 있습니다. 여기에 대해서는 나중에 더 자세히 알아봅시다.

geometry와 더불어, 무언가를 색칠해줄 요소가 필요합니다. Three.js에서는 여러 방법을 고려했지만, 현재로서는MeshBasicMaterial을 고수하고자 합니다. 이 속성이 적용된 오브젝트들은 모두 영향을 받을 것입니다. 가장 단순하게 알아볼 수 있도록, 여기에서는 녹색인 0x00ff00만을 속성으로 사용하겠습니다. CSS 나 Photoshop에서처럼 (hex colors)로 동일하게 작동합니다.

세 번째로 필요한 것은Mesh입니다. mesh는 기하학을 받아 재질을 적용하고 우리가 화면 안에 삽입하고 자유롭게 움직일 수 있게 해 줍니다.

기본 설정상 scene.add()를 불러오면, 추가된 모든 것들은 (0,0,0) 속성을 가집니다. 이렇게 되면 카메라와 큐브가 동일한 위치에 겹치게 되겠죠. 이를 피하기 위해, 카메라를 약간 움직여 두었습니다.

# scene 렌더링
씬에다가 큐브까지 생성을 해서 추가해주었는데 왜 아무 것도 렌더링되지 않았을까요? 우리는 아직 아무것도 렌더링하지 않았습니다...!
 render or animate loop라는 것으로 렌더링을 해줘야합니다.
    renderer.render(scene, camera);

init 함수 제일 하단에 추가를 하면
짜ㅏ잔
화면에 렌더링 되었죠?
여기에 간단한 애니메이션을 추가해보겠습니다.

requestAnimationFrame라는 함수를 사용할 건데요. 모든 프레임마다(화면이 새로고침 될 때마다) 실행되면서 (1초에 60번정도), 큐브에 애니메이션을 추가해줄 거예요. setInterval을 검색을 해서 비교대상으로 봤거나, 웹 애니메이션 구현을 해보거나 검색을 해보았다면 한번쯤은 봤던 함수죠?

```javascript
function animate() {
    requestAnimationFrame(animate);

    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;

    renderer.render(scene, camera);
}

animate();
```

# 완성코드 
```javascript
import * as THREE from "three";
import { Canvas, useFrame, ThreeElements } from "@react-three/fiber";
import { useState, useRef, useEffect } from "react";

export default function Page() {
  const canvasRef = useRef<HTMLCanvasElement>(null!);

  useEffect(() => {
    if (!canvasRef) return;
  });
  return (
    <Canvas
      camera={{
        position: [0, 0, 10],
      }}
    >
      <ambientLight />
      <Cube position={[0, 0, 0]} />
    </Canvas>
  );
}

type CubeProps = ThreeElements["mesh"];

export function Cube(props: CubeProps) {
  const meshRef = useRef<THREE.Mesh>(null!);
  const [hovered, setHover] = useState(false);
  const [active, setActive] = useState(false);
  useFrame((state, delta) => {
    meshRef.current.rotation.x += delta;
    meshRef.current.rotation.y += delta;
  });
  return (
    <mesh
      ref={meshRef}
      scale={active ? 1.5 : 1}
      onClick={(event) => setActive(!active)}
      onPointerOver={(e) => setHover(true)}
      onPointerOut={(e) => setHover(false)}
      {...props}
    >
      <boxGeometry args={[5, 5, 5]} />
      <meshStandardMaterial color={hovered ? "hotpink" : "orange"} />
    </mesh>
  );
}

```



# 3D 불러오기

이번엔 3D GLF 파일을 불러서 렌더링을 해보겠습니다.

자료는 [sketchfab](https://sketchfab.com/)에서 다운로드를 했습니다. 가입 후 검색 필터에 Downloadable을 선택하면 다운로드할 수 있는 무료 파일을 다운로드 받을 수 있습니다. 저는 [눈사람](https://sketchfab.com/3d-models/snow-man-0a7fb227e2c147178c576bdb6c1c5ea7#download)으로 했어요.

## GLTFLoader
three에서 지원하는 GLTF loader를 사용해서 렌더링할 거예요. 먼저 import를 해줍니다.
```javascript
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
```
위에서 생성했던 InitThree 함수에서 계속 진행했습니다. scene.add(cube) 코드는 잠시 주석으로 막아줍시다..

animate() 함수 위에 추가해주었습니다.
```javascript
// GLTF 모델 로드 및 Scene에 추가
const loader = new GLTFLoader();
const url = `${process.env.PUBLIC_URL}/snow_man.glb`;
loader.load(
    url,
    function (gltf) {
        scene.add(gltf.scene);
        renderer.render(scene, camera);
    },
    undefined,
    function (error) {
        console.error(error);
    }
);
```
파일 구하는 데에도 한참 걸리고 열심히 추가를 해주었는데... 눈사람이 흙사람이 되어서 렌더링이 되었습니다. 😓 왜 그림자만 렌더링되는지 찾아보니 Three.js에서 3D모델이 제대로 렌더링되기 위해서는 조명 설정도 중요하고 모델의 재질 설정도 중요하다고 합니다.
```javascript
// 조명 추가
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
light.castShadow = true;// 그림자 설정

const ambientLight = new THREE.AmbientLight(0x404040); // 약간의 주변광 추가
scene.add(ambientLight);
```

밝아진 눈사람이 나왔습니다. 추가한 조명은 여려종류가 있는데요.

TODO:

## 응용
아까 추가해봤던 cube를 이용해서 바닥에 눈이 있는 것처럼 보이게 해보겠습니다.

```javascript
const initThree = async () => {
const canvas = document.getElementById("canvas") as HTMLCanvasElement;

// Canvas 크기 설정
canvas.width = 500;
canvas.height = 500;

// Scene 만들기
const scene = new THREE.Scene();
scene.background = new THREE.Color("skyblue");

// Renderer 생성 및 크기 설정
const renderer = new THREE.WebGLRenderer({ canvas });
renderer.setSize(canvas.width, canvas.height);

// 카메라 생성 및 위치 설정
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
camera.position.set(0, 0, 2);

// 큐브 생성 및 Scene에 추가
const geometry = new THREE.BoxGeometry(10, 10, 1);
const material = new THREE.MeshBasicMaterial({ color: "#fff" });
const cube = new THREE.Mesh(geometry, material);
cube.position.set(0, -5, 0); // y 위치 조정
scene.add(cube);

// 조명 추가
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 5, 5);
light.castShadow = true;
scene.add(light);

const ambientLight = new THREE.AmbientLight(0x404040); // 약간의 주변광 추가
scene.add(ambientLight);

// GLTF 모델 로드
const loader = new GLTFLoader();
const url = `${process.env.PUBLIC_URL}/snow_man.glb`;
const snowman = await loader.loadAsync(url);
snowman.scene.rotation.y = 10;

// Scene에 추가
scene.add(snowman.scene);
const animate = () => {
    requestAnimationFrame(animate);

    snowman.scene.rotation.y += 0.01;

    renderer.render(scene, camera);
};

animate();
// 초기 렌더링 호출
renderer.render(scene, camera);
};
```

# 컨트롤

진짜 마지막 입니다. 처음 시작에는 어떤 것부터 해야하나 막막했는데 역시 keep going~ 하나 시작하니 계속 욕심이 생기네요. 마우스로 화면을 돌리면서 확인할 수 있게 컨트롤을 추가해보겠습니다. [OrbitControls](https://threejs.org/docs/#examples/ko/controls/OrbitControls)를 사용할 거예요.
```javascript
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
```

# objects 추가
눈사람 주변에 눈이 떠있도록 추가를 좀 해보겠습니다.