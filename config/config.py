from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://akashsoni3101:tGmgo5qJrztSFmrH@naadvenu.simddgx.mongodb.net/"

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.naadvenuDB
blogs = db["blogs"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)