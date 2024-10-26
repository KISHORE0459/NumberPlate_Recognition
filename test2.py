
# # import torch
# # import cv2
# # import easyocr
# # import numpy as np
# # import matplotlib.pyplot as plt
# # from ultralytics import YOLO

# # # Load YOLO model
# # model = YOLO('yolov5s.pt')

# # # Load image
# # image_path = 'c:/Users/Mohandinesh.D/Downloads/car1.jpg'  # Path to your car image
# # image = cv2.imread(image_path)

# # # Perform detection
# # results = model(image)
# # detected_objects = results[0].boxes.xyxy
# # class_ids = results[0].boxes.cls

# # # Assuming plates are detected manually or using custom-trained YOLO
# # detected_plates = []

# # # Filter out bounding boxes (manual filtering can be used here)
# # for i, box in enumerate(detected_objects):
# #     x1, y1, x2, y2 = map(int, box)
# #     cropped_plate = image[y1:y2, x1:x2]
# #     detected_plates.append(cropped_plate)
# #     cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# # plt.show()

# # # Initialize EasyOCR
# # reader = easyocr.Reader(['en'])

# # # Recognize text from detected plates
# # for plate in detected_plates:
# #     plate_text = reader.readtext(plate)
    
# #     for (bbox, text, prob) in plate_text:
# #         print(f"Detected text: {text} with confidence {prob:.4f}")
        
# #     plt.imshow(cv2.cvtColor(plate, cv2.COLOR_BGR2RGB))
# #     plt.show()

# from ultralytics import YOLO
# import torch
# import cv2
# import easyocr
# import numpy as np
# import matplotlib.pyplot as plt

# # Load YOLO model (YOLOv5 in this case)
# # model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  # Use your trained model path
# # model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
# model = YOLO('D:/yolov8-license-plate-detection-pytorch-overall-best-and-last-epoch-models-v1/best.pt')

# # Initialize EasyOCR reader
# reader = easyocr.Reader(['en'])

# # Load image
# image_path = 'C:/Users/Mohandinesh.D/Downloads/car6.jpg'
# img = cv2.imread(image_path)

# # Run YOLOv5 inference on the image
# results = model(img)

# # Get the bounding box coordinates for detected plates
# detections = results.xyxy[0]  # get the detection details
# for detection in detections:
#     x_min, y_min, x_max, y_max, confidence, class_id = detection

#     # Convert coordinates to integers
#     x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])

#     # Crop the detected number plate from the image
#     cropped_img = img[y_min:y_max, x_min:x_max]

#     # Display the cropped number plate image
#     plt.imshow(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
#     plt.title("Detected Number Plate")
#     plt.show()

#     # Use EasyOCR to extract text from the cropped image
#     ocr_result = reader.readtext(cropped_img)

#     # Print the detected text (number plate)
#     print("Detected Number Plate Text:")
#     for result in ocr_result:
#         print(result[1])

