---
layout: post
title: 리팩토링은 왜 하는 걸까? 
summary: 리팩토링을 알아보자!
date: 2024-05-14 10:56:12 +09:00
categories: etc
tags: refactoring
---


> Refactoring is a systematic process of improving code without creating new functionality, that can transform a mess into clean code and simple design.

# Code Refactoring

사용하지 않는 코드 또는 중복된 코드를 지우고, 코드의 로직을 깨끗하고 이해하기 쉽게 디자인하는 것 "Code Refactoring" 입니다. <span class="h-yellow">"without creating new functionality"</span> 새로운 기능을 만들지 않고, 깨끗한 코드와 간단한 디자인으로 변환하는 것입니다. 코드 가독성 향상 및 복잡성 감소, 성능 향상을 목표로 리팩토링을 배우고 실천해 보는 것이 목표입니다. 

처음부터 요구사항에 맞게 설계를 정확히 하고 코드 컨벤션을 만들어서 확장성 있는 개발이 진행되면 좋겠지만, 현실에서 계속 움직이는 프로젝트떄문에 마음대로 되는 것이 없습니다. 더 나은 소스코드를 위해 리팩토링을 왜 해야되는지, 언제 하는 게 좋은지, 또 리팩토링은 어떻게 하는지 방법을 공부하려고 합니다.

## Clean Code 🫧

리팩토링의 주요 목적은 기술적 부채와 싸우는 것입니다. 기존 코드를 깔끔한 코드와 심플한 디자인으로 바꿔줍니다.

깨끗한 코드란 무엇일까요? 

__가독성__ - 깔끔하고 명시적인 변수명, 함수명 등으로 다른 사람이 알아보기 쉬운 코드를 작성합니다.<br>
__중복 제거__ - 중복된 코드 최소화 합니다.<br>
__간결성__ - 짧고 단순하게 필요한 내용만 유지합니다.<br>

## 기술적 부채 💸

그렇다면 ~~지저분한~~ 코드는 왜 생기는 것일까요? 비즈니스 압력, 테스트 부족, 문서 부족, 커뮤니케이션 부족 등 여러가지 이유들로 기술적 부채가 쌓이게 되고 점점 이자가 쌓이게 되는 것입니다. 

특히, 프로젝트의 요구사항은 끊임없이 변경됩니다. 그런 상황에서 쓰이지 않는 코드가 쌓이고 기존에 있는 함수가 복잡해지면서 이 코드의 방어 코드를 또 작성을 하다보면 의존성이 높은 코드가 생기게 됩니다.

## 언제 해야할까?

새로운 기능을 만들지 않고 깨끗한 코드와 디자인으로 변환하라고요? 도대체 언제 진행해야되는 걸까요? 리팩토링은 코드를 더 좋게 개선하기 위해서 개발과정에서 수시로 진행을 합니다.

__3의 법칙__ - 하고 있는 일이 세번째로 반복이 될 때.<br>
__기능 추가__ - 새로운 기능을 추가하거나 다른 사람의 코드를 수정할 때.<br>
__버그 수정__ - 버그를 수정할 때.<br>
__코드 리뷰__ - 동료와 코드 리뷰를 할 떄.<br>

# 체크리스트 
앞에서 계속 언급했듯 리팩토링은 작은 변경으로 진행되어야 합니다. 더 중요한 것은, 기존 코드를 약간 더 좋게 만들어 프로그램 오류가 없이 계속 작동되고 있어야합니다. 리팩토링때문에 잘 작동하고 있던 프로그램이 오작동을 하고, 버그가 생긴다면 당연히 리팩토링을 진행하지 않았던 코드보다 더 끔찍한 일입니다. 성공적인 리팩토링 체크리스트를 가지고 리팩토링 후에 검토를 해보면 좋을 것 같습니다.

✅ 코드가 더 깔끔해졌다.
리팩토링을 했는데 코드가 더 복잡해졌거나 간결해지지 않았다면 리팩토링을 한 의미가 없습니다. 복잡도가 높은 부분이라면 충분한 시간을 가지고 이 코드 전체를 다시 작성을 하는 것이 더욱 좋은 코드를 만들 수 있습니다.

