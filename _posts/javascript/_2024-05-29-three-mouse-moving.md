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

# mouseover Event
마지막으로 얼굴에 마우스를 올리면 선글라스가 스르륵 올라가는 애니메이션을 구현하고 싶어요!

onMouseMove 함수에서 마우스를 올렸을 때 감지를 해야함

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();
3d 공간이기때문에 위치를 찾기가 힘들다 그래서 이거 두개가 필요함

raycaster.setFromCamera(mouse, camera);
let intersect = raycaster.intersectObjects(scene.children);
이렇게하면 레이저로 감지 가능
intersect.forEach((obj) => {
console.log(obj)
});
로 마우스에 닿는 물체가 어떤 건지 확인해볼 수 있음
근데 내가 불러온 얼굴, 선글라스 물체인지 알 수가 없음 각각 분리돼서 감지됨
const setupFaceObject = (scene: THREE.Scene, faceObject: GLTF) => {
faceObject.scene.position.set(0, -5, 0);
faceObject.scene.traverse((child) => {
if (child instanceof THREE.Mesh) {
child.userData.isFace = true; // sunglass를 face 그룹에 넣어두었기 때문에 이거 하나로 분별 가능!
}
});
scene.add(faceObject.scene);
};

mousemove 함수에 sunglasses: GLTF, 파라미터를 추가함

    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;

mouse.y = -(event.clientY / window.innerHeight) \* 2 + 1;
raycaster.setFromCamera(mouse, camera);
let intersect = raycaster.intersectObjects(scene.children);

intersect.forEach((obj) => {
if (obj.object.userData.isFace) {
obj.object.traverse((child) => {
console.log(child.userData);
sunglasses.scene.rotation.x += 1;
});
}
});

애니메이션을 구현해볼까? 너무 딱딱하고 마우스가 얼굴 안에서 움직일 때만 됨 ㅠ 아쉽다

# 애니메이션 추가

```javascript
  let isMouseOverFace = false;
  let targetY = sunglassObject.scene.position.y;

  renderer.domElement.addEventListener("mousemove", (event) =>
    onMouseMove(
      event,
      faceObject,
      sunglassObject,
      objectGroup,
      raycaster,
      mouse,
      camera,
      scene,
      isMouseOverFace,
      (overFace: boolean) => {
        isMouseOverFace = overFace;
        targetY = overFace ? 5 : 0;
      }
    )
  );


const animate = () => {
requestAnimationFrame(animate);
controls.update();

    // 선글라스 위치를 부드럽게 업데이트
    sunglassObject.scene.position.y +=
      (targetY - sunglassObject.scene.position.y) * 0.1;

    renderer.render(scene, camera);

};

const onMouseMove = (
event: MouseEvent,
faceObject: GLTF,
sunglasses: GLTF,
objectGroup: THREE.Group,
raycaster: THREE.Raycaster,
mouse: THREE.Vector2,
camera: THREE.Camera,
scene: THREE.Scene,
isMouseOverFace: boolean,
setMouseOverFace: (overFace: boolean) => void
) => {
mouse.x = (event.clientX / window.innerWidth) _ 2 - 1;
mouse.y = -(event.clientY / window.innerHeight) _ 2 + 1;
raycaster.setFromCamera(mouse, camera);
const intersects = raycaster.intersectObjects(scene.children, true);

const isOverFace = intersects.some((obj) => obj.object.userData.isFace);
if (isOverFace && !isMouseOverFace) {
setMouseOverFace(true);
} else if (!isOverFace && isMouseOverFace) {
setMouseOverFace(false);
}

faceObject.scene.rotation.x = mouse.y / 10;
faceObject.scene.rotation.y = mouse.x / 10;

objectGroup.rotation.x = -mouse.y / 10;
objectGroup.rotation.y = -mouse.x / 10;
};
```

