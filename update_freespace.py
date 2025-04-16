from ultralytics import YOLO
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime

CONNECTION_STRING = "mongodb+srv://kishorebabu200409:kishore26@cluster0.hf4t5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# rzp_test_GL7rIL2x0NYu1z

# 3fHjboaIwgTaGP8qGQAMMFfU


# Connect to MongoDB Atlas
client = MongoClient(CONNECTION_STRING)
db = client['number_plate_recognition'] 
users_collection = db['user']  
user_entry = db['entry']
user_exit = db['exit']
path_collection = db['parkingspace']


def update_space(i,j):
    # Fetch all documents from 'parkingspace' collection
    cursor = path_collection.find({})

    for doc in cursor:
        path = doc.get("path", [])  # Get the 'path' field (a 2D array)

        if len(path) > 1 and len(path[1]) > 1:  # Ensure valid index
            path[i][j] = 0  # Set a specific part of the array to 0

            # Update the document in MongoDB
            path_collection.update_one(
                {"_id": doc["_id"]},  # Find document by _id
                {"$set": {"path": path}}  # Update the path field
            )

# update_space()

def reset_parking_space():
    # Fetch all documents from 'parkingspace' collection
    cursor = path_collection.find({})

    for doc in cursor:
        path = doc.get("path", [])  # Get the 'path' field (a 2D array)

        if isinstance(path, list):  # Ensure path is a list
            # Set all values in the 2D array to 0
            path = [[0 for _ in row] for row in path]

            # Update the document in MongoDB
            path_collection.update_one(
                {"_id": doc["_id"]},  # Find document by _id
                {"$set": {"path": path}}  # Update the path field
            )
            print(f"Path reset to 0s.")