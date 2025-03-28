from ultralytics import YOLO
import easyocr
import cv2
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from pymongo import MongoClient
from datetime import datetime
from shortestpath import find_shortest_path

CONNECTION_STRING = "mongodb+srv://kishorebabu200409:kishore26@cluster0.hf4t5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(CONNECTION_STRING)
db = client['number_plate_recognition']
users_collection = db['user']
user_entry = db['entry']

model = YOLO('d:/yolov8-license-plate-detection-pytorch-overall-best-and-last-epoch-models-v1/best.pt')
reader = easyocr.Reader(['en'])
plate_pattern = re.compile(r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$')

def is_valid_plate(plate_text):
    return bool(plate_pattern.match(plate_text))

def user_entry_process(number_plate):
    number_plate = number_plate.upper()
    user = users_collection.find_one({"number_plate": number_plate})
    if user:
        time = datetime.now()
        user["EnterTime"] = time
        if user_entry.find_one({"number_plate": number_plate}):
            print("User Already Entered!")
            return True
        else:
            path, nearest_free_space = find_shortest_path()
            user["allocated Space"] = nearest_free_space
            user_entry.insert_one(user)
            users_collection.find_one_and_update(
                {"number_plate": number_plate},
                {"$push": {"history": {"enter": time}}},
                return_document=True
            )
            print("User Entry Recorded.")
            return True
        
def new_user_entry(number_plate):
    number_plate = number_plate.upper()
    user = users_collection.find_one({"number_plate": number_plate})
    time = datetime.now()
    if user:
        user["EnterTime"] = time
        if user_entry.find_one({"number_plate": number_plate}):
            print("User Already Entered!")
        else:
            path, nearest_free_space = find_shortest_path()
            user["allocated Space"] = nearest_free_space
            user_entry.insert_one(user)
            users_collection.find_one_and_update(
                {"number_plate": number_plate},
                {"$push": {"history": {"enter": time}}},
                return_document=True
            )
            print("User Entry Recorded.")
            return
    else:
        path, nearest_free_space = find_shortest_path()
        user = {
            "number_plate": number_plate,
            "EnterTime": time,
            "allocated Space": nearest_free_space,
        }
        user_entry.insert_one(user)


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

detected_plates = []
plt.ion()
fig, ax = plt.subplots()
while len(detected_plates) < 20:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    results = model(frame)
    for result in results[0].boxes:
        box = result.xyxy[0]
        xmin, ymin, xmax, ymax = map(int, box[:4])
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        cropped_img = frame[ymin:ymax, xmin:xmax]
        if cropped_img.size == 0:
            continue

        gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = reader.readtext(thresh)

        for item in text:
            plate_text = item[1].replace(" ", "").upper()
            detected_plates.append(plate_text)
            is_entered = user_entry_process(plate_text)
            if(is_entered):
                cap.release()
                cv2.destroyAllWindows()
            print(f"Detected Plate: {plate_text}")

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    ax.clear()
    ax.imshow(frame_rgb)
    ax.axis('off')
    plt.pause(0.01)

most_frequent_plate = Counter(detected_plates).most_common(1)
if most_frequent_plate:
    final_plate = most_frequent_plate[0][0]
    print(f"🏆 Most Frequent Number Plate: {final_plate}")
    new_user_entry(final_plate)
else:
    print("No valid number plates detected.")
