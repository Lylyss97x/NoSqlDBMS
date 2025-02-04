import json
from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')

db = client.mydb
collection = db.mycollection

with open("accounts.json", "r") as file:
    data = json.load(file)

result = collection.insert_many(data)

print("Inserted data with the following IDs:", result.inserted_ids)


index_name = "city_index"
collection.create_index("address.city", name=index_name)

city = "Bradshawborough"
results = collection.find({"address.city": city})

for result in results:
    print(result)

min_balance = 30000
results = collection.find({"balance": {"$gt": min_balance}})

for result in results:
    print(result)
