---
layout: post
title: 리팩토링은 어떻게 해야될까?
summary: 리팩토링의 방법들 🔨
date: 2024-05-15 10:56:12 +09:00
categories: etc
tags: refactoring
---
[리팩토링과 클린코드]({{base_path}}/etc/code-refactoring/) 이어서 작성한 글입니다.

리팩토링을 시작하기에 앞서 계속 강조했던 부분만 다시 짚어보겠습니다. 

> 새로운 기능 추가 없이! 기존 기능은 오류 없이!

저는 리팩토링을 하기 전에는 테스트코드를 먼저 생성해두거나 테스트케이스를 작성을 해둔 후 진행하는 것이 바람직하다고 생각합니다. 

다양한 리팩토링의 기법중, 메소드와 조건문기반으로 리팩토링을 알아보겠습니다. 💪

# 메소드 정리
__Composing Methods__

리팩토링을 할 때 가장 큰 부분은 메소드들을 다듬고 정리하는 것입니다. 간결하고 명시적으로, 기능별로 작성된 메소드 들은 가독성을 많이 높여줍니다. 메소드를 정리하는 방법들은 어떤 것들이 있을까요?

## Extract Method
메소드가 길어지고 복잡해질 수록 어떤 기능을 가진 메소드인지 파악하기가 어렵습니다. 기존 메소드를 <span class="h-yellow">기능 단위로 추출</span>한 후 알맞는 이름을 지어줍니다. 메소드가 잘 쪼개져 있을 수록 다른 메소드에서 사용되기 쉽습니다. 그래서 메소드는 최대한 하나의 리턴값을 갖도록 쪼개줍니다. Extract Method 기법을 통해 더 읽기 쉽고, 중복이 적고, 오류 발생을 줄일 수 있습니다.

```javascript
// ASIS
printInfo() {
  printPrice();

  // Print Orders.
  console.log("name: " + name);
  console.log("orders: " + getOrders());
}

// TOBE
printInfo() {
  printPrice();
  printOrders(getOrders());
}

printOrders(orders: number) {
  console.log("name: " + name);
  console.log("orders: " + orders);
}
```

## Extract Variable
변수를 추출합니다. Extract Method를 하기 위해 먼저 진행해야하는 단계가 될 수도 있습니다. if() 문이나 ?: operator를 사용할때, for() 문을 사용할 때 등 임시 변수를 사용합니다. 이때 변수명을 지을 때는 메소드의 목적으로 이름을 만들어 줍니다. 아무리 변수를 쪼개놓고 임시 변수를 사용한다고 해도 a, b 같은 이름을 사용한다면 더욱 복잡해지겠죠?

❗️여기서 주의 <br>
__Introduce Explaining Variable__<br>
복잡한 수식을 사용하는 경우에는 메소드의 목적으로 된 이름을 사용합니다.

```javascript
// ASIS
if ((platform.toUpperCase().indexOf("MAC") > -1) &&
      (browser.toUpperCase().indexOf("IE") > -1) &&
      wasInitialized() && resize > 0 )
{
}
// TOBE
const isMasOS = platform.toUpperCase().indexOf("MAC") > -1;
const isIEBrowser = browser.toUpperCase().indexOf("IE") > -1;
const wasResized = 0;

if( isMacOS && isIEBrowser && wasInitialized() && wasResized )
{
}
```

## Inline Methods
불필요한 메소드를 최소화합니다. 메소드가 메소드 그 자체의 역할을 한다면 과감하게 삭제를 해줍니다.

__Inline Temp__<br>
메소드뿐만아니라 변수를 사용하는 경우에도 마찬가지입니다.

```javascript
// ASIS
getRating(){
  return moreThanFiveOrders() ? 2 : 1;
}
moreThanFiveOrders(){
  return orders > 5;
}
hasDiscount(order) {
  let basePrice: number = order.basePrice();
  return basePrice > 1000;
}
// TOBE
getRating(){
  return orders > 5 ? 2 : 1;
}
hasDiscount(order) {
  return order.basePrice() > 1000;
}
```

## Replace Temp with Query
계산식을 따로 정리를 합니다. Temp(임시변수)를 Query로 대체하면 코드를 별도의 메소드로 추출하는 데 방해가 되는 지역 변수를 제거할 수 있습니다. 즉, 임시 변수를 의미있는 메소드 호출로 바꿔서 코드 중복을 줄이고 가독성을 높일 수 있습니다.

