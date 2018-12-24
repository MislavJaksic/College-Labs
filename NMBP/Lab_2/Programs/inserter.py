#!/usr/bin/python
# -*- coding: utf-8 -*-

from data_generation.data_functions import GetRandomTitle, GetRandomAuthor, GetRandomText, GetRandomPicture, GetRandomYear, GetRandomMonth, GetRandomDay

import datetime

import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client["nmbp"]
collection = db["articles"]



for index in range(19995):
  title = GetRandomTitle()
  author = GetRandomAuthor()
  text = GetRandomText()
  picture = GetRandomPicture()
  comments = []

  year = GetRandomYear()
  month = GetRandomMonth()
  day = GetRandomDay()
  timestamp = datetime.datetime(year, month, day)

  random_data = {"title": title,
                 "author": author,
                 "text": text,
                 "picture": picture,
                 "timestamp": timestamp,
                 "comments": comments}  
  
  print(index)
  collection.insert_one(random_data)



client.close()






