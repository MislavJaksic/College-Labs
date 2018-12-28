#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("localhost", 27017)
db = client["nmbp"]
collection = db["articles"]



start = time.time()

collection.update({"_id" : ObjectId("5c223e76e380c80f43933d60")},
                  {"$push" : {"comments" : "Hello world!"}})
end = time.time()
print(end - start)



client.close()






