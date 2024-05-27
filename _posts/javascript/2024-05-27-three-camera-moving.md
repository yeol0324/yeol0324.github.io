---
layout: post
title: three.js 객체(object) 움직이기
summary: three.js 사용자 인터렉션 키보드 이벤트로 물체 이동 구현하기
date: 2024-05-27 11:46:49 +09:00
categories: javascript
tags: threejs interactive javascript
---

three.js 두번째 작성 글입니다.

먼저 최종 목표로 만들고 싶은 작업물을 소개하겠습니다. 화면의 중심에 캐릭터가 지구 모양의 바닥을 돌아다니는 장면을 구현하고 싶습니다. 어떤 라이브러리나 언어를 배울 때, 무작정 프로젝트를 따라 하기보다는 자신이 만들고 싶은 프로젝트를 먼저 구상하고, 그 프로젝트에 필요한 기술을 하나씩 배워나가는 것이 이해도 빠르고 기억에도 오래 남는다는 것을 경험했습니다. 오늘도 원하는 프로젝트에 한 걸음 더 다가가기 위해 키보드를 이용한 캐릭터 이동과 카메라 처리를 적용해보겠습니다.

# 시작하기 전에
먼저 기본 시작은 이전 글[Three.js 시작하기]({{base_path}}/javascript/three-js-start/)에 이어서 하려고 합니다.

전 글에서 작성한 코드는 init 함수에 때려넣었더니, 기능을 추가하거나 수정할 때 찾기가 어려웠습니다. 😕 처음부터 이러면 안 되는데... 하지만 이렇게 하라고 리팩토링이 있는 거죠! 그래서 기능별로 함수를 나누어 리팩토링을 했습니다.

```javascript
const init = async () => {
  const canvas = document.getElementById("canvas") as HTMLCanvasElement;
  setupCanvas(canvas);

  const scene = createScene();
  const renderer = createRenderer(canvas);
  const camera = createCamera();
  const controls = createControls(camera, renderer.domElement);

  addGround(scene);
  addLights(scene);

  const me = createSphere();
  scene.add(me);

  const animate = createAnimateFunction(
      renderer,
      me,
  );
  animate();

  renderer.render(scene, camera);
};

// Ground 추가 함수
const addGround = (scene: THREE.Scene) => {
  const groundGeometry = new THREE.PlaneGeometry(10000, 10000);
  const groundMaterial = new THREE.MeshStandardMaterial({
    color: 0x00ff00,
  });
  const ground = new THREE.Mesh(groundGeometry, groundMaterial);
  ground.rotation.x = -Math.PI / 2; // 평면을 수평으로 
  scene.add(ground);
};
```
이런 식으로 코드를 함수로 분리했습니다. 최종 코드는 마지막에서 확인하세요.

## 카메라 설정
OrbitControls을 사용하고 있었는데, 카메라 시야가 바닥을 뚫고 넘어가는 문제가 있어서 카메라 각도에 제한을 주었습니다. 이를 위해 maxPolarAngle 속성을 사용할 수 있습니다.
```javascript
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.maxPolarAngle = Math.PI / 2;
```

# 키보드 이벤트 추가

Three.js에는 다양한 카메라 컨트롤이 있지만, 지금 하고 싶은 것은 카메라를 움직이는 것이 아닌 키보드로 물체를 이동하는 기능입니다. 키보드를 사용하기 위해서는 우선 키보드 이벤트를 받아야 합니다. <code>document.addEventListener("keydown", function)</code> 코드를 사용해서 추가해보겠습니다.먼저 빈 키 객체를 생성하고, 이를 animate 함수에 전달합니다. <code>animate</code> 함수는 차차 확인해봅시다.

```javascript
const init = () =>{
// ...
  const keys = setupKeyControls();
  const animate = createAnimateFunction(
    renderer,
    scene,
    camera,
    controls,
    me,
    keys
  );
  animate();
// ...
}

const setupKeyControls = () => {
  const keys = {};

  document.addEventListener("keydown", (event) => {
   keys[event.key] = true;
  });

  document.addEventListener("keyup", (event) => {
   keys[event.key] = false;
  });

  return keys;
};
```
_코드를 간결하게 표현하기 위해서 typescript를 위한 코드는 삭제되었습니다. 최종 코드에서 확인 가능합니다._

## 앞뒤좌우 컨트롤

