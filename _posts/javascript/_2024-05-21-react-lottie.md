---
layout: post
title: fabric.js 에서 lottie 사용하기
summary: 
date: 2024-05-21 16:46:52 +09:00
categories: javascript
tags: react refactoring migration
---

# lottie
lottie는 airbnb에서 만든 애니메이션. gif 뭐 어쩌고 보다 엄청 가볍다.

# lottie 사용하기

# Fabric.js
Fabric.js는 강력하고 심플한 자바스크립트 HTML5 캔버스 라이브러리입니다.

# migration & refactoring

vue로 만들었던 프로젝트였는데 react로 변경해야될 일이 있어서 마이그레이션과함께 코드 리팩토링을 진행해보겠습니다.

먼저 기존 소스
vue
```javascript

onBeforeMount(async () => {
   await initGround();
   await drawItems();
})
const initGround = async () => {
if (ground.value) return;
let w = 1262;
let h = 454;
ground.value = await new fabric.Canvas("ground");
let maxScale = 1.5;
let minScale = 0.5;
ground.value.on("object:moving", (e) => {
    maxScale = 1.5;
    let obj = e.target;
    obj.catgryId == "JC-23012602050000000"
    ? (maxScale = 2)
    : (maxScale = 1.5);
    let halfw = (obj.width * obj.scaleX) / 2;
    let halfh = (obj.height * obj.scaleX) / 2;
    let limit_l = obj.canvas.width - obj.width * obj.scaleX;
    let limit_b = obj.canvas.height - obj.height * obj.scaleX;
    let bounds = {
    tl: { x: halfw, y: halfh },
    br: { x: obj.canvas.width, y: obj.canvas.height },
    };
    if (obj.top < bounds.tl.y || obj.left < bounds.tl.x) {
    obj.top = Math.max(obj.top, 0);
    obj.left = Math.max(obj.left, 0);
    }
    if (
    obj.top + obj.height * obj.scaleX > bounds.br.y ||
    obj.left + obj.width * obj.scaleX > bounds.br.x
    ) {
    obj.top = Math.min(obj.top, limit_b);
    obj.left = Math.min(obj.left, limit_l);
    }
});

ground.value.on("object:scaling", (e) => {
    let obj = e.target;
    obj.catgryId == "JC-23012602050000000"
    ? (maxScale = 2)
    : (maxScale = 1.5);
    if (obj.scaleX > maxScale) {
    obj.scaleX = maxScale;
    obj.left = obj.lastGoodLeft;
    obj.top = obj.lastGoodTop;
    }
    if (obj.scaleY > maxScale) {
    obj.scaleY = maxScale;
    obj.left = obj.lastGoodLeft;
    obj.top = obj.lastGoodTop;
    }
    if (obj.scaleX < minScale) {
    obj.scaleX = minScale;
    obj.left = obj.lastGoodLeft;
    obj.top = obj.lastGoodTop;
    }
    if (obj.scaleY < minScale) {
    obj.scaleY = minScale;
    obj.left = obj.lastGoodLeft;
    obj.top = obj.lastGoodTop;
    }
    let halfw = (obj.width * obj.scaleX) / 2;
    let halfh = (obj.height * obj.scaleX) / 2;
    let bounds = {
    tl: { x: halfw, y: halfh },
    br: { x: obj.canvas.width, y: obj.canvas.height },
    };

    if (
    obj.top + obj.height * obj.scaleX > bounds.br.y ||
    obj.left + obj.width * obj.scaleX > bounds.br.x
    ) {
    e.target.scaleX = e.transform.scaleX;
    e.target.scaleY = e.transform.scaleY;
    }
    e.target.lastGoodTop = e.target.top;
    e.target.lastGoodLeft = e.target.left;
});
// canvas 선택 block
ground.value.uniformScaling = true;
ground.value.selection = false;
ground.value.setHeight(h);
ground.value.setWidth(w);
};
const addCanvasObj = async (obj, catgryId) => {
  console.log(obj, 'addCanvasObj')

  const activeObject = ground.value.getActiveObject()
  if (activeObject) return
  putItem.value = true
  const { x, y } = obj
  const jitemFilePath = reward.returnItem(catgryId, obj.jitemId).jitemFilePath
  if (!jitemFilePath) {
    reward.isActive = false
    return
  }
  if (jitemFilePath?.indexOf('png') > 0) {
    fabric.Image.fromURL(
      jitemFilePath,
      (img) => {
        const target = settingObj(obj, img, catgryId)
        if (!obj.scale && obj.catgryId == 'JC-23012602050000000') {
          target.set('scaleY', 1.5)
          target.set('scaleX', 1.5)
        }
        ground.value.add(target)
        x == undefined &&
          selectObj(obj.jitemId, target.o_idx, target.catgryId, 'add')
      },
      {
        crossOrigin: window.location.host
      }
    )
    return true
  }
  if (jitemFilePath?.indexOf('json') > 0) {
    const canvas = document.createElement('canvas')
    const { data } = await axios.get(jitemFilePath)
    canvas.width = data.w
    canvas.height = data.h
    const animItem = lottie.loadAnimation({
      renderer: 'canvas',
      loop: reward.returnItem(obj.catgryId, obj.jitemId).jitemTp == 'T' ? 0 : 1,
      autoplay: false,
      animationData: data,
      rendererSettings: {
        context: canvas.getContext('2d'),
        preserveAspectRatio: 'xMidYMid meet'
      },
      audioFactory: createAudio
    })
    animItem.addEventListener('enterFrame', () => {
      ground.value.requestRenderAll()
    })
    animItem.addEventListener('complete', () => {
      lottieComplete(animItem)
    })
    if (obj.jitemId == 'JI-23012603490000000') animItem.setSpeed(0.6)

    animItem.goToAndStop(0, true)
    animItem.addEventListener(
      'DOMLoaded',
      () => {
        const ane = new fabric.Lottie(
          canvas,
          {
            objectCaching: true
          },
          animItem
        )
        const target = settingObj(obj, ane, catgryId)
        if (!obj.scale && obj.catgryId == 'JC-23012602050000000') {
          target.set('scaleY', 1.5)
          target.set('scaleX', 1.5)
        }
        ground.value.add(target)
        ground.value.renderAll()
        x == undefined &&
          selectObj(obj.jitemId, target.o_idx, target.catgryId, 'add')
      },
      {
        crossOrigin: window.location.host
      }
    )
  }
}
const drawItems = async () => {
console.log(reward.objList, "drawItems1");
if (!reward.objList) return;
console.log(reward.objList, "drawItems2");
for await (const obj of reward.objList) {
    console.log(obj, "obj draw start");

    const cnt = await updateCnt(obj.jitemId, obj.catgryId, "minus");
    console.log(cnt);
    if (cnt >= 0) {
    await addCanvasObj(obj, obj.catgryId);
    } else {
    reward.objList = reward.objList.filter((e) => e.o_idx !== obj.o_idx);
    }
}
};
const addCanvasObj = async (obj, catgryId) => {
console.log(obj, "addCanvasObj");

const activeObject = ground.value.getActiveObject();
if (activeObject) return;
putItem.value = true;
const { x, y } = obj;
const jitemFilePath = reward.returnItem(
    catgryId,
    obj.jitemId
).jitemFilePath;
if (!jitemFilePath) {
    reward.isActive = false;
    return;
}
if (jitemFilePath?.indexOf("png") > 0) {
    fabric.Image.fromURL(
    jitemFilePath,
    (img) => {
        const target = settingObj(obj, img, catgryId);
        if (!obj.scale && obj.catgryId == "JC-23012602050000000") {
        target.set("scaleY", 1.5);
        target.set("scaleX", 1.5);
        }
        ground.value.add(target);
        x == undefined &&
        selectObj(obj.jitemId, target.o_idx, target.catgryId, "add");
    },
    {
        crossOrigin: window.location.host,
    }
    );
    return true;
}
if (jitemFilePath?.indexOf("json") > 0) {
    const canvas = document.createElement("canvas");
    const { data } = await axios.get(jitemFilePath);
    canvas.width = data.w;
    canvas.height = data.h;
    const animItem = lottie.loadAnimation({
    renderer: "canvas",
    loop:
        reward.returnItem(obj.catgryId, obj.jitemId).jitemTp == "T" ? 0 : 1,
    autoplay: false,
    animationData: data,
    rendererSettings: {
        context: canvas.getContext("2d"),
        preserveAspectRatio: "xMidYMid meet",
    },
    audioFactory: createAudio,
    });
    animItem.addEventListener("enterFrame", () => {
    ground.value.requestRenderAll();
    });
    animItem.addEventListener("complete", () => {
    lottieComplete(animItem);
    });
    if (obj.jitemId == "JI-23012603490000000") animItem.setSpeed(0.6);

    animItem.goToAndStop(0, true);
    animItem.addEventListener(
    "DOMLoaded",
    () => {
        const ane = new fabric.Lottie(
        canvas,
        {
            objectCaching: true,
        },
        animItem
        );
        const target = settingObj(obj, ane, catgryId);
        if (!obj.scale && obj.catgryId == "JC-23012602050000000") {
        target.set("scaleY", 1.5);
        target.set("scaleX", 1.5);
        }
        ground.value.add(target);
        ground.value.renderAll();
        x == undefined &&
        selectObj(obj.jitemId, target.o_idx, target.catgryId, "add");
    },
    {
        crossOrigin: window.location.host,
    }
    );
}
};
```

