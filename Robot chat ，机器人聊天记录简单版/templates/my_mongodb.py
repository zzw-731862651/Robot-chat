import pymongo
from bson import ObjectId
mclient = pymongo.MongoClient(host="127.0.0.1",port=27017)
mongo_db = mclient["jiqiren"]