키 객체에 담겨있는 값을 확인해서 물체의 x, z 좌표 값을 업데이트해줍니다. 3D로 표현되기 때문에 y는 상하 좌표이고, 앞뒤는 z, 좌우는 x값을 가지고 있습니다.
```javascript
// 애니메이션 함수 생성 함수
function createAnimateFunction(
  renderer: THREE.Renderer,
  scene: THREE.Scene,
  camera: THREE.Camera,
  controls: OrbitControls,
  object: THREE.Mesh, // 이동할 기준이 될 물체 전달
  keys: KeyState
) {
  const updatePosition = () => {

    // 키보드 입력에 따라 물체 이동
    if (keys["ArrowUp"]) object.position.z -= 0.05;
    if (keys["ArrowDown"]) object.position.z += 0.05;
    if (keys["ArrowLeft"]) object.position.x -= 0.05;
    if (keys["ArrowRight"]) object.position.x += 0.05;
  };

  const animate = () => {
    requestAnimationFrame(animate);
    updatePosition();

    renderer.render(scene, camera);
  };

  return animate;
}
```

## 점프 로직 추가

스페이스를 눌렀을 때 점프도 표현을 해볼까요?
```javascript
    if (keys[" "]) object.position.y += 0.05;
```

이렇게 하면 원하는 대로 동작하지 않습니다. Three.js에는 우리가 생각하는 중력이 작용하고 있지 않거든요. 🥲 하지만 간단한 중력 효과를 구현하면 되죠! 완전 럭키비키잖앙 🍀

```javascript
function createAnimateFunction(
  let isJumping = false;
  let jumpSpeed = 0;
  const gravity = 0.005;
  const jumpStrength = 0.15;
  const initialY = object.position.y;
  // ...
  const handleJump = () => {
    if (keys[" "] && !isJumping) {
      isJumping = true;
      jumpSpeed = jumpStrength;
    }

    if (isJumping) {
      object.position.y += jumpSpeed;
      jumpSpeed -= gravity;

      if (object.position.y <= initialY) {
        // 땅에 도달했을 때
        object.position.y = initialY;
        isJumping = false;
        jumpSpeed = 0;
      }
    }
  };
  // ...
)
```

<code>animate</code> 함수 안에 handleJump() 추가하는 것도 잊지 마세요!

무한 점프를 방지하기 위해 isJumping 값을 설정해두었습니다. 물체는 jumpSpeed 값으로 위치시킨 후, 점프가 시작된 후에는 중력(gravity)만큼 점점 감소하게 만들었습니다. object.position.y를 미리 저장해두어 땅에 도달했을 때 물체가 땅보다 더 아래로 꺼지지 않도록 조정했습니다.


# 움직이는 물체 따라가기
물체를 움직이는 기능은 완전 성공입니다! 이제 카메라도 움직이는 물체에 따라서 이동하게 만들어볼까요? updateCamera 함수를 생성해줍니다.
```javascript
  const updateCamera = () => {
    camera.position.x = object.position.x + 5;
    camera.position.y = object.position.y + 2;
    camera.position.z = object.position.z + 5;
    camera.lookAt(object.position);
  };
```
requestAnimationFrame으로 animate() 함수가 실행될 때마다 updateCamera 함수를 호출합니다. updatePosition()을 호출한 바로 아래에서 호출하면 됩니다. 카메라의 위치를 물체의 위치보다 살짝 떨어지게 설정합니다. <code>lookAt</code>를 사용하여 카메라가 항상 물체를 바라보도록 설정합니다. lookAt 메서드는 카메라의 시야를 특정 좌표(여기서는 object.position)로 맞춥니다.