✅ 새로운 기능을 생성하지 않는다.
리팩토링을 할 때는 새로운 기능이 추가되지 않아야합니다.

✅ 기존 테스트를 모두 통과했다.
당연한 결과입니다. 리팩토링 후에 기존이 되던 기능이 동작되지 않는다면 리팩토링을 하지 않는 것이 더 바람직합니다. 리팩토링 후에는 충분한 테스트를 거쳐 기능이 정상작동해야합니다.




## 리팩토링 적용하기

> 새로운 기능 추가 없이! 기존 기능은 오류 없이!

저는 리팩토링을 하기 전에는 테스트코드를 먼저 생성해두거나 테스트케이스를 작성을 해둔 후 진행하는 것이 바람직하다고 생각합니다. 

다양한 리팩토링의 기법중, 메서드와 조건문기반으로 리팩토링을 알아보겠습니다. 💪

# 메서드 정리
__Composing Methods__

리팩토링을 할 때 가장 큰 부분은 메서드들을 다듬고 정리하는 것입니다. 간결하고 명시적으로, 기능별로 작성된 메서드 들은 가독성을 많이 높여줍니다. 메서드를 정리하는 방법들은 어떤 것들이 있을까요?

## 메서드 쪼개기
__Extract Method__ 기존 메서드를 기능 단위로 추출하기

메서드가 길어지고 복잡해질 수록 어떤 기능을 가진 메서드인지 파악하기가 어렵습니다.
기존 메서드를 <span class="h-yellow">기능 단위로 추출</span>한 후 알맞는 이름을 지어줍니다. 메서드가 잘 쪼개져 있을 수록 다른 메서드에서 사용되기 쉽습니다. 그래서 메서드는 최대한 하나의 리턴값을 갖도록 쪼개줍니다. Extract Method 기법을 통해 더 읽기 쉽고, 중복이 적고, 오류 발생을 줄일 수 있습니다.

```javascript
// AS-IS
printInfo() {
  printPrice();

  // Print Orders.
  console.log("name: " + name);
  console.log("orders: " + getOrders());
}

// TO-BE
printInfo() {
  printPrice();
  printOrders(getOrders());
}

printOrders(orders: number) {
  console.log("name: " + name);
  console.log("orders: " + orders);
}
```

## 변수 쪼개기
__Extract Variable__ 데이터를 임시 변수로 사용하기

변수를 추출합니다. Extract Method를 하기 위해 먼저 진행해야하는 단계가 될 수도 있습니다. if() 문이나 ?: operator를 사용할때, for() 문을 사용할 때 등 임시 변수를 사용합니다. 이때 변수명을 지을 때는 메서드의 목적으로 이름을 만들어 줍니다. 아무리 변수를 쪼개놓고 임시 변수를 사용한다고 해도 a, b 같은 이름을 사용한다면 더욱 복잡해지겠죠?

❗️여기서 주의 <br>
__Introduce Explaining Variable__<br>
복잡한 수식을 사용하는 경우에는 메서드의 목적으로 된 이름을 사용합니다.

```javascript
// AS-IS 😩
if ((platform.toUpperCase().indexOf("MAC") > -1) &&
      (browser.toUpperCase().indexOf("IE") > -1) &&
      wasInitialized() && resize > 0 )
{
}
// TO-BE 🤩
const isMasOS = platform.toUpperCase().indexOf("MAC") > -1;
const isIEBrowser = browser.toUpperCase().indexOf("IE") > -1;
const wasResized = 0;

if( isMacOS && isIEBrowser && wasInitialized() && wasResized )
{
}
```


## 인라인 방식 사용
__Inline Methods__ 그리고 __Inline Temp__<br>
불필요한 메서드를 최소화합니다. 메서드가 메서드 그 자체의 역할을 한다면 과감하게 삭제를 해줍니다.

