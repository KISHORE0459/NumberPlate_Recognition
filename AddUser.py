from pymongo import MongoClient
from datetime import datetime

# MongoDB Atlas connection string
CONNECTION_STRING = "mongodb+srv://kishorebabu200409:kishore26@cluster0.hf4t5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(CONNECTION_STRING)
db = client['number_plate_recognition']  # Updated database name
users_collection = db['user']  # Updated collection name

def add_user(user_name, number_plate, mobile_number, wallet_balance):
    """Add a new user to the database."""
    user = {
        "user_name": user_name,
        "number_plate": number_plate,
        "mobile_number": mobile_number,
        "wallet_balance": wallet_balance,
        "history": []
    }
    result = users_collection.insert_one(user)
    print(f"User added with ID: {result.inserted_id}")

def display_user_details(number_plate):
    """Display user details."""
    user = users_collection.find_one({"number_plate": number_plate})
    if not user:
        print("User with this number plate not found.")
        return

    print("\nUser Details:")
    print(f"Name: {user['user_name']}")
    print(f"Number Plate: {user['number_plate']}")
    print(f"Mobile Number: {user['mobile_number']}")
    print(f"Wallet Balance: {user['wallet_balance']}")

# Example usage
if __name__ == "__main__":
    # Add a new user
    add_user("Lucifer", "JA62UAR", "9856743210", 1000)