# 카메라 기준 이동
그런데 컨트롤이 뭔가 이상해요. ⬆️ 키를 눌러도 대각선 방향으로 이동하고, ⬅️ 키를 눌러도 계속 대각선으로 이동합니다. Three.js의 좌표가 우리가 생각하는 대로 되어있지 않아서 그렇습니다! 화면 기준으로 앞, 뒤, 좌, 우로 움직이도록 하려면 카메라의 방향을 고려해야 합니다. <code>camera.getWorldDirection</code>을 사용하여 카메라의 방향 벡터를 얻고, 그 방향을 기준으로 물체를 움직여야 합니다.
```javascript
 const updatePosition = () => {
    // 카메라의 방향 벡터 계산
    const direction = new THREE.Vector3();
    camera.getWorldDirection(direction);
    direction.y = 0; // 수평 이동만 허용
    direction.normalize();

    // 키보드 입력에 따라 물체 이동
    if (keys["ArrowUp"]) {
      object.position.addScaledVector(direction, 0.05);
    }
    if (keys["ArrowDown"]) {
      object.position.addScaledVector(direction, -0.05);
    }
    if (keys["ArrowLeft"]) {
      const left = new THREE.Vector3()
        .crossVectors(camera.up, direction)
        .normalize();
      object.position.addScaledVector(left, 0.05);
    }
    if (keys["ArrowRight"]) {
      const right = new THREE.Vector3()
        .crossVectors(direction, camera.up)
        .normalize();
      object.position.addScaledVector(right, 0.05);
    }
  };
```
<code>direction.normalize()<code> 메서드는 방향 벡터를 정규화합니다. 정규화는 벡터의 길이를 1로 만들어 방향만 유지하도록 합니다. 카메라의 방향 벡터의 길이에 따라 이동 거리가 달라질 수 있어 일관되지 않은 움직임이 발생할 수 있기때문에 방향만 유지하고 길이를 1로 만드는 것이 중요하다고 합니다. 좌,우 키는 <code>crossVectors</code> 메서드를 사용하여 방향 벡터를 계산해서 정규화한 후, 물체의 위치를 방향으로 이동시킵니다.


