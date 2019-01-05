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
  let staff_country = this.staff.address.country
  let name = this.staff.first_name
  let surname = this.staff.last_name

  let customer_country = this.customer.address.country
  let id = this.customer.customer_id

  if (staff_country === "Philippines") {
    let key = {"name":name, "lastname":surname}
    
    let value = {}
    value.id = [id]
    if (customer_country === "Philippines") {
      value.country = ["Philippines"]
    } else {
      value.country = ["Other"]
    }

    emit(key, value)
  }
  
}
""")
#output: emits (key, value) pairs

#input: key and key's values
reduce_function = Code("""
function (key, values) {
  let count = {"id":[], "country":[]}
  
  for (let i = 0; i < values.length; i++) {
    let value = values[i]
    for (let j = 0; j < value.id.length; j++) {
      count.id.push(value.id[j])
      count.country.push(value.country[j])
    }
    
  }
  return count
}
""")
#output: key and reduced values

finalise_function = Code("""
function (key, reduced_values) {
  let count = {"phil":0, "other":0}
  let distincter = []

  let ids = reduced_values.id
  let countries = reduced_values.country

  for (let i = 0; i < ids.length; i++) {
    let id = ids[i]
    let country = countries[i]

    if (distincter.indexOf(id) === -1) {
      distincter.push(id)

      if (country === "Philippines") {
        count.phil += 1
      }
      if (country === "Other") {
        count.other += 1
      }
    }
  }
  
  return count
}
""")




start = time.time()
results = collection.map_reduce(map_function, reduce_function, "dvd_results", finalize=finalise_function)
end = time.time()
print(end - start)
print(results)



client.close()






