import pymongo
from bson.objectid import ObjectId



def GetArticles():
  client = pymongo.MongoClient("localhost", 27017)
  db = client["nmbp"]
  collection = db["articles"]

  cursor = collection.find().sort("timestamp", pymongo.DESCENDING).limit(10)
  articles = [article for article in cursor]
  client.close()

  return articles

def AddCommentById(comment, id):
  client = pymongo.MongoClient("localhost", 27017)
  db = client["nmbp"]
  collection = db["articles"]

  collection.update({"_id" : ObjectId(id)},
                    {"$push" : {"comments" : comment}})
  client.close()





