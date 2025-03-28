# from ultralytics import YOLO
# import easyocr
# import cv2
# import matplotlib.pyplot as plt
# from pymongo import MongoClient

# # MongoDB connection setup
# client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string if needed
# db = client["NP_Rec"]  # The database name
# collection = db["users"]  # Collection where user details are stored

# # Load YOLOv8 model
# model = YOLO('D:/yolov8-license-plate-detection-pytorch-overall-best-and-last-epoch-models-v1/best.pt')

# # Load image
# img_path = 'images/car3.jpg'
# img = cv2.imread(img_path)

# # Perform detection
# results = model(img)

# # Display the detected results
# img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# # Get the bounding box of the detected license plate
# for result in results[0].boxes:
#     box = result.xyxy[0]  # Get box coordinates
#     xmin, ymin, xmax, ymax = map(int, box[:4])  # Convert to integers

#     # Crop the detected license plate from the image
#     cropped_img = img[ymin:ymax, xmin:xmax]

#     # Use EasyOCR to extract text
#     reader = easyocr.Reader(['en'])
#     text = reader.readtext(cropped_img)

#     # Print and check extracted text
#     for (bbox, plate_text, prob) in text:
#         print(f"Detected Number Plate Text: {plate_text}")

#         # Check if the number plate already exists in the 'users' collection
#         existing_user = collection.find_one({"licence_number": plate_text})
#         if existing_user:
#             print("License plate found in database.")
#             print(f"User Info: \nName: {existing_user['name']}\nAge: {existing_user['age']}\n"
#                   f"Mobile Number: {existing_user['mobile_number']}\nWallet Balance: {existing_user['wallet_balance']}")
#         else:
#             print(f"Number Plate '{plate_text}' not found in the database.")

#     # Optionally display the cropped image
#     plt.imshow(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
#     plt.show()

# import shutil

# # Example usage
# shutil.rmtree('your_directory', onerror=handler)

from ultralytics import YOLO
import easyocr
import cv2
import matplotlib.pyplot as plt

# Load YOLOv8 model
model = YOLO('d:/yolov8-license-plate-detection-pytorch-overall-best-and-last-epoch-models-v1/best.pt')

# Load image
img_path = 'images/car10.jpg'
img = cv2.imread(img_path)

# Perform detection
results = model(img)

# Display the detected results
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Get the bounding box of the detected license plate
for result in results[0].boxes:
    box = result.xyxy[0]  # Get box coordinates
    xmin, ymin, xmax, ymax = map(int, box[:4])  # Convert to integers
    
    # Crop the detected license plate from the image
    cropped_img = img[ymin:ymax, xmin:xmax]

    # Use EasyOCR to extract text
    reader = easyocr.Reader(['en'])
    text = reader.readtext(cropped_img)

    # Print extracted text
    for (bbox, plate_text, prob) in text:
        print(f"Detected Number Plate Text: {plate_text}")

    # Optionally display the cropped image
    plt.imshow(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
    plt.show()

