---
layout: post
title:  three.js 마우스 무빙
summary: StereoCamera 사용해서 사용자 인터렉션 마우스 따라 이벤트 구현하기
date: 2024-05-29 10:29:17 +09:00
categories: javascript
tags:  threejs interactive javascript
---

three.js 세번째 작성 글입니다.

마우스 움직임에 따라 변화가 있는 웹을 접속해본 적이 있으신가요? 단순히 마우스 커서를 따라다니는 이벤트가 아니라, 마우스를 계속 쳐다보는 고양이라든지, 마우스 반대로 도망가는 오브젝트가 있다든지 하는 웹을 만난 적이 있으실 거예요. 저는 그런 기능이 구현된 사이트에 접속하면 단순하지만 재미있고 신기해서 머무는 시간이 길어지는 것을 느꼈습니다. 그래서 한번 구현해보고 싶어졌습니다. 오늘은 이 기능에 대해 알아보고 직접 구현해볼게요!

시작하기 전에 예시를 

https://threejs.org/examples/#webgl_effects_anaglyph


오브젝트에 오브젝트를 고정시키고 싶다!
위 코드에서는 sunglassObject를 faceObject의 자식으로 추가하여, faceObject가 회전하거나 이동할 때 sunglassObject도 함께 움직이도록 하였습니다. sunglassObject.scene.position.set(0.5, 0, 0.5);로 sunglassObject의 위치를 조정하여 faceObject의 한쪽 벽면에 고정시켰습니다.
```javascript   
 faceObject.scene.add(sunglassObject.scene);
```
이제 faceObject가 마우스 움직임에 따라 회전할 때 sunglassObject도 함께 회전하게 됩니다.

아... 좌표 잡기가 너무 힘들다

모델의 정확한 위치를 맞추는 것은 수동으로 조정하는 것보다 더 효율적으로 할 수 있습니다. 여기서는 모델의 크기와 위치를 계산하여 적절한 위치에 배치하는 방법을 살펴보겠습니다.

Three.js에서는 객체의 크기와 경계를 계산하기 위해 THREE.Box3를 사용할 수 있습니다. 이를 사용하면 모델의 경계 상자를 계산하여 정확한 위치를 지정할 수 있습니다.

다음은 Box3를 사용하여 sunglassObject를 faceObject의 표면에 정확히 배치하는 예제입니다:

이 코드는 Box3를 사용하여 객체의 크기와 위치를 계산하고, 이를 기반으로 sunglassObject를 faceObject의 앞쪽에 배치합니다. 이렇게 하면 수동으로 위치를 조정할 필요 없이 객체를 정확하게 배치할 수 있습니다.

```javascript
// 경계 상자 계산
const faceBox = new THREE.Box3().setFromObject(faceObject.scene);

// faceObject의 크기 계산
const faceSize = new THREE.Vector3();
faceBox.getSize(faceSize);

console.log(faceBox.max.x, faceBox.max.y, faceBox.max.z);

// sunglassObject를 faceObject의 앞쪽에 배치
sunglassObject.scene.position.set(0, faceBox.max.y / 2, faceBox.max.z);

faceObject.scene.add(sunglassObject.scene);
```
무작위로 object를 생성하고 배치하고 싶은데 이건 마우스를 올릴 때 묶음처럼 한번에 움직이게 할거야. 얼굴이랑 반대로

무작위로 객체를 생성하고 배치하는 방법은 Three.js의 여러 기능을 활용하여 간단하게 구현할 수 있습니다. 다음은 무작위로 생성된 객체들을 그룹으로 묶어 얼굴과 반대로 움직이도록 하는 방법입니다.

    TODO: 랜덤 오브젝트 생성
```javascript
// 객체 그룹 생성
const objectGroup = new THREE.Group();
scene.add(objectGroup);

// 무작위 객체 생성 및 배치
for (let i = 0; i < 10; i++) {
    // const obj = await createObject("lightning");
    const obj = await createObject("sparkle");
    obj.scene.position.set(
    Math.random() * 10 - 5,
    Math.random() * 10 - 5,
    Math.random() * 10 - 5
    );
    // obj.scene.rotateX(90);
    obj.scene.scale.set(10, 10, 10);
    objectGroup.add(obj.scene);
}
```
이 코드는 다음과 같이 동작합니다:

씬과 카메라, 렌더러를 생성합니다.
무작위 객체를 생성하고 배치하기 위해 createObject 함수를 사용합니다.
객체들을 그룹으로 묶어 objectGroup에 추가합니다.
faceObject를 생성하고 씬에 추가합니다.
마우스 움직임에 따라 faceObject는 마우스 방향으로, objectGroup은 반대로 회전하도록 이벤트 리스너를 등록합니다.
이제 마우스를 움직일 때 faceObject와 objectGroup이 서로 반대로 회전하면서 움직이게 됩니다.

TODO:랜덤을 faceObject랑 겹치지 않게 하고 싶은데
랜덤으로 배치된 객체들이 faceObject와 겹치지 않게 하기 위해서는 객체들이 서로 겹치지 않도록 충돌 감지를 추가해야 합니다. 이를 위해서 객체의 경계 상자를 계산하고, 새로운 객체가 기존 객체들과 겹치는지 확인하는 로직을 추가하면 됩니다.

다음은 객체가 서로 겹치지 않도록 하는 업데이트된 코드입니다:

faceObject와 객체 그룹을 생성하고 씬에 추가합니다.
객체를 무작위로 생성하고 배치할 때, 새로운 객체가 faceObject 또는 기존 객체들과 겹치는지 확인합니다.
겹치는 경우, 객체의 위치를 다시 무작위로 설정하고 충돌 검사를 반복합니다.
모든 객체가 겹치지 않는 위치에 배치

intersectsBox 메서드는 Three.js에서 두 개의 경계 상자(Axis-Aligned Bounding Boxes, AABB)가 서로 교차(겹치는)하는지 여부를 검사하는 함수입니다. 이 메서드는 주로 객체 간의 충돌 감지에 사용됩니다. 객체들이 공간 내에서 겹치지 않도록 배치할 때 매우 유용합니다.
 
이런 기능도 있지만 랜덤을 뽑을 때부터 얼굴 보다 멀리로 뽑기