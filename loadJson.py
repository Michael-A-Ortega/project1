from pymongo import MongoClient
import json
from pymongo.errors import BulkWriteError

client = MongoClient()
db = client['project1']
collection = db.movies
try:
    with open('json/movies.json') as file:
        file_data = json.load(file)
        collection.insert_many(file_data) 
except BulkWriteError:
    print('Already exist')