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
  var total_word_count = {}
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



start = time.time()
results = collection.map_reduce(map_function, reduce_function, "tempMapReduceResults")
end = time.time()
print(end - start)
print(results)



client.close()






