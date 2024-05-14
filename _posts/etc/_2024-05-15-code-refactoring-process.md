---
layout: post
title: 리팩토링 방법
summary: 리팩토링의 방법들 🔨
date: 2024-05-15 10:56:12 +09:00
categories: etc
tags: refactoring
---
[리팩토링과 클린코드]({{base_path}}/etc/code-refactoring/) 이어서 작성한 글입니다.
# 리팩토링 하기 
## 메소드 정리
Method 추출하기
메소드에서 더 많은 행이 발견될수록 메소드가 수행하는 작업을 파악하기가 더 어려워집니다. 이것이 이 리팩토링의 주된 이유입니다.

코드의 거친 가장자리를 제거하는 것 외에도 메소드 추출은 다른 많은 리팩토링 접근 방식의 한 단계이기도 합니다.

이익
더 읽기 쉬운 코드! 메소드의 목적을 설명하는 이름( createOrder(), renderCustomerInfo()등) 을 새 메소드에 지정하십시오.

코드 중복이 적습니다. 메소드에 있는 코드는 프로그램의 다른 위치에서 재사용될 수 있는 경우가 많습니다. 따라서 중복 항목을 새 메서드에 대한 호출로 바꿀 수 있습니다.

코드의 독립적인 부분을 분리하므로 오류 가능성이 줄어듭니다(예: 잘못된 변수가 수정되는 경우).

리팩터링 방법
새로운 메소드를 생성하고 목적을 명확하게 하는 방식으로 이름을 지정합니다.

관련 코드 조각을 새 메서드에 복사합니다. 이전 위치에서 조각을 삭제하고 대신 새 메서드를 호출하세요.

이 코드 단편에 사용된 모든 변수를 찾으십시오. 프래그먼트 내부에서 선언되고 외부에서 사용되지 않는 경우 변경하지 않고 그대로 두면 새 메서드에 대한 지역 변수가 됩니다.

추출하는 코드보다 먼저 변수가 선언된 경우 이전에 변수에 포함된 값을 사용하려면 이러한 변수를 새 메서드의 매개 변수에 전달해야 합니다. 때로는 Temp를 Query로 대체 하여 이러한 변수를 제거하는 것이 더 쉽습니다 .

추출된 코드에서 지역 변수가 어떤 식으로든 변경되는 것을 확인하면 변경된 값이 나중에 기본 메서드에 필요할 수 있음을 의미할 수 있습니다. 이중 점검! 그리고 이것이 실제로 그렇다면 모든 기능이 계속 작동하도록 이 변수의 값을 기본 메서드에 반환합니다.


```javascript
printOwing(): void {
  printBanner();

  // Print details.
  console.log("name: " + name);
  console.log("amount: " + getOutstanding());
}

printOwing(): void {
  printBanner();
  printDetails(getOutstanding());
}

printDetails(outstanding: number): void {
  console.log("name: " + name);
  console.log("amount: " + outstanding);
}
```
## 객체간의 기능 이동
## 데이터 구성
## 조건문 단순화

# 체크리스트 ✅
앞에서 계속 언급했듯 리팩토링은 작은 변경으로 진행되어야 하고, 기존 코드를 약간 더 좋게 만들어 프로그램 오류가 없이 계속 작동되고 있어야합니다. 프로젝트에 새로운 기능을 추가하면서 연관 되어있는 부분을 생각하지 못하고 대공사를 하다가 새로운 버그를 발생시킨 적이 있습니다. 이런 버그를 만나지 않으려면 정말 작은 아주 사소한 것부터 실천을 해서 프로그램에 지장이 없도록 리팩토링을 진행해봅시다.

리팩터링 방법
리팩토링은 일련의 작은 변경으로 수행되어야 하며, 각 변경은 기존 코드를 약간 더 좋게 만드는 동시에 프로그램을 계속 작동 상태로 유지합니다.

올바른 방식으로 수행된 리팩토링 체크리스트
코드가 더 깔끔해져야 합니다.
리팩토링 후에도 코드가 여전히 깨끗하지 않다면... 미안하지만 인생의 한 시간을 낭비한 것입니다. 왜 이런 일이 발생했는지 알아보세요.

작은 변경으로 리팩토링에서 벗어나 전체 리팩토링을 하나의 큰 변경으로 혼합할 때 자주 발생합니다. 그래서 정신을 잃기 쉽습니다. 특히 시간 제한이 있는 경우에는 더욱 그렇습니다.

그러나 이는 매우 엉성한 코드로 작업할 때도 발생할 수 있습니다. 무엇을 개선하더라도 코드 전체는 여전히 재앙으로 남아 있습니다.

이 경우 코드의 일부를 완전히 다시 작성하는 것을 고려해 볼 가치가 있습니다. 하지만 그 전에 테스트를 작성하고 상당한 시간을 투자해야 합니다. 그렇지 않으면 첫 번째 단락에서 설명한 것과 같은 결과를 얻게 됩니다.

리팩토링 중에는 새로운 기능을 생성해서는 안 됩니다.
리팩토링과 새로운 기능의 직접 개발을 혼합하지 마십시오. 최소한 개별 커밋 범위 내에서 이러한 프로세스를 분리해 보세요.

리팩토링 후에는 기존 테스트를 모두 통과해야 합니다.
리팩토링 후에 테스트가 중단될 수 있는 경우는 두 가지입니다.

리팩토링 중에 오류가 발생했습니다. 이것은 생각할 필요도 없는 일입니다. 계속해서 오류를 수정하세요.

테스트 수준이 너무 낮았습니다. 예를 들어 클래스의 비공개 메서드를 테스트하고 있었습니다.

이 경우 테스트의 책임이 있습니다. 테스트 자체를 리팩터링하거나 완전히 새로운 상위 수준 테스트 세트를 작성할 수 있습니다. 이러한 상황을 피하는 가장 좋은 방법은 BDD 스타일 테스트를 작성하는 것입니다.




---

- <https://refactoring.guru/refactoring>
- [clean code - 로버트 C.마틴]