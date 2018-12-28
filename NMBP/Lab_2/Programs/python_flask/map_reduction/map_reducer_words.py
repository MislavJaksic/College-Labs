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
  
  words.forEach(function (word) {
    let key = word
    let value = 1
    emit(key, value)
  })
}
""")
#output: emits (key, value) pairs

#input: key and key's values
reduce_function = Code("""
function (key, values) {
  return Array.sum(values)
}
""")
#output: key and reduced values



start = time.time()
results = collection.map_reduce(map_function, reduce_function, "tempMapReduceResults")
end = time.time()
print(end - start)
print(results)



client.close()






