#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import pymongo
from bson.code import Code

client = pymongo.MongoClient("localhost", 27017)
db = client["nmbp"]
collection = db["dvdrent"]



#input: a document
map_function = Code("""
function () {
  let country = this.customer.address.country
  let payment = this.payment
  let duration = this.film.length
  let rental_rate = this.film.rental_rate

  if (payment !== null && country !== null && duration > 120 && rental_rate > 3.0) {
    let key = {"country":country}

    let value = {}
    value.count = 1
    value.amount = payment.amount

    emit(key, value)
  }
}
""")
#output: emits (key, value) pairs

#input: key and key's values
reduce_function = Code("""
function (key, values) {
  let sum = {"count":0, "amount":0}
  
  for (let i = 0; i < values.length; i++) {
    sum.count += values[i].count
    sum.amount += values[i].amount
  }

  return sum
}
""")
#output: key and reduced values

finalise_function = Code("""
function (key, reduced_values) {
  reduced_values.amount = Math.round(reduced_values.amount * 100) / 100  

  return reduced_values
}
""")




start = time.time()
results = collection.map_reduce(map_function, reduce_function, "dvd_results", finalize=finalise_function)
end = time.time()
print(end - start)
print(results)



client.close()






