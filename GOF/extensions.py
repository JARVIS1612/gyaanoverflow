from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pymongo

conn_str = "mongodb+srv://admin:admin@vaibhav.ki2u279.mongodb.net/?retryWrites=true&w=majority"

mongo = pymongo.MongoClient(conn_str, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)