메서드뿐만아니라 변수를 사용하는 경우에도 마찬가지입니다.

```javascript
// AS-IS 😩
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
// TO-BE 🤩
getRating(){
  return orders > 5 ? 2 : 1;
}
hasDiscount(order) {
  return order.basePrice() > 1000;
}
```

## 임시 변수 사용
__Replace Temp with Query__ 계산식을 변수로 사용

Temp(임시변수)를 Query로 대체하면 코드를 별도의 메서드로 추출하는 데 방해가 되는 지역 변수를 제거할 수 있습니다. 즉, 임시 변수를 의미있는 메서드 호출로 바꿔서 코드 중복을 줄이고 가독성을 높일 수 있습니다.

```javascript
// AS-IS
calculateTotal(): number {
  let basePrice = quantity * itemPrice;
  if (basePrice > 1000) {
    return basePrice * 0.95;
  }
  else {
    return basePrice * 0.98;
  }
}
//  TO-BE
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

__Split Temporary Variable__ 임시 변수 쪼개기

임시변수에 여러가지 값을 대입하는 경우에는 임시변수를 더 생성해 추출해내는 것입니다. 이부분은 정말 중요하다고 생각이드는데요. 변수 하나를 선언 해 그 변수에 값을 넣었다 뺐다 바꿨다 하다보면 말그대로 스파게티 🍝 코드 완성이라고 생각합니다. 아무리 임시변수여도 어떤 값을 가진 변수인지 한눈에 알아보기 쉬우면 좋겠죠! 저는 값이 변하는 변수 이외에는 const 선언을 자주 사용해서 이런 일이 없지만, 하나의 변수에 값을 계속 바꿔 코드를 작성하는 것은 오류를 만나는 지름길인 것 같습니다. 처음 작성부터 사용하지 않고 리팩토링할 일이 없는 게 베스트인 것 같네요...
```javascript
// AS-IS
let temp = 2 * (height + width);
console.log(temp);
temp = height * width;
console.log(temp);
// TO-BE
const perimeter = 2 * (height + width);
console.log(perimeter);
const area = height * width;
console.log(area);
```
이와 비슷하게 주의해야할 점도 있습니다. <br>
__Remove Assignments to Parameters__ <br>
```info
프로그램의 각 요소는 한 가지만 담당해야 합니다.
이렇게 하면 부작용 없이 코드를 안전하게 교체할 수 있어 코드 유지 관리가 훨씬 쉬워집니다.
```
파라미터로 전달 된 값은 새로운 값에 할당하여 사용하는 것입니다. 파라미터의 값을 바로 변경하면 호출을 요청한 곳에서도 영향을 끼칠 위험이 있습니다. 당연한 부분이었지만 항상 조심하고 주의를 기울여야할 부분입니다.


## 알고리즘 대체
__Substitute Algorithm__ 알고리즘을 더 간단하고 쉬운 방법으로 변경

어떤 기능을 수행하거나, 어떤 값을 찾아야하는 일을 할 땐 다양한 방법들이 있습니다. 그중에서 가장 쉽고 간단명료한 방법으로 바꿔줍니다. 이때 미리 메서드를 분리해두었다면 더욱 간단합니다! 복잡하고 큰 알고리즘을 변경하는 것보다 간단하고 작은 알고리즘을 변경하는 것이 더 쉽습니다. 당연히 변경한 알고리즘은 변경 전의 알고리즘과 값이 같아야겠죠?
```javascript
// AS-IS
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
// TO-BE
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

거대한 산을 하나 넘었습니다. 하지만 이제 시작에요. 집중해서 공부를 해봅시다! 올바르게 메서드를 작성을 했는지, 동작을 필요한 메서드에 정확히 작성을 했는지 확인합니다.
## Move Method
## Move Field 
# 데이터 구성 -->


# 조건식 단순화
__Simplifying Conditional Expressions__

