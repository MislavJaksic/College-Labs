#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client["nmbp"]
collection = db["articles"]



collection.create_index([("timestamp", pymongo.DESCENDING)])



client.close()