# 최종 코드
카메라 기준 좌표, 벡터 등등이 나오면서 조금 복잡해졌는데요. 😓 괜찮습니다! 차차 익히면 되니깐요. 오늘도 파이팅 ✨
```javascript
import { useEffect } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

export default function ThreePage() {
  const initThree = async () => {
    const canvas = document.getElementById("canvas") as HTMLCanvasElement;
    setupCanvas(canvas);

    const scene = createScene();
    const renderer = createRenderer(canvas);
    const camera = createCamera();
    const controls = createControls(camera, renderer.domElement);

    addGround(scene);
    addLights(scene);

    const me = createSphere();
    scene.add(me);
    const wall = createWall();
    scene.add(wall);

    const box = createBox();
    scene.add(box);

    const keys = setupKeyControls();
    const animate = createAnimateFunction(
      renderer,
      scene,
      camera,
      controls,
      me,
      keys
    );
    animate();

    renderer.render(scene, camera);
  };

  useEffect(() => {
    initThree();
  }, []);

  return (
    <canvas
      id="canvas"
      style={{ display: "block", width: "500px", height: "500px" }}
    ></canvas>
  );
}
type KeyState = {
  ArrowUp: boolean;
  ArrowDown: boolean;
  ArrowLeft: boolean;
  ArrowRight: boolean;
  " ": boolean;
};
// Canvas 설정 함수
const setupCanvas = (canvas: HTMLCanvasElement) => {
  canvas.width = 500;
  canvas.height = 500;
};

// Scene 생성 함수
const createScene = () => {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color("skyblue");
  return scene;
};

// Renderer 생성 함수
const createRenderer = (canvas: HTMLCanvasElement) => {
  const renderer = new THREE.WebGLRenderer({ canvas });
  renderer.setSize(canvas.width, canvas.height);
  return renderer;
};

// 카메라 생성 함수
const createCamera = () => {
  const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 100);
  camera.position.set(0, 2, 4);
  return camera;
};

// OrbitControls 생성 함수
const createControls = (camera: THREE.Camera, domElement: HTMLElement) => {
  const controls = new OrbitControls(camera, domElement);
  controls.maxPolarAngle = Math.PI / 2;
  controls.enableDamping = true; // 부드러운 감속 효과를 위해 damping 활성화
  controls.dampingFactor = 0.25;
  controls.update();
  return controls;
};

// Ground 추가 함수
const addGround = (scene: THREE.Scene) => {
  const groundGeometry = new THREE.PlaneGeometry(10000, 10000); // 매우 큰 평면
  const groundMaterial = new THREE.MeshStandardMaterial({
    color: 0x00ff00,
  });
  const ground = new THREE.Mesh(groundGeometry, groundMaterial);
  ground.rotation.x = -Math.PI / 2; // 평면을 수평으로 만듭니다
  scene.add(ground);
};

// 조명 추가 함수
const addLights = (scene: THREE.Scene) => {
  const light = new THREE.DirectionalLight(0xffffff, 1);
  light.position.set(5, 5, 5);
  light.castShadow = true;
  scene.add(light);

  const ambientLight = new THREE.AmbientLight(0x404040); // 약간의 주변광 추가
  scene.add(ambientLight);
};

// Sphere 생성 함수
const createSphere = () => {
  const sphereGeometry = new THREE.SphereGeometry(1, 32, 32);
  const sphereMaterial = new THREE.MeshStandardMaterial({ color: 0x0000ff });
  const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
  const radius = sphereGeometry.parameters.radius;
  sphere.position.set(-2, radius, 0); // 반지름에 맞게 y 위치 설정
  return sphere;
};

// Wall 생성 함수
const createWall = () => {
  const coneGeometry = new THREE.ConeGeometry(1, 3, 4);
  const coneMaterial = new THREE.MeshStandardMaterial({ color: 0xffffff });
  const wall = new THREE.Mesh(coneGeometry, coneMaterial);
  wall.position.set(0.2, 0.1, 0);
  return wall;
};

// Box 생성 함수
const createBox = () => {
  const boxGeometry = new THREE.BoxGeometry(1, 1, 1);
  const boxMaterial = new THREE.MeshStandardMaterial({ color: 0x00ffff });
  const box = new THREE.Mesh(boxGeometry, boxMaterial);
  const bbox = new THREE.Box3().setFromObject(box);
  const height = bbox.max.y - bbox.min.y;
  box.position.set(2, height / 2, 0); // 다른 위치에 추가
  return box;
};

// 키보드 컨트롤 설정 함수
const setupKeyControls = () => {
  const keys = {
    ArrowUp: false,
    ArrowDown: false,
    ArrowLeft: false,
    ArrowRight: false,
    " ": false,
  };

  const isKeyOfKeyState = (key: any): key is keyof KeyState =>
    key === "ArrowUp" ||
    key === "ArrowDown" ||
    key === "ArrowLeft" ||
    key === "ArrowRight" ||
    key === " ";

  document.addEventListener("keydown", (event) => {
    if (isKeyOfKeyState(event.key)) keys[event.key] = true;
  });

  document.addEventListener("keyup", (event) => {
    if (isKeyOfKeyState(event.key)) keys[event.key] = false;
  });

  return keys;
};

// 애니메이션 함수 생성 함수
function createAnimateFunction(
  renderer: THREE.Renderer,
  scene: THREE.Scene,
  camera: THREE.Camera,
  controls: OrbitControls,
  object: THREE.Mesh, // 움직일 물체
  keys: KeyState
) {
  let isJumping = false;
  let jumpSpeed = 0;
  const gravity = 0.005;
  const jumpStrength = 0.15;
  const initialY = object.position.y;

  const updatePosition = () => {
    // 카메라의 방향 벡터 계산
    const direction = new THREE.Vector3();
    camera.getWorldDirection(direction);
    direction.y = 0; // 수평 이동만 허용
    direction.normalize();

    // 키보드 입력에 따라 물체 이동
    if (keys["ArrowUp"]) {
      object.position.addScaledVector(direction, 0.05);
    }
    if (keys["ArrowDown"]) {
      object.position.addScaledVector(direction, -0.05);
    }
    if (keys["ArrowLeft"]) {
      const left = new THREE.Vector3()
        .crossVectors(camera.up, direction)
        .normalize();
      object.position.addScaledVector(left, 0.05);
    }
    if (keys["ArrowRight"]) {
      const right = new THREE.Vector3()
        .crossVectors(direction, camera.up)
        .normalize();
      object.position.addScaledVector(right, 0.05);
    }
  };

  const handleJump = () => {
    if (keys[" "] && !isJumping) {
      isJumping = true;
      jumpSpeed = jumpStrength;
    }

    if (isJumping) {
      object.position.y += jumpSpeed;
      jumpSpeed -= gravity;

      if (object.position.y <= initialY) {
        // 땅에 도달했을 때
        object.position.y = initialY;
        isJumping = false;
        jumpSpeed = 0;
      }
    }
  };

  const updateCamera = () => {
    camera.position.x = object.position.x + 5;
    camera.position.y = object.position.y + 2;
    camera.position.z = object.position.z + 5;
    camera.lookAt(object.position);
  };

  const animate = () => {
    requestAnimationFrame(animate);

    updatePosition();
    handleJump();
    updateCamera();

    renderer.render(scene, camera);
  };

  return animate;
}
```