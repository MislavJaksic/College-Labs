#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("localhost", 27017)
db = client["nmbp"]
collection = db["articles"]



start = time.time()

collection.update({"_id" : ObjectId("5c1e774ee380c811099f8824")},
                  {"$push" : {"comments" : "Yet another..."}})
end = time.time()
print(end - start)



client.close()