가독성이 떨어지는 것 같고 어쩌고 react api 를 사용하여
useEffect로 초기화 및 정리 로직 관리
useRef로 DOM 요소 참조
useState로 상태 관리
useCallback으로 메모이제이션
useMemo로 메모이제이션된 값 생성
Custom Hooks로 반복적인 로직 추출

useState를 사용하여 isMouseOverFace와 sunglassesTargetY 상태를 관리합니다.
useThreeJS Custom Hook을 사용하여 Three.js 씬을 초기화하고 관리합니다.
onMouseMove 이벤트 핸들러는 마우스가 얼굴 위에 있을 때와 없을 때를 감지하고, 상태를 업데이트합니다.
animate 함수는 매 프레임마다 sunglassesTargetY 값을 참조하여 선글라스의 위치를 부드럽게 업데이트합니다.
이 접근 방식은 React의 상태 관리를 사용하여 코드의 가독성과 유지보수성을 높이며, Three.js와의 통합을 간단하고 효율적으로 처리할 수 있게 해줍니다.

# gsap 사용

npm i gsap

const onMouseMove = (
event: MouseEvent,
faceObject: GLTF,
sunglasses: GLTF,
objectGroup: THREE.Group,
raycaster: THREE.Raycaster,
mouse: THREE.Vector2,
camera: THREE.Camera,
scene: THREE.Scene,
isMouseOverFace: boolean,
setMouseOverFace: (overFace: boolean) => void
) => {
mouse.x = (event.clientX / window.innerWidth) _ 2 - 1;
mouse.y = -(event.clientY / window.innerHeight) _ 2 + 1;
raycaster.setFromCamera(mouse, camera);
const intersects = raycaster.intersectObjects(scene.children, true);

const isOverFace = intersects.some((obj) => obj.object.userData.isFace);
if (isOverFace && !isMouseOverFace) {
// 마우스가 얼굴 위로 들어왔을 때
gsap.to(sunglasses.scene.position, { y: 5, duration: 1 });
setMouseOverFace(true);
} else if (!isOverFace && isMouseOverFace) {
// 마우스가 얼굴 밖으로 나갔을 때
gsap.to(sunglasses.scene.position, { y: 0, duration: 1 });
setMouseOverFace(false);
}

faceObject.scene.rotation.x = mouse.y / 10;
faceObject.scene.rotation.y = mouse.x / 10;

objectGroup.rotation.x = -mouse.y / 10;
objectGroup.rotation.y = -mouse.x / 10;
};

# 갑분 리액트 공부

얼굴 오브젝트에 마우스 오버가 되면 썬글라스 되는 부분을 리액트로 만들어서 어쩌고

```javascript
const onMouseMove = useCallback(
  (
    event: MouseEvent,
    camera: THREE.Camera,
    scene: THREE.Scene,
    raycaster: THREE.Raycaster,
    mouse: THREE.Vector2,
    faceObject: GLTF,
    objectGroup: THREE.Group,
    sunglassObject: GLTF
  ) => {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(scene.children, true);

    const isOverFace = intersects.some((obj) => obj.object.userData.isFace);
    console.log(`isOverFace: ${isOverFace}`);

    // setMouseOverFace(isOverFace);

    faceObject.scene.rotation.x = mouse.y / 10;
    faceObject.scene.rotation.y = mouse.x / 10;

    objectGroup.rotation.x = -mouse.y / 10;
    objectGroup.rotation.y = -mouse.x / 10;
  },
  []
);
```

마우스를 올릴 떄마다 화면이 하얘지는 문제 발생

setMouseOverFace를 주석 처리하면 문제가 해결되는 것으로 보아, 상태 업데이트로 인해 리렌더링이 발생하면서 Three.js 렌더링 로직에 문제가 생기는 것 같습니다. 상태 업데이트와 렌더링 간의 충돌을 방지하기 위해서는 상태 업데이트를 비동기적으로 처리하거나 상태 업데이트 빈도를 줄이는 방법이 필요합니다.

다음은 상태 업데이트를 비동기적으로 처리하고, 상태 업데이트가 과도하게 발생하지 않도록 최적화한 코드입니다:
