// Few useful JS snippets for solving AdvDB HW
// Latest version is always here: https://repl.it/repls/PoshVirtualAttributes 
// Few useful JS snippets for solving AdvDB HW

console.log("DATES");
// Date stuff:
var minDate = new Date("2008-10-04T07:14:00.000Z");
var maxDate = new Date("2018-10-11T01:38:00.000Z");
// Diff in days:
var diff = Math.round((maxDate-minDate)/(1000*60*60*24));
console.log(diff);
// Extract year:
console.log(maxDate.getFullYear());


console.log("\n\nROUNDING NUMBERS");
var pi = 3.14159;
console.log('π', pi);
pi = Math.round(pi * 1000)/1000;  // to three decimals
console.log('π to three decimals', pi);
var br100 = 100.9999999;
br100 = Math.round(br100 * 1000)/1000;  // to three decimals

console.log(100.9999999, ' ROUNDED to three decimals', br100);
console.log(100.9999999, ' ROUNDED and FORMATTED to three decimals ', br100.toFixed(3));



// Array stuff:
console.log("\n\nARRAYS");
var arr1 = [1, 2, 3];
var arr2 = [6, 5, 4, 3, 2, 1];
arr1.concat(arr2);  // wrong: nothing happens, concat does NOT change the array
console.log(arr1);
arr1 = arr1.concat(arr2);
console.log(arr1);
arr1.sort(); // sort CHANGES the array
console.log('default sort', arr1);
arr1.sort(function(a, b) {
  return b - a;
}); // sort CHANGES the array
console.log('custom sort (using compare function)', arr1);


// DISTINCT array:
var darr1 = arr1.filter((obj, idx, arr) => (
        arr.findIndex((o) => o === obj) === idx
      ));
console.log('distinct array', darr1);      



// Object stuff:
console.log("\n\nOBJECTS");
var obj = {};
console.log(obj);
obj.a = 'a-value';
obj['b'] = 'b-value';
console.log(obj);
Object.keys(obj).forEach(key => {
    console.log('object key:', key, 'object value:', obj[key]);
}); 
// Let's us it as a hash map:
// First, remove a and b:
delete obj.a;
delete obj.b;
arr1.forEach(function(elem) {  // or you can use for(i = 0; i < arr1.length; ++i)
  if (obj[elem]) obj[elem]++;
  else obj[elem] = 1;
});
console.log(obj);


console.log("\n\STRING OPs");
var s = "A woodchuck would chuck as much wood as a woodchuck could chuck if a woodchuck could chuck wood";

console.log('s.indexOf("wood")', s.indexOf('wood'));
console.log('s.indexOf("metal")', s.indexOf('metal'));

console.log('s.search("wood")', s.search('wood'));
console.log('s.search("wood")', s.search(/wood/));
console.log('s.search(/wOOd/i)', s.search(/wOOd/i));
console.log('s.search(/wOOd/ig)', s.search(/wOOd/ig));
console.log('s.match(/wOOd/i)', s.match(/wOOd/i));
console.log('s.match(/wOOd/ig)', s.match(/wOOd/ig));
console.log('\n Via variable:');
// via a variable:
var targets = ['wood', 'Chuck'];
targets.forEach(function(elem) {  // or you can use for(i = 0; i < arr1.length; ++i)
  let re = new RegExp(elem, "gi");
  console.log(re, s.match(re));
});

// Be careful with regexs, might not work identical in mongo's js env
//  eg try splitting string in words
console.log(s.match(/\S+/g));
// works here, not so much in Mongo (at least for me :()