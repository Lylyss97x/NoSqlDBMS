#Connexion MongoDB
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')

#Connexion BDD
db = client.mydb
#Connexion collection
collection = db.mycollection

#Insert
document = {"name": "John Doe", "email": "john.doe@example.com", "age": 30}
result = collection.insert_one(document)
print("Inserted document ID:", result.inserted_id)

#Insert many
documents = [
    {"name": "Alice", "email": "alice@example.com", "age": 25},
    {"name": "Bob", "email": "bob@example.com", "age": 35}
]
result = collection.insert_many(documents)
print("Inserted document IDs:", result.inserted_ids)

#Read  
query = {"name": "John Doe"}
document = collection.find_one(query)
print(document)

#Read many
query = {"age": {"$gt": 25}}
documents = collection.find(query)

for doc in documents:
    print(doc)

"""#Update 
query = {"name": "John Doe"}
update = {"$set": {"age": 31}}
result = collection.update_one(query, update)
print("Modified document count:", result.modified_count)

#Update many
query = {"age": {"$gt": 25}}
update = {"$inc": {"age": 1}}
result = collection.update_many(query, update)
print("Modified document count:", result.modified_count)

#Delete
query = {"name": "John Doe"}
result = collection.delete_one(query)
print("Deleted document count:", result.deleted_count)

#Delete many
query = {"age": {"$gt": 25}}
result = collection.delete_many(query)
print("Deleted document count:", result.deleted_count)"""
