#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import pymongo
from bson.code import Code

client = pymongo.MongoClient("localhost", 27017)
db = client["nmbp"]
collection = db["articles"]



#input: a document
map_function = Code("""
function () {
  let words = this.text.match(/[^,(?!.:; )]+/g)
  
  let word_count = {}
  words.forEach(function (word) {
    if (word in word_count) {
      word_count[word] = word_count[word] + 1
    } else {
      word_count[word] = 1
    }
  })
  
  let key = this.author
  let value = word_count
  emit(key, value)
}
""")
#output: emits (key, value) pairs

#input: key and key's values
reduce_function = Code("""
function (key, values) {
  let total_word_count = {}
  values.forEach(function(word_count) {
    for (let word in word_count) {
      if (word in total_word_count) {
        total_word_count[word] = total_word_count[word] + word_count[word]
      } else {
        total_word_count[word] = word_count[word]
      }
    }
  })

  return total_word_count
}
""")
#output: key and reduced values

finalise_function = Code("""
function (key, reduced_values) {
  let limited_word_count = []
  for (let property in reduced_values) {
    limited_word_count.push([property, reduced_values[property]])
  }

  // sort descending
  limited_word_count.sort(function(a, b) {
    return b[1] - a[1]
  })
  
  return limited_word_count.slice(0, 10)
}
""")



start = time.time()
results = collection.map_reduce(map_function, reduce_function, "words_per_author", finalize=finalise_function)
end = time.time()
print(end - start)
print(results)



client.close()






