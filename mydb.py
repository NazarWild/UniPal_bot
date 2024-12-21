from pymongo import MongoClient
import pymongo
import json
import random
from bson import ObjectId

import certifi
ca = certifi.where()


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = \
        ("mongodb+srv://mag4147731:pURmzg6GtqEa1i0z@unipalclaster.rmqvr.mongodb.net/?retryWrites=true&w=majority"
         "&appName=UniPalClaster")
    client = MongoClient(CONNECTION_STRING, tlsCAFile=ca)

    return client['UniPal_DB']


myDB = get_database()

users_collection = myDB['users']


def generate_random_users(count=5):
    names = ["Олександр", "Марія", "Іван", "Андрій", "Ольга"]
    surnames = ["Шевченко", "Коваленко", "Бойко", "Козак", "Мельник"]
    genders = ["Чоловік", "Жінка", "Чоловік", "Чоловік", "Жінка"]

    for i in range(count):
        user = {
            "name": names[i - 1],
            "surname": surnames[i - 1],
            "age": random.randint(18, 60),
            "gender": genders[i - 1]
        }
        users_collection.insert_one(user)