코드로 가장 간단하고 빠르게 구현을 하기위해, 또는 요구사항이 점점 늘어남에따라서 조건문이 점점 늘어나고 복잡해지기마련입니다... 조건문이 길고 복잡하면 코드를 알아보기가 정말 힘들어요. 이 문제를 해결하기 위한 많은 기술들이 있습니다.

## 조건부 분해
__Decompose Conditional__ 복잡한 조건문을 별도의 메서드로 분리

조건부를 간단하게 작성하는 것입니다. 함수를 분석할 때 조건문으로 가득 찬 경우가 정말 함수를 이해하기가 어렵습니다. 코드가 길어진다면 앞에 정의해둔 조건도 기억이 나지 않을 떄도 있습니다. 조건부 코드를 메서드로 추출하여 조건을 알아볼 수 있도록 이름을 지정해서 조건부 코드를 리팩토링 합니다.

```javascript
// AS-IS
if (date.before(SUMMER_START) || date.after(SUMMER_END)) {
  charge = quantity * winterRate + winterServiceCharge;
}
else {
  charge = quantity * summerRate;
}
// TO-BE
if (isSummer(date)) {
  charge = summerCharge(quantity);
}
else {
  charge = winterCharge(quantity);
}
```

## 조건식 통합
__Consolidate Conditional Expression__ 불필요한 조건문을 줄이기

메서드 내에서 동일한 판단을 하고 있는 조건문이 나열되고 있다면 조건을 메서드로 만들어 단일 표현식으로 합쳐줍니다. 이렇게 조건을 메서드로 만들어두면 똑같은 조건을 검사해야되는 곳에서 코드 중복도 줄일 수 있습니다.
```javascript
// AS-IS
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
//TO-BE
disabilityAmount(): number {
  if (isNotEligibleForDisability()) {
    return 0;
  }
  // Compute the disability amount.
  // ...
}
```

__Consolidate Conditional Expression__ 조건식 안에 있는 중복 구문 빼기

조건식 안에서 중복되어 표현되는 코드를 조건식 밖으로 빼줍니다. if문을 이해하고 있다면 if에 걸리든, else에 걸리든 조건식 밖에 있는 코드도 실행된다는 것은 알고있을 겁니다. 이렇게 모든 조건에서 실행되는 코드는 조건문 밖으로 빼서 코드의 중복을 줄입니다.
```javascript
// AS-IS
if (isSpecialDeal()) {
  total = price * 0.95;
  send();
}
else {
  total = price * 0.98;
  send();
}
//TO-BE
if (isSpecialDeal()) {
  total = price * 0.95;
}
else {
  total = price * 0.98;
}
send();
```

## 제어 플래그 제거
__Remove Control Flag__ 제어 플래그만을 위해 사용된 변수 제거
반복적으로 실행할 때, boolean 형식을 사용하여 반복문을 제어하는 기능으로만 사용하는 플래그 역할을 하는 변수를 말합니다. 제어 플래그 대신 <span class="h-yellow"> break, continue, return</span> 을 사용하여 반복문을 제어합니다.
```javascript
// AS-IS
let flag = true
for (let i = 0; i < 10 && flag; i++) {
  console.log(i)
  if (i === 3) {
    flag = false
  }
}
// TO-BE
for (let i = 0; i < 10; i++) {
  console.log(i)
  if (i === 3) { break; }
}
```

## 중첩 조건문 지양
__Replace Nested Conditional with Guard Clauses__
중첩된 조건문을 보호 조항으로 대체합니다. " 각 중첩 수준의 들여쓰기는 화살표를 형성하여 고통과 비애의 방향을 오른쪽으로 가리킵니다." 라고 표현이 되어있어서 너무 공감되고 재미있었습니다. 사실 코드분석을 하려고 할 때, 들여쓰기가 5depth만 들어가있어도 이건 뭐지...? 하고 보게 되는 것 같아요. 물론 제가 작성한 코드일 때도 똑같죠. 이렇게 코드가 작성이 되어있으면 조건문이 어떤 것을 의미하는지 파악하기가 어렵습니다. 

