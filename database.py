from pymongo import MongoClient

try:
    conn = MongoClient()
    # print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

def mongodb(collection_name):
  db = conn.bullnose # Database name
  collection = db[collection_name] # Collection name

  return collection