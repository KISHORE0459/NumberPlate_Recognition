from ultralytics import YOLO
import easyocr
import cv2
import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime
from shortestpath import find_shortest_path;
CONNECTION_STRING = "mongodb+srv://kishorebabu200409:kishore26@cluster0.hf4t5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB Atlas
client = MongoClient(CONNECTION_STRING)
db = client['number_plate_recognition']  # Updated database name
users_collection = db['user']  # Updated collection name
user_entry = db['entry']


# adding user to the enter collection that store the user details when they enter

def UserEntry(number_plate):
    print(number_plate)
    user = users_collection.find_one({"number_plate" : number_plate})
    if user:
        time = datetime.now()
        print(time)
        user["EnterTime"] = time
        print(user)
        np = user["number_plate"]
        print(np)
        if(user_entry.find_one({"number_plate":np})):
            print("User Alreafy Entered !")
        else:
            path, nearest_free_space = find_shortest_path()
            user["allocated Space"] = nearest_free_space
            user_entry.insert_one(user)
            result = users_collection.find_one_and_update(
                    {"number_plate": number_plate},
                    {"$push": {"history": {"enter" : time}}},
                    return_document=True
                    )
            print(result)
            


#recogonize the number plate of the user when they leave


#display the user details when the number plate is recognized

def display_user_details(number_plate):
    """Display user details."""
    number_plate = number_plate.upper()
    user = users_collection.find_one({"number_plate": number_plate})
    if user:
        print("\nUser Details:")
        print(f"Name: {user['user_name']}")
        print(f"Number Plate: {user['number_plate']}")
        print(f"Mobile Number: {user['mobile_number']}")
        print(f"Wallet Balance: {user['wallet_balance']}")
        UserEntry(number_plate)
        return 0
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
            print(f"Detected Number Plate Text: {plate_text.replace(' ','')}")
            display_user_details(plate_text.replace(' ',''))

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
