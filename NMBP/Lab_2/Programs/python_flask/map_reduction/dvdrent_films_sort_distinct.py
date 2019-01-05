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
  let rating = this.film.rating
  let title = this.film.title
  let actors = this.film.actors
  
  let number_of_actors = 0
  for (let actor in actors) {
    number_of_actors += 1
  }

  if (number_of_actors >= 10) {
    let key = {"rating":rating}

    let value = {}
    value.title = [title]
    value.actors = [number_of_actors]

    emit(key, value)
  }
}
""")
#output: emits (key, value) pairs

#input: key and key's values
reduce_function = Code("""
function (key, values) {
  let count = {"title":[], "actors":[]}
  
  for (let i = 0; i < values.length; i++) {
    let value = values[i]
    for (let j = 0; j < value.title.length; j++) {
      count.title.push(value.title[j])
      count.actors.push(value.actors[j])
    }
    
  }
  return count
}
""")
#output: key and reduced values

finalise_function = Code("""
function (key, reduced_values) {
  let everything = {"films":[]}
  let distincter = []

  let titles = reduced_values.title
  let all_number_of_actors = reduced_values.actors

  for (let i = 0; i < titles.length; i++) {
    let title = titles[i]
    let actors = all_number_of_actors[i]

    if (distincter.indexOf(title) === -1) {
      distincter.push(title)

      let film = {}
      film.title = title
      film.actors = actors

      everything.films.push(film)
    }
  }
  
  everything.films.sort(function(a, b) {
    return a.title > b.title
  })
  return everything
}
""")




start = time.time()
results = collection.map_reduce(map_function, reduce_function, "dvd_results", finalize=finalise_function)
end = time.time()
print(end - start)
print(results)



client.close()






