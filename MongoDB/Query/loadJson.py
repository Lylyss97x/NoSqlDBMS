import json
# Connexion MongoDB
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')

#Connexion BDD
db = client.mydb
#Connexion collection
collection = db.mycollection

# Supprimer tous les documents de la collection
collection.delete_many({})


with open("accounts.json", "r") as file:
    data = json.load(file)

result = collection.insert_many(data)
print("Inserted data with the following IDs:", result.inserted_ids)

#Create index(already create)
"""index_name = "city_index"
collection.create_index("city", name=index_name)"""

#Find all acounts with one parameter
city = "Changi"
results = collection.find({"city": city})

for result in results:
    print(result)

#Find all account with value
min_balance = 30000
results = collection.find({"balance": {"$gt": min_balance}})

for result in results:
    print(result)


#Find total balance
pipeline = [
    {"$group": {"_id": "$city", "total_balance": {"$sum": "$balance"}}},
    {"$sort": {"total_balance": -1}}
]

results = collection.aggregate(pipeline)
for result in results:
    print(f"{result['_id']}: {result['total_balance']}")


collection.delete_many({"email": None})

#Create index 
index_name = collection.create_index("email", unique=True)

#Find age under condition
pipeline = [
    {"$match": {"age": {"$gt": 25}}},
    {"$group": {"_id": "$age", "count": {"$sum": 1}}}
]
results = collection.aggregate(pipeline)

for result in results:
    print(result)