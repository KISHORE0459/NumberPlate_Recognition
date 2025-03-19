from datetime import datetime


print(datetime.now())

# import torch
# import easyocr
# import cv2
# import matplotlib.pyplot as plt

# # Load YOLOv5 model
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='D:/yolov8-license-plate-detection-pytorch-overall-best-and-last-epoch-models-v1/best.pt', force_reload=True)

# # Load image
# img_path = 'c:/Users/Mohandinesh.D/Downloads/car1.jpg'
# img = cv2.imread(img_path)

# # Perform detection
# results = model(img)

# # Display the detected results
# results.show()

# # Get the bounding box of the detected license plate
# for result in results.xyxy[0]:  # results.xyxy contains bounding boxes (xmin, ymin, xmax, ymax)
#     xmin, ymin, xmax, ymax, conf, cls = result
#     # Crop the detected license plate from the image
#     cropped_img = img[int(ymin):int(ymax), int(xmin):int(xmax)]

#     # Use EasyOCR to extract text
#     reader = easyocr.Reader(['en'])
#     text = reader.readtext(cropped_img)

#     # Print extracted text
#     for (bbox, plate_text, prob) in text:
#         print(f"Detected Number Plate Text: {plate_text}")

# # Optionally display the cropped image
# plt.imshow(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
# plt.show()
