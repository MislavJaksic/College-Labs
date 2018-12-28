#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import pymongo
from bson.objectid import ObjectId

class MongoCollection(object):
  def __init__(self, mongo_uri, database, collection):
    self.client
    self.



client = pymongo.MongoClient("localhost", 27017)
db = client["nmbp"]
collection = db["articles"]



start = time.time()

explaination = collection.find().sort("timestamp", pymongo.DESCENDING).limit(10).explain()

end = time.time()
print(end - start)

print(explaination)



client.close()