```javascript
// ASIS
calculateTotal(): number {
  let basePrice = quantity * itemPrice;
  if (basePrice > 1000) {
    return basePrice * 0.95;
  }
  else {
    return basePrice * 0.98;
  }
}
//  TOBE
calculateTotal(): number {
  if (basePrice() > 1000) {
    return basePrice() * 0.95;
  }
  else {
    return basePrice() * 0.98;
  }
}
basePrice(): number {
  return quantity * itemPrice;
}
```


## Split Temporary Variable
임시변수에 여러가지 값을 대입하는 경우에는 임시변수를 더 생성해 추출해내는 것입니다. 이부분은 정말 중요하다고 생각이드는데요. 변수 하나를 선언 해 그 변수에 값을 넣었다 뺐다 바꿨다 하다보면 말그대로 스파게티 🍝 코드 완성이라고 생각합니다. 아무리 임시변수여도 어떤 값을 가진 변수인지 한눈에 알아보기 쉬우면 좋겠죠! 저는 값이 변하는 변수 이외에는 const 선언을 자주 사용해서 이런 일이 없지만, 하나의 변수에 값을 계속 바꿔 코드를 작성하는 것은 오류를 만나는 지름길인 것 같습니다. 처음 작성부터 사용하지 않고 리팩토링할 일이 없는 게 베스트인 것 같네요...
```javascript
// ASIS
let temp = 2 * (height + width);
console.log(temp);
temp = height * width;
console.log(temp);
// TOBE
const perimeter = 2 * (height + width);
console.log(perimeter);
const area = height * width;
console.log(area);
```
이와 비슷하게 주의해야할 점도 있습니다. <br>
__Remove Assignments to Parameters__ <br>
파라미터로 전달 된 값은 새로운 값에 할당하여 사용하는 것입니다. 파라미터의 값을 바로 변경하면 호출을 요청한 곳에서도 영향을 끼칠 위험이 있습니다. 당연한 부분이었지만 항상 조심하고 주의를 기울여야할 부분입니다.

```info
프로그램의 각 요소는 한 가지만 담당해야 합니다.
이렇게 하면 부작용 없이 코드를 안전하게 교체할 수 있어 코드 유지 관리가 훨씬 쉬워집니다.
```

<!-- ## Replace Method with Method Object
긴 메소드가 있는데 지역변수로 인해 Extract Method가 어려운 경우, 메소드를 자신을 위한 객체로 바꿔서 모든 지역변수가 그 객체의 필드가 되도록 만듭니다. 이렇게 하면 메소드를 같은 객체 안의 여러 메소드로 분해할 수 있습니다.

```javascript
// ASIS
class Order {
  // ...
  price(): number {
    let primaryBasePrice;
    let secondaryBasePrice;
    let tertiaryBasePrice;
    // Perform long computation.
  }
}

// TOBE
class Order {
  // ...
  price(): number {
    return new PriceCalculator(this).compute();
  }
}

class PriceCalculator {
  private _primaryBasePrice: number;
  private _secondaryBasePrice: number;
  private _tertiaryBasePrice: number;
  
  constructor(order: Order) {
    // Copy relevant information from the
    // order object.
  }
  
  compute(): number {
    // Perform long computation.
  }
}
``` -->

## Substitute Algorithm
알고리즘을 더 간단하고 쉬운 방법으로 바꿔줍니다. 어떤 기능을 수행하거나, 어떤 값을 찾아야하는 일을 할 땐 다양한 방법들이 있습니다. 그중에서 가장 쉽고 간단명료한 방법으로 바꿔줍니다. 이때 미리 메소드를 분리해두었다면 더욱 간단합니다! 복잡하고 큰 알고리즘을 변경하는 것보다 간단하고 작은 알고리즘을 변경하는 것이 더 쉽습니다. 당연히 변경한 알고리즘은 변경 전의 알고리즘과 값이 같아야겠죠?
```javascript
// ASIS
foundPerson(people: string[]): string{
  for (let person of people) {
    if (person.equals("Don")){
      return "Don";
    }
    if (person.equals("John")){
      return "John";
    }
    if (person.equals("Kent")){
      return "Kent";
    }
  }
  return "";
}
// TOBE
foundPerson(people: string[]): string{
  let candidates = ["Don", "John", "Kent"];
  for (let person of people) {
    if (candidates.includes(person)) {
      return person;
    }
  }
  return "";
}
```


<!-- # Moving Features between Objects
__개체 간 기능 이동__

