---
layout: post
title: three.js 마우스 무빙
summary: StereoCamera 사용해서 사용자 인터렉션 마우스 따라 이벤트 구현하기
date: 2024-05-29 10:29:17 +09:00
categories: javascript
tags: threejs interactive javascript
---

three.js 세번째 작성 글입니다.

마우스 움직임에 따라 변화가 있는 웹을 접속해본 적이 있으신가요? 단순히 마우스 커서를 따라다니는 이벤트가 아니라, 마우스를 계속 쳐다보는 고양이라든지, 마우스 반대로 도망가는 오브젝트가 있다든지 하는 웹을 만난 적이 있으실 거예요. 저는 그런 기능이 구현된 사이트에 접속하면 단순하지만 재미있고 신기해서 머무는 시간이 길어지는 것을 느꼈습니다. 그래서 한번 구현해보고 싶어졌습니다. 오늘은 이 기능에 대해 알아보고 직접 구현해볼게요!

시작하기 전에 [예시](https://threejs.org/examples/#webgl_effects_anaglyph) 한번 보고 오세요.


# 오브젝트 고정

얼굴 이모지와 선글라스가 각각 다른 모델이어서 회전 이벤트를 받을 때 한 개의 모델인 것처럼 보이게 하기 위해 두 개를 고정시켜두고 싶었습니다. 이를 위해 sunglassObject를 faceObject의 자식으로 추가하여 함께 움직이도록 하겠습니다. 어떤 객체의 자식으로 추가하려면 scene에 바로 추가하는 것이 아니라, 해당 객체의 씬에 추가하면 됩니다.

sunglassObject의 위치를 조정하여 faceObject의 한쪽 벽면에 고정시켰습니다.

```javascript
sunglassObject.scene.position.set(0.5, 0, 0.5);
faceObject.scene.add(sunglassObject.scene);
```

이렇게 하면 faceObject와 sunglassObject가 함께 움직이며, 하나의 모델처럼 보이게 됩니다. 아... 좌표 잡기가 너무 힘들어요. 얼굴을 기준으로 x: 가운데, y: 가운데, z: 맨 앞으로 나오게 설정하는데 0.1씩 조정을 하며 원하는 위치로 배치했습니다. 그런데 앞으로 물체를 추가할 때마다 가운데로 배치하거나 맨 끝으로 배치할 때마다 0.1씩 조정을 할 수는 없습니다!

이 문제를 해결하기 위해서 좌표를 더 효율적으로 계산하는 방법을 사용할 수 있습니다. 

# 효율적인 좌표 잡기

모델의 정확한 위치를 맞추는 것은 수동으로 조정하는 것보다 더 효율적으로 할 수 있습니다. 여기서는 모델의 크기와 위치를 계산하여 적절한 위치에 배치하는 방법을 살펴보겠습니다.

Three.js에서는 객체의 크기와 경계를 계산하기 위해 <code>THREE.Box3</code>를 사용할 수 있습니다. 이를 사용하면 모델의 경계 상자를 계산하여 정확한 위치를 지정할 수 있습니다.


```javascript
// 경계 상자 계산
const faceBox = new THREE.Box3().setFromObject(faceObject.scene);

// faceObject의 크기 계산
const faceSize = new THREE.Vector3();
faceBox.getSize(faceSize);

// sunglassObject를 faceObject의 앞쪽에 배치
sunglassObject.scene.position.set(0, faceBox.max.y / 2, faceBox.max.z);

// faceObject에 sunglassObject를 추가
faceObject.scene.add(sunglassObject.scene);
```

이 코드는 Box3를 사용하여 객체의 크기와 위치를 계산하고, 이를 기반으로 sunglassObject를 faceObject의 앞쪽에 배치합니다. 이렇게 하면 수동으로 위치를 조정할 필요 없이 객체를 정확하게 배치할 수 있습니다.

# 무작위 배치

무작위로 객체를 생성하고 배치한 후, 그룹으로 묶어 마우스 이벤트가 있을 때 위에서 만든 얼굴 이모지 객체와 반대로 한번에 움직이게 구현하겠습니다.

```javascript
const createAndAddObjects = async (
  objectGroup: THREE.Group,
  faceObject: GLTF
) => {
  const objectNames = [
    "sparkle",
    "snowflake",
    "diamond",
    "cherry",
    "bulb",
    "swirl",
    "lightning",
    "turtle",
    "fish",
    "lamp",
    "idea_lamp",
  ];
  const faceBox = new THREE.Box3().setFromObject(faceObject.scene);

  for (const name of objectNames) {
    const obj = await createObject(name);
    objectGroup.add(replaceObject(obj, faceBox.max.x).scene);
  }
};
```

오브젝트 무작위 생성 및 배치 

```javascript
const replaceObject = (object: GLTF, standardSize: number): GLTF => {
  const objBox = new THREE.Box3().setFromObject(object.scene);
  object.scene.position.set(
    getRandomNumber(5, -8, 8),
    getRandomNumber(5, -8, 8),
    Math.floor(Math.random() * (7 + 10) - 10)
  );
  const objRatio = standardSize / objBox.max.x / 5;
  object.scene.scale.set(objRatio, objRatio, objRatio);
  return object;
};
```
씬과 카메라, 렌더러를 생성하고, 무작위 객체를 생성하고 배치하기 위해 createObject 함수를 사용합니다. 객체들을 그룹으로 묶어 objectGroup에 추가합니다. faceObject를 생성하고 씬에 추가합니다. 마우스 움직임에 따라 faceObject는 마우스 방향으로, objectGroup은 반대로 회전하도록 이벤트 리스너를 등록합니다. 이제 마우스를 움직일 때 faceObject와 objectGroup이 서로 반대로 회전하면서 움직이게 됩니다.

## 충돌 검사

아... 뭔가 아쉽죠? 

랜덤으로 객체를 배치하다 보면 얼굴 뒤로 숨어버리거나 얼굴 안으로 들어가는 경우가 많을 수 있습니다. 이를 방지하기 위해 객체들이 서로 겹치지 않도록 충돌 감지를 추가해야 합니다. 객체의 경계 상자를 계산하고, 새로운 객체가 기존 객체들과 겹치는지 확인하는 로직을 추가하면 됩니다.

다음은 faceObject와 객체 그룹을 생성하고 씬에 추가하는 코드입니다. 객체를 무작위로 생성하고 배치할 때, 새로운 객체가 faceObject 또는 기존 객체들과 겹치는지 확인합니다. 겹치는 경우, 객체의 위치를 다시 무작위로 설정하고 충돌 검사를 반복합니다. 모든 객체가 겹치지 않는 위치에 배치될 때까지 반복합니다.

```javascript
const initThree = async () => {
  //...
  window.addEventListener("mousemove", (event) =>
    onMouseMove(event, faceObject, objectGroup)
  );
  //...
};
const onMouseMove = (
  event: MouseEvent,
  faceObject: GLTF,
  objectGroup: THREE.Group
) => {
  const mouse = new THREE.Vector2();
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  faceObject.scene.rotation.x = mouse.y / 10;
  faceObject.scene.rotation.y = mouse.x / 10;

  objectGroup.rotation.x = -mouse.y / 10;
  objectGroup.rotation.y = -mouse.x / 10;
};
```
객체들이 faceObject와 겹치지 않게 무작위로 배치되고, 마우스를 움직일 때 faceObject와 objectGroup이 서로 반대로 회전하면서 움직입니다.

> 근데 무작위 랜덤으로 배치했더니 마음에 안들 때가 너무 많아서 어떻게 해결할까 하다가 제가 원하는 곳에 배치하는 게 제일 좋을 것 같아서 원하는 곳에 배치를 했습니다. 😅

# raycaster 마우스 감지

얼굴에 마우스를 올리면 선글라스가 스르륵 올라가는 애니메이션을 구현하고 싶어요!

onMouseMove 함수에서 마우스를 올렸을 때 그 포인터가 어디에 닿는지 감지를 해야 합니다. 2D로 생각하면 x, y 값 안에만 들어와도 찾아낼 수 있는데, z 좌표까지 추가되었으니까 아주 까다로워졌죠.

3D 공간에서 위치를 찾기 위해서는 이 두 가지가 필요합니다:
```javascript
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
```

raycaster를 사용하여 마우스 위치 감지

```javascript
const onMouseMove = (
  event: MouseEvent,
  faceObject: GLTF,
  objectGroup: THREE.Group,
  sunglassesObject: GLTF,
  camera: THREE.Camera
) => {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  faceObject.scene.rotation.x = mouse.y / 10;
  faceObject.scene.rotation.y = mouse.x / 10;

  objectGroup.rotation.x = -mouse.y / 10;
  objectGroup.rotation.y = -mouse.x / 10;

  // Raycaster 설정
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(faceObject.scene.children, true);

  if (intersects.length > 0) {
    // 얼굴에 마우스가 닿았을 때 선글라스를 올리는 애니메이션
    console.log('mouse on faceObject')
  } else {
    // 마우스가 얼굴에서 벗어났을 때 선글라스를 원래 위치로 되돌림
    console.log('mouse out faceObject')
  }
};

```

# 애니메이션 추가

마우스 감지는 잘 추가된 것 같습니다! 이제 애니메이션만 추가하면 되는데요, 기존에 사용하던 requestAnimationFrame을 사용하는 방법도 있지만, Three.js에서 지원하는 GSAP이라는 모듈도 있어서 두 가지 버전으로 구현해보겠습니다.

## requestAnimationFrame

```javascript
let isMouseOverFace = false;
let targetY = sunglassObject.scene.position.y;

const animate = () => {
    requestAnimationFrame(animate);
    controls.update();

    // 선글라스 위치를 부드럽게 업데이트
    sunglassObject.scene.position.y +=
        (targetY - sunglassObject.scene.position.y) * 0.1;

    renderer.render(scene, camera);
};

const onMouseMove = (
    //...
) => {
    //...
    // Raycaster 설정
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(faceObject.scene.children, true);

    targetY = intersects.length > 0 ? 5 : 0;
    // ...
};
```


## gsap 사용
먼저 gsap을 설치합니다.
```bash
npm i gsap
```
```javascript
const onMouseMove = (
    // ...

) => {
    // ...
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);

    const isOverFace = intersects.some((obj) => obj.object.userData.isFace);
    if (isOverFace) {
        gsap.to(sunglasses.scene.position, { y: 5, duration: 1 });
    } else if (!isOverFace) {
        gsap.to(sunglasses.scene.position, { y: 0, duration: 1 });
    }
    //...
};
```
# 리액트 API 사용

기존의 상태 관리 및 이벤트 핸들링 로직을 최신 리액트 API로 마이그레이션하여 최적화해보았습니다. useState, useRef, useEffect와 같은 React 훅을 사용하여 상태 관리와 DOM 조작을 개선하였습니다. 

```javascript
import React, { useEffect, useRef, useState, useCallback } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { GLTF, GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";

export default function ProfilePage() {
  const mountRef = useRef<HTMLDivElement>(null);
  const mouseOverFace = useRef<boolean>(false);

  const onMouseMove = useCallback(
    (
      event: MouseEvent,
      camera: THREE.Camera,
      scene: THREE.Scene,
      raycaster: THREE.Raycaster,
      mouse: THREE.Vector2,
      faceObject: GLTF,
      objectGroup: THREE.Group
    ) => {
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(scene.children, true);

      const isOverFace = intersects.some((obj) => obj.object.userData.isFace);
      mouseOverFace.current = isOverFace;

      faceObject.scene.rotation.x = mouse.y / 10;
      faceObject.scene.rotation.y = mouse.x / 10;

      objectGroup.rotation.x = -mouse.y / 10;
      objectGroup.rotation.y = -mouse.x / 10;
    },
    []
  );

  const initThree = useCallback(async (): Promise<() => void> => {
    const mount = mountRef.current;

    if (!mount) return () => {};

    const scene = createScene();
    const camera = createCamera();
    const renderer = createRenderer();
    mount.appendChild(renderer.domElement);

    const controls = setupControls(camera, renderer);
    setupLights(scene);

    const faceObject = await createObject("emoji");
    setupFaceObject(scene, faceObject);

    const sunglassObject = await createObject("sunglasses");
    setupSunglassObject(faceObject, sunglassObject);

    const objectGroup = new THREE.Group();
    scene.add(objectGroup);

    await createAndAddObjects(objectGroup, faceObject);

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const handleMouseMove = (event: MouseEvent) => {
      onMouseMove(
        event,
        camera,
        scene,
        raycaster,
        mouse,
        faceObject,
        objectGroup
      );
    };

    renderer.domElement.addEventListener("mousemove", handleMouseMove);

    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();

      const faceBox = new THREE.Box3().setFromObject(faceObject.scene);

      if (mouseOverFace.current) {
        const targetY = faceBox.max.y / 2 + 5;
        sunglassObject.scene.position.y +=
          (targetY - sunglassObject.scene.position.y) * 0.1;
      } else {
        const originalY = faceBox.max.y / 2;
        sunglassObject.scene.position.y +=
          (originalY - sunglassObject.scene.position.y) * 0.1;
      }

      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener("resize", handleResize);

    return () => {
      renderer.domElement.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("resize", handleResize);
      if (renderer.domElement.parentNode) {
        mount.removeChild(renderer.domElement);
      }
    };
  }, [onMouseMove]);

  useEffect(() => {
    const cleanupPromise: Promise<() => void> = initThree();

    return () => {
      cleanupPromise.then((cleanup) => {
        if (cleanup) cleanup();
      });
    };
  }, [initThree]);

  return <div ref={mountRef} />;
}

const createScene = (): THREE.Scene => {
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x000000);
  return scene;
};

const createCamera = (): THREE.PerspectiveCamera => {
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    1,
    10000
  );
  camera.position.set(0, 0, 25);
  return camera;
};

const createRenderer = (): THREE.WebGLRenderer => {
  const renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0x000000, 1); // Ensure the clear color is set
  return renderer;
};

const createObject = async (fileName: string): Promise<GLTF> => {
  const loader = new GLTFLoader();
  const url = `${process.env.PUBLIC_URL}/glb/${fileName}.glb`;
  const gltf = await loader.loadAsync(url);
  return gltf;
};

const setupFaceObject = (scene: THREE.Scene, faceObject: GLTF) => {
  faceObject.scene.position.set(0, -5, 0);
  faceObject.scene.traverse((child) => {
    if (child instanceof THREE.Mesh) {
      child.userData.isFace = true;
    }
  });
  scene.add(faceObject.scene);
};

const setupSunglassObject = (faceObject: GLTF, sunglassObject: GLTF) => {
  const faceBox = new THREE.Box3().setFromObject(faceObject.scene);
  sunglassObject.scene.position.set(0, faceBox.max.y / 2, faceBox.max.z);
  sunglassObject.scene.scale.set(8, 8, 8);
  faceObject.scene.add(sunglassObject.scene);
};

const createAndAddObjects = async (
  objectGroup: THREE.Group,
  faceObject: GLTF
) => {
  const objectNames = [
    { name: "sparkle", position: [3, 3, 7] },
    { name: "snowflake", position: [-3, 3, 7] },
    { name: "lamp", position: [5, 3, -2] },
    { name: "cherry", position: [-5, 3, -2] },
    { name: "bulb", position: [7, 0, 3] },
    { name: "swirl", position: [-8, 0, 3] },
    { name: "lightning", position: [8, -9, -4] },
    { name: "fish", position: [-6, -9, -4] },
    { name: "diamond", position: [3, -6, 6] },
    { name: "idea_lamp", position: [-3, -6, 6] },
  ];
  const faceBox = new THREE.Box3().setFromObject(faceObject.scene);

  for (const object of objectNames) {
    const obj = await createObject(object.name);
    objectGroup.add(replaceObject(obj, faceBox.max.x, object.position).scene);
  }
};

const replaceObject = (
  object: GLTF,
  standardSize: number,
  position: number[]
): GLTF => {
  const objBox = new THREE.Box3().setFromObject(object.scene);
  object.scene.position.set(position[0], position[1], position[2]);
  const objRatio = standardSize / objBox.max.x / 5;
  object.scene.scale.set(objRatio, objRatio, objRatio);
  return object;
};

const setupControls = (
  camera: THREE.PerspectiveCamera,
  renderer: THREE.WebGLRenderer
): OrbitControls => {
  const controls = new OrbitControls(camera, renderer.domElement);
  controls.target.set(0, 0, 0);
  controls.update();
  return controls;
};

const setupLights = (scene: THREE.Scene) => {
  const ambientLight = new THREE.AmbientLight(0xfefefe);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
  directionalLight.position.set(0, 1, 1).normalize();
  scene.add(directionalLight);
};

```
