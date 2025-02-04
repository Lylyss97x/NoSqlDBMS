#Connexion MongoDB
from pymongo import MongoClient, ASCENDING
client = MongoClient('mongodb://localhost:27017/')

#Connexion BDD
db = client.mydb
#Connexion collection
collection = db.mycollection

#Conditions
query = {
    "$and": [
        {"age": {"$gt": 25}},
        {"email": {"$regex": "@example\.com$"}}
    ]
}
documents = collection.find(query)

for doc in documents:
    print(doc)

#Limit
query = {"age": {"$gt": 25}}
projection = {"_id": 0, "name": 1, "email": 1}
documents = collection.find(query, projection)

for doc in documents:
    print(doc)

#Sort
query = {"age": {"$gt": 25}}
documents = collection.find(query).sort("name", ASCENDING)

for doc in documents:
    print(doc)