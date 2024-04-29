---
layout: post
title: "Javascript Search Params"
date: 2024-03-02 10:06:52 +0900
categories: javascript
tags: javascript
published : false
---

> array 전체 값 검사하기
Array.every((x) => {
	return x == true
})

var obj = [
	{ name: 'Max', age: 23 },
	{ name: 'John', age: 20 },
	{ name: 'Caley', age: 18 }
];

var found = obj.find(e => e.name === 'John');

**console.log(found);**

array map
array flatmap

배열, 유사배열
Array.isArray(array);
// array => true  |||  not array => false
// 배열 = 객체 + length + 메서드
// 유사배열 = 객체 + length

var array = [1, 2, 3, 4];
var node = document.querySelector('div'); 
var ele = document.body.children;

console.log(array);		// [1, 2, 3, 4]  => Array
console.log(node);		// NodeList [div, div, div] => Not Array
console.log(ele);		// HTMLCollection [noscript, div, script, ...] => Not Array

ele.forEach(function(ele, index, array){
	console.log(ele, index);
});
// 유사배열에 forEach를 썻을 때 오류난다
// Uncaught TypeError: ss.forEach is not a function

//call 을 사용해서 유사배열객체를  call의 첫번째 인자로 넘겨줘서 사용 가능!
[].forEach.call(ele, function(element, index, array){
	console.log(element, index);
});