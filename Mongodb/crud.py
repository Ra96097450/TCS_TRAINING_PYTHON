import pymongo
from pymongo import MongoClient

uri ="mongodb://localhost:27017/"
client = MongoClient(uri)

database = client.cars_dealership
collection = database.cars




pipeline =[
    {"$match":{"fuel_type":"Petrol"}},
    {"$group":{"_id":"$maker","total":{"$sum":1}}},
    {"$sort":{"total":-1}},
    {"$project":{"_id":0,"maker":"$_id","model":1,"total":1}}
]

p = [
    {
        "$count":"total_cars"
    }
]

r = collection.aggregate(p)

for i in r:
    print(i)