fabric.js
```javascript
import { fabric } from 'fabric'
import imgBR from '../assets/img/btn/resize.png'
import imgB from './arrow-b.png'
import imgL from './arrow-l.png'
import imgR from './arrow-r.png'
import imgT from './arrow-t.png'
fabric.Lottie = fabric.util.createClass(fabric.Image, {
  type: 'croppableimage',
  initialize: function (LottieCanvas, options, lottieItem) {
    options = options || {}
    this.callSuper('initialize', LottieCanvas, options)
    this.LottieCanvas = LottieCanvas
    this.lottieItem = lottieItem
  },
  drawCacheOnCanvas: function (ctx) {
    ctx.drawImage(this.LottieCanvas, -this.width / 2, -this.height / 2)
  },
  _createCacheCanvas: function () {
    this._cacheProperties = {}
    this._cacheCanvas = this.LottieCanvas
    console.log(this._cacheCanvas)
    this._cacheContext = this._cacheCanvas.getContext('2d')
    this.dirty = true
  },
  play: function () {
    this.lottieItem.goToAndStop(0, true)
    this.lottieItem.play()
  },
  render: function (ctx) {
    if (this.isNotVisible()) {
      return
    }
    if (
      this.canvas &&
      this.canvas.skipOffscreen &&
      !this.group &&
      !this.isOnScreen()
    ) {
      return
    }
    ctx.save()
    this._setupCompositeOperation(ctx)
    this.drawSelectionBackground(ctx)
    this.transform(ctx)
    this._setOpacity(ctx)
    this._setShadow(ctx, this)
    if (this.transformMatrix) {
      // eslint-disable-next-line prefer-spread
      ctx.transform.apply(ctx, this.transformMatrix)
    }
    this.clipTo && fabric.util.clipContext(this, ctx)

    if (this.shouldCache()) {
      if (!this._cacheCanvas) {
        console.log('create cache')
        this._createCacheCanvas()
      }
      this.drawCacheOnCanvas(ctx)
    } else {
      console.log('remove cache and draw : ')
      this._removeCacheCanvas()
      this.dirty = false
      this.drawObject(ctx)
      if (this.objectCaching && this.statefullCache) {
        this.saveState({ propertySet: 'cacheProperties' })
      }
    }
    this.clipTo && ctx.restore()
    ctx.restore()
  },
  _findTargetCorner: function (pointer, forTouch) {
    // objects in group, anykind, are not self modificable,
    // must not return an hovered corner.

    const ex = pointer.x,
      ey = pointer.y,
      keys = Object.keys(this.oCoords)
    let xPoints,
      lines,
      j = keys.length - 1,
      i
    this.__corner = 0

    // cycle in reverse order so we pick first the one on top
    for (; j >= 0; j--) {
      i = keys[j]
      if (!this.isControlVisible(i)) {
        continue
      }

      lines = this._getImageLines(
        forTouch ? this.oCoords[i].touchCorner : this.oCoords[i].corner
      )
      xPoints = this._findCrossPoints({ x: ex, y: ey }, lines)
      if (xPoints !== 0 && xPoints % 2 === 1) {
        this.__corner = i
        return i
      }
    }
    return false
  }
})
fabric.Object.prototype._findTargetCorner = function (pointer, forTouch) {
  const ex = pointer.x,
    ey = pointer.y,
    keys = Object.keys(this.oCoords)
  let xPoints,
    lines,
    j = keys.length - 1,
    i
  this.__corner = 0
  for (; j >= 0; j--) {
    i = keys[j]
    if (!this.isControlVisible(i)) {
      continue
    }

    lines = this._getImageLines(
      forTouch ? this.oCoords[i].touchCorner : this.oCoords[i].corner
    )
    xPoints = this._findCrossPoints({ x: ex, y: ey }, lines)
    if (xPoints !== 0 && xPoints % 2 === 1) {
      this.__corner = i
      return i
    }
  }
  return false
}
fabric.Object.prototype.set({
  borderColor: '#1e678000'
})
//////////////////////////
////////// icon //////////
// const rotateIcon = imgfile
const imgsR = document.createElement('img')
const imgsT = document.createElement('img')
const imgsL = document.createElement('img')
const imgsB = document.createElement('img')
const imgsBR = document.createElement('img')
imgsR.src = imgR
imgsT.src = imgT
imgsL.src = imgL
imgsB.src = imgB
imgsBR.src = imgBR
fabric.Object.prototype.controls.mr = new fabric.Control({
  x: 0.5,
  y: 0,
  render: function renderIconsR(ctx, left, top, styleOverride, fabricObject) {
    const size = this.cornerSize
    ctx.save()
    ctx.translate(left, top)
    ctx.drawImage(imgsR, -size / 2, -size / 2, size, size)
    ctx.restore()
  },
  cornerSize: 28
})
fabric.Object.prototype.controls.mt = new fabric.Control({
  x: 0,
  y: -0.5,
  render: function renderIconsT(ctx, left, top, styleOverride, fabricObject) {
    const size = this.cornerSize
    ctx.save()
    ctx.translate(left, top)
    ctx.drawImage(imgsT, -size / 2, -size / 2, size, size)
    ctx.restore()
  },
  cornerSize: 28
})
fabric.Object.prototype.controls.ml = new fabric.Control({
  x: -0.5,
  y: 0,
  render: function renderIconsL(ctx, left, top, styleOverride, fabricObject) {
    const size = this.cornerSize
    ctx.save()
    ctx.translate(left, top)
    ctx.drawImage(imgsL, -size / 2, -size / 2, size, size)
    ctx.restore()
  },
  cornerSize: 28
})
fabric.Object.prototype.controls.mb = new fabric.Control({
  x: 0,
  y: 0.5,
  render: function renderIconsB(ctx, left, top, styleOverride, fabricObject) {
    const size = this.cornerSize
    ctx.save()
    ctx.translate(left, top)
    ctx.drawImage(imgsB, -size / 2, -size / 2, size, size)
    ctx.restore()
  },
  cornerSize: 28
})
fabric.Object.prototype.controls.br = new fabric.Control({
  x: 0.5,
  y: 0.5,
  actionHandler: fabric.controlsUtils.scalingEqually,
  actionName: 'scale',
  render: function renderIconsBR(ctx, left, top, styleOverride, fabricObject) {
    const size = this.cornerSize
    ctx.save()
    ctx.translate(left, top)
    ctx.drawImage(imgsBR, -size / 2, -size / 2, size, size)
    ctx.restore()
  },
  cornerSize: 28
})

export default fabric

```

console.log, 주석 날것 그대로 가져왔는데 이렇게 보니 좀 부끄럽습니다. 2년 전의 코드를 본다는 것이..

## initCanvas
```javascript
export default function LottieGround({}) {
  const [canvas, setCanvas] = useState<fabric.Canvas | null>();
  const initCanvas = async () => {
    let w = 1262;
    let h = 454;
    const newCanvas = await new fabric.Canvas("canvas");
    newCanvas.setHeight(h);
    newCanvas.setWidth(w);
    setCanvas(newCanvas);
    return () => {
      newCanvas.dispose();
    };
  };
  useEffect(() => {
    initCanvas();
  }, []);
  return (
    <>
      <canvas id="canvas"></canvas>
    </>
  );
}
```
캔버스 초기화가 중요!!! 
return 에서 Dispose 해줌