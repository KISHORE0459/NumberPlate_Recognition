from ultralytics import YOLO
import easyocr
import cv2
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime

CONNECTION_STRING = "mongodb+srv://kishorebabu200409:kishore26@cluster0.hf4t5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(CONNECTION_STRING)
db = client['number_plate_recognition']  # Updated database name
users_collection = db['user']  # Updated collection name
user_entry = db['entry']
user_exit = db['exit']

# Calculate the time duration and parking cost, and update the wallet balance
def calculate_parking_cost(entry_time, exit_time):
    # entry_time = datetime.strptime(entry_time, "%H:%M:%S")
    # exit_time = datetime.strptime(exit_time, "%H:%M:%S")
    duration = (exit_time - entry_time).total_seconds() // 60  # Duration in minutes
    cost = duration * 1  # Rs.1 per minute
    return duration, cost

# Adding user to the exit collection that stores the user details when they exit and removing them from the entry collection
def UserExit(number_plate):
    user = users_collection.find_one({"number_plate": number_plate})
    if user:
        exit_time = datetime.now()
        print("Exit Time:", exit_time)
        
        # Retrieve entry time from the user entry collection
        entry_record = user_entry.find_one({"number_plate": number_plate})
        if entry_record:
            entry_time = entry_record.get("EnterTime")
            duration, cost = calculate_parking_cost(entry_time, exit_time)
            print(f"Parking Duration: {duration} minutes")
            print(f"Parking Cost: Rs.{cost}")

            # Deduct the cost from the user's wallet balance
            wallet_balance = user['wallet_balance'] - cost
            user['wallet_balance'] = wallet_balance
            user['ExitTime'] = exit_time

            # Update the user's history with the enter and exit time pair
            history_entry = {"enter": entry_time, "exit": exit_time}
            result = users_collection.find_one_and_update(
                {"number_plate": number_plate},
                {
                    "$push": {"history": history_entry},
                    "$set": {"wallet_balance": wallet_balance}
                },
                return_document=True
            )
            
            # Remove the '_id' field from the user document before inserting it into the exit collection
            user.pop('_id')
            user_exit.insert_one(user)
            user_entry.delete_one({"number_plate": number_plate})

            print("Updated User Details:", result)
        else:
            print("No entry record found for this user.")
    else:
        print("No User Found")

# Load YOLOv8 model
model = YOLO('d:/yolov8-license-plate-detection-pytorch-overall-best-and-last-epoch-models-v1/best.pt')

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Open a connection to the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera or replace with the camera index

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Process each frame from the camera feed
plt.ion()  # Turn on interactive mode for matplotlib
fig, ax = plt.subplots()
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Perform detection
    results = model(frame)

    # Draw bounding boxes and extract license plate text
    for result in results[0].boxes:
        box = result.xyxy[0]  # Get box coordinates
        xmin, ymin, xmax, ymax = map(int, box[:4])  # Convert to integers

        # Draw the bounding box on the frame
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        # Crop the detected license plate from the frame
        cropped_img = frame[ymin:ymax, xmin:xmax]

        # Use EasyOCR to extract text
        text = reader.readtext(cropped_img)
        for (bbox, plate_text, prob) in text:
            # Display the detected text on the frame
            cv2.putText(frame, plate_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print(f"Detected Number Plate Text: {plate_text.replace(' ', '')}")
            
            UserExit(plate_text.replace(' ', ''))

    # Convert the frame to RGB (OpenCV uses BGR by default)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the frame using matplotlib
    ax.clear()
    ax.imshow(frame_rgb)
    ax.axis('off')  # Turn off axis labels
    plt.pause(0.001)  # Small pause to allow for updates

    # Check for 'q' key press to exit the loop
    if plt.waitforbuttonpress(timeout=0.01):
        break

# Release the camera and close all windows
cap.release()
plt.close()
