#!/usr/bin/python
# -*- coding: utf-8 -*-

from data_generation.data_functions import GetRandomTitle, GetRandomAuthor, GetRandomText, GetRandomImage, GetRandomYear, GetRandomMonth, GetRandomDay

import datetime

import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client["nmbp"]
collection = db["articles"]



for index in range(20000):
  title = GetRandomTitle()
  author = GetRandomAuthor()
  text = GetRandomText()
  image = GetRandomImage()
  comments = []

  year = GetRandomYear()
  month = GetRandomMonth()
  day = GetRandomDay()
  timestamp = datetime.datetime(year, month, day)

  random_data = {"title": title,
                 "author": author,
                 "text": text,
                 "image": image,
                 "timestamp": timestamp,
                 "comments": comments}  
  
  print(index)
  collection.insert_one(random_data)



client.close()






