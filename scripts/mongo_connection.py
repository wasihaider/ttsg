from pymongo import MongoClient

###########################################################

client = MongoClient('localhost:27017', connect = False)

db_users = client['user']
db_images = client['images']

###########################################################