** 핵심 **

조건문을 사용할 때 return 을 적극 활용하여 depth가 깊어지지 않게 빠른 종료를 해줍니다.

```javascript
getPayAmount(): number {
  let result: number;
  if (isDead){
    result = deadAmount();
  }
  else {
    if (isSeparated){
      result = separatedAmount();
    }
    else {
      if (isRetired){
        result = retiredAmount();
      }
      else{
        result = normalPayAmount();
      }
    }
  }
  return result;
}

getPayAmount(): number {
  if (isDead){
    return deadAmount();
  }
  if (isSeparated){
    return separatedAmount();
  }
  if (isRetired){
    return retiredAmount();
  }
  return normalPayAmount();
}
```



# 메서드 호출 단순화
__Simplifying Method Calls__ 

메서드 호출을 더 간단하고 이해하기 쉽게 만듭니다. 클래스 간 상호 작용을 위한 인터페이스를 단순화 시켜 알아보기 쉬운 코드로 리팩토링을 해봅시다!

## 메서드 이름 바꾸기
__Rename Method__ 메서드를 충분히 설명하는 작명
메서드 이름을 과도한 축약어로 사용하면 그룹원들과 합의한 것이더라도 헷갈리는 일도 많고, 새로 투입되는 인원들은 코드를 봤을 때 엄청 어질어질하겠죠. 메서드를 충분히 설명하는 이름으로 변경을 해줍니다.

```javascript
 // AS-IS
const getUsrNm

 // TO-BE
const getUserName
```

## 적절한 매개변수 사용
__Add Parameter__ 그리고 __Remove Parameter__

필요한 경우 새로운 매개변수를 추가합니다. 항상 객체에 보관하는 것이 의미가 없거나 자주 변경되는 데이터가 필요할 때 새로운 매개변수를 추가하여 전달합니다
사용되지 않는 매개변수는 제거해줍니다. 코드를 작성할 때 확장성을 고려하거나 여러가지 요인으로 사용하지 않는 매개변수가 잔뜩 생겨져 있습니다. 이것들을 깔끔하게 정리 해줍니다.

__❗️Long Parameter List 주의__

파라미터를 제거하는 것보다 새로운 파라미터를 추가하는 것은 간단하기 때문에 파라미터가 엄청나게 길어질 때를 항상 주의합니다.

```javascript
 // AS-IS
getUserName(userCode, userId){
  return userList.find(user=>user.code === userCode).name
  //...
}

 // TO-BE
getUserName(userCode){
   return userList.find(user=>user.code === userCode).name
}
```

## 최소 기능단위 분리
__Separate Query from Modifier__

조회와 업데이트를 동시에 하고 있는 메서드는 좋지 않습니다. 최소 기능 단위로 메서드를 분리해줍니다.
```javascript
 // AS-IS
getUserNameAndSetNickName(){ }
 // TO-BE
getUserName(){ }
setNickName(){ }
```

## 매개변수 사용
__Parameterize Method__ 매개변수화 하기

비슷한 기능을 하지만 다른 값을 가지는 메소드는 파라미터를 사용해서 결합합니다. 한가지 값만 동일하고 나머지가 다 다른 상황이고, 동작이 다르다면 당연히 나누어져있는 게 좋은 방법입니다. 나머지 값이나 조건이 동일하고 같은 동작을 하는경우 메서드 결합을 통해서 중복된 코드를 줄일 수 있습니다.
```javascript
 // AS-IS
joinUnderFifteen(){ }
joinMoreFifteen(){ }
 // TO-BE
join(age){ }
```

__Replace Parameter with Explicit Methods__ 매개변수를 명시적 메서드로 바꾸기

매개변수가 다른 의미를 가진 메서드는 최악이라고 생각합니다. 어떤 데이터가 들어올지 예상을 할 수도 없고 예외처리만 점점 늘어나게 되죠. 이런 메서드는 나누어줍니다.

