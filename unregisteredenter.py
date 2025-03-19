from ultralytics import YOLO
import easyocr
import cv2
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Load YOLOv8 model
model = YOLO('d:/yolov8-license-plate-detection-pytorch-overall-best-and-last-epoch-models-v1/best.pt')

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Regular expression for validating number plates (e.g., AB12CD3456)
plate_pattern = re.compile(r'^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$')

def is_valid_plate(plate_text):
    """Check if the detected number plate matches the required format."""
    return bool(plate_pattern.match(plate_text))

# Open a connection to the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

valid_plates = []  # Store valid number plates
detected_plates = []  # Store all detected plates for frequency analysis
plt.ion()
fig, ax = plt.subplots()

while len(valid_plates) < 10:  # Collect 10 valid plates
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Perform detection
    results = model(frame)

    for result in results[0].boxes:
        box = result.xyxy[0]
        xmin, ymin, xmax, ymax = map(int, box[:4])
        
        # Draw bounding box
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        
        # Crop and process the detected license plate
        cropped_img = frame[ymin:ymax, xmin:xmax]
        if cropped_img.size == 0:
            continue  # Skip if no valid crop
        
        # Preprocess the cropped image for better OCR results
        gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Use EasyOCR to extract text
        text = reader.readtext(thresh)
        
        for item in text:
            plate_text = item[1].replace(" ", "").upper()
            detected_plates.append(plate_text)
            print(f"Detected Plate: {plate_text}")
            
            if is_valid_plate(plate_text):
                valid_plates.append(plate_text)
                print(f"✅ Valid Plate: {plate_text}")
                cv2.putText(frame, plate_text, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            else:
                print(f"❌ Invalid Plate: {plate_text}")

    # Display frame using Matplotlib
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    ax.clear()
    ax.imshow(frame_rgb)
    ax.axis('off')
    plt.pause(0.01)

    if len(valid_plates) >= 10:
        break

plt.ioff()
plt.show()

# Determine the most frequent number plate
most_frequent_plate = Counter(detected_plates).most_common(1)
if most_frequent_plate:
    print(f"🏆 Most Frequent Number Plate: {most_frequent_plate[0][0]}")
else:
    print("No valid number plates detected.")

# Cleanup
cap.release()
cv2.destroyAllWindows()