거대한 산을 하나 넘었습니다. 하지만 이제 시작에요. 집중해서 공부를 해봅시다! 올바르게 메소드를 작성을 했는지, 동작을 필요한 메소드에 정확히 작성을 했는지 확인합니다.
## Move Method
## Move Field 
# 데이터 구성 -->
# 조건문 단순화
__Simplifying Conditional Expressions__

코드로 가장 간단하고 빠르게 구현을 하기위해, 또는 요구사항이 점점 늘어남에따라서 조건문이 점점 늘어나고 복잡해지기마련입니다... 조건문이 길고 복잡하면 코드를 알아보기가 정말 힘들어요. 이 문제를 해결하기 위한 많은 기술들이 있습니다.

## Decompose Conditional
복잡한 조건문을 별도의 메소드로 분리해 조건부를 간단하게 작성하는 것입니다. 함수를 분석할 때 조건문으로 가득 찬 경우가 정말 함수를 이해하기가 어렵습니다. 코드가 길어진다면 앞에 정의해둔 조건도 기억이 나지 않을 떄도 있습니다. 조건부 코드를 메서드로 추출하여 조건을 알아볼 수 있도록 이름을 지정해서 조건부 코드를 리팩토링 합니다.

```javascript
// ASIS
if (date.before(SUMMER_START) || date.after(SUMMER_END)) {
  charge = quantity * winterRate + winterServiceCharge;
}
else {
  charge = quantity * summerRate;
}
// TOBE
if (isSummer(date)) {
  charge = summerCharge(quantity);
}
else {
  charge = winterCharge(quantity);
}
```

## Consolidate Conditional Expression
불필요한 조건문을 줄입니다. 메소드 내에서 동일한 판단을 하고 있는 조건문이 나열되고 있다면 조건을 메소드로 만들어 단일 표현식으로 합쳐줍니다. 이렇게 조건을 메소드로 만들어두면 똑같은 조건을 검사해야되는 곳에서 코드 중복도 줄일 수 있습니다.
```javascript
// ASIS
disabilityAmount(): number {
  if (seniority < 2) {
    return 0;
  }
  if (monthsDisabled > 12) {
    return 0;
  }
  if (isPartTime) {
    return 0;
  }
  // Compute the disability amount.
  // ...
}
//TOBE
disabilityAmount(): number {
  if (isNotEligibleForDisability()) {
    return 0;
  }
  // Compute the disability amount.
  // ...
}
```

## Consolidate Conditional Expression
조건식 안에서 중복되어 표현되는 코드를 조건식 밖으로 빼줍니다. if문을 이해하고 있다면 if에 걸리든, else에 걸리든 조건식 밖에 있는 코드도 실행된다는 것은 알고있을 겁니다. 이렇게 모든 조건에서 실행되는 코드는 조건문 밖으로 빼서 코드의 중복을 줄입니다.
```javascript
// ASIS
if (isSpecialDeal()) {
  total = price * 0.95;
  send();
}
else {
  total = price * 0.98;
  send();
}
//TOBE
if (isSpecialDeal()) {
  total = price * 0.95;
}
else {
  total = price * 0.98;
}
send();
```

## Remove Control Flag
제어 플래그를 제거합니다. 반복적으로 실행할 때, boolean 형식을 사용하여 반복문을 제어하는 기능으로만 사용하는 플래그 역할을 하는 변수를 말합니다. 제어 플래그 대신 <span class="h-yellow"> break, continue, return</span> 을 사용하여 반복문을 제어합니다.
```javascript
// ASIS
let flag = true
for (let i = 0; i < 10 && flag; i++) {
  console.log(i)
  if (i === 3) {
    flag = false
  }
}
// TOBE
for (let i = 0; i < 10; i++) {
  console.log(i)
  if (i === 3) { break; }
}
```

# 마무리
글을 읽고 가장 중요하다고 생각되는 것들을 가져와봤습니다. 계속 강조하는 것은 간단하게 코드를 만들고, 알아보기 쉽게 만드는 것같습니다. 평소에도 항상 지식을 갖고 코드를 만들도록 노력해봅시다! 글이 엄청 많고 길어서 며칠은 걸렸던 것 같습니다. 읽는 내내 저의 코딩 스타일도 다시 되돌아보게되고 이런 방법도 있구나~ 회고할 수 있는 값진 시간이 되었습니다. 이 글을 읽으신 분이면 [원문](https://refactoring.guru/refactoring)을 읽어보시는 것도 좋을 것 같습니다.

![capture](/assets/images/20240516/01.png)


---


- <https://refactoring.guru/refactoring>