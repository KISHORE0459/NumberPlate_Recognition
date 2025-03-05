from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  
# MongoDB Atlas connection
MONGO_URI = "mongodb+srv://kishorebabu200409:kishore26@cluster0.hf4t5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Replace with your connection string
client = MongoClient(MONGO_URI)
db = client["number_plate_recognition"]  # Replace with your database name
users = db["user"]  # Replace with your collection name
entries = db['entry']
exit = db['exit']
space = db['parkingspace']

@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        userdata = list(users.find({}, {"_id": 0}))  # Exclude ObjectId from response
        return jsonify(userdata)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/users/name/<user_name>", methods=["GET"])
def get_users_by_name(user_name):
    try:
        userdata = list(users.find({'user_name' : user_name}, {"_id": 0}))  # Exclude ObjectId from response
        if(userdata):
            return jsonify(userdata)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

    
@app.route('/api/entries' , methods =["GET"])
def get_entries():
    try:
        entrydata = list(entries.find({} , {"_id" : 0}))
        return jsonify(entrydata);
    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    

@app.route('/api/exits' , methods =["GET"])
def get_exits():
    try:
        exitdata = list(exit.find({} , {"_id" : 0}))
        return jsonify(exitdata)
    except Exception as e:
        return jsonify({"error" : str(e)}), 500
    

@app.route('/api/path' , methods =["GET"])
def get_path():
    try:
        exitdata = list(space.find({} , {"_id" : 0}))
        return jsonify(exitdata)
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
