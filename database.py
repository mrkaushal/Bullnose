from pymongo import MongoClient

# MongoDB connection string
# conn = MongoClient('mongodb+srv://demo:rQ2Cy5BNpMZ3x246@bullnose.tmzlxt8.mongodb.net/?retryWrites=true&w=majority')
conn = MongoClient('mongodb://localhost:27017/')

# Database name and collection name in static variables
DATABASE = conn.demo


def mongodb(collection_name):
  db = DATABASE
  collection = db[collection_name] # Collection name

  return collection