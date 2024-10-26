import pymongo
import os

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["NP_Rec"]
users_collection = db["users"]

# Function to add a new user and update the database with the QR code path
def add_new_user():
    # Get user details interactively
    user_id = int(input("Enter User ID: "))
    license_no = input("enter the license plate number : ")
    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    mobile_number = int(input("Enter Mobile Number: "))
    wallet_balance = float(input("Enter Wallet Balance: "))

    # Create user data (without the QR code path for now)
    user_data = {
        "user_id": user_id,
        "licence_number":license_no,
        "name": name,
        "age": age,
        "mobile_number": mobile_number,
        "wallet_balance": wallet_balance
    }

    # Insert the user data into MongoDB
    users_collection.insert_one(user_data)

add_new_user()