```javascript
// AS-IS
setCharactor(name: string, value: number): void {
  if (name == 'gender') {
    gender = value;
    return;
  }
  if (name == 'nickName') {
    nickName = value;
    return;
  }
}
// TO-BE
setGender(gender: number){
  gender = gender;
}
setNickName(nickName: string){
  nickName = nickName;
}
```

## 객체 매개변수
__Preserve Whole Object__ 객체 사용

객체에서 값을 가져와서 변수로 저장을 해서 사용하지 않고 원본 객체를 그대로 전달해줍니다.
```javascript
// AS-IS
let age = user.getAge();
let name = user.getName();
let printUserInfo = print.user(age, name);
// TO-BE
let printUserInfo = print.user(user);
```

__Introduce Parameter Object__ 매개변수를 객체화

반복되는 매개변수들이 있다면 객체로 바꿔서 사용해줍니다.
```javascript
// AS-IS
getDateRan(start: Date, end: Date)
// TO-BE
getDateRan(date: DateRange)
```

## 예외처리
__Replace Constructor with Factory Method__ 오류 코드 예외처리

프로그램이 실행될 때 오류가 발생하면 안 되죠. 적절한 예외처리를 추가해줍니다. 중요한 것은 코드 실행이나 조건을 위해서 예외를 사용하면 안 된다는 것입니다. 예외는 오류나 심각한 상황을 알리기 위해서만 사용을 합니다.
```javascript
// AS-IS
withdraw(amount: number): number {
  if (amount > _balance) {
    return -1;
  }
  else {
    balance -= amount;
    return 0;
  }
}
// TO-BE
withdraw(amount: number): void {
  if (amount > _balance) {
    throw new Error();
  }
  balance -= amount;
}
```
__Replace Exception with Test__ 예외를 테스트로 대체

위와 이어지는 내용으로, 조건문으로 피할 수 있는 예외로 만들기 전에 조건문으로 피합니다.
```javascript
// AS-IS
getValueForPeriod(periodNumber: number): number {
  try {
    return values[periodNumber];
  } catch (ArrayIndexOutOfBoundsException e) {
    return 0;
  }
}
// TO-BE
getValueForPeriod(periodNumber: number): number {
  if (periodNumber >= values.length) {
    return 0;
  }
  return values[periodNumber];
}
```
```info
지뢰밭에 들어가서 그곳에서 지뢰를 작동시켜 예외가 발생했습니다.
예외는 성공적으로 처리되었으며 당신은 지뢰밭 너머의 안전한 곳으로 공중으로 들어 올려졌습니다.
하지만 처음부터 지뢰밭 앞에 있는 경고 표지판을 읽는 것만으로도 이 모든 것을 피할 수 있었습니다.
```
재미있는 예시인데요, 예시 그대로 만나지 않아도 될 예외인데 예외로 넘기는 것은 불필요한 행동입니다. 간단한 조건식으로 처리할 수 있는 예외는 조건식으로 피해줍니다.

# 마무리
글을 읽고 가장 중요하다고 생각되는 것들을 가져왔습니다. 작성을 하다보니 거의 클린코드로 코드를 작성하는 법 같았습니다. 계속 강조하는 것은 간단하게 코드를 만들고, 알아보기 쉽게 만드는 것, 상황에 맞게 적절한 메서드와 변수를 사용하는 것들이었네요. 평소에도 항상 지식을 갖고 코드를 만들도록 노력해봅시다! 글이 엄청 많고 길어서 읽는 데도, 정리하는 데도 며칠은 걸렸렸습니다. 읽는 내내 저의 코딩 스타일도 다시 되돌아보게되고 이런 방법도 있구나~ 회고할 수 있는 값진 시간이 되었습니다. 이 글을 읽으신 분이라면 [원문](https://refactoring.guru/refactoring)에 예시와 재미있는 설명이 있으니 읽어보시는 것도 좋을 것 같습니다. (조금 길어요 😅)

![capture](/assets/images/20240516/01.png)


---


- <https://refactoring.guru/refactoring>
- <https://refactoring.guru/refactoring>