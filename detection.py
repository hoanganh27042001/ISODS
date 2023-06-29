import cv2
import numpy as np
import json

# Path to input video clip
input_video = 'Intersection.mp4'

# Load YOLOv3 pre-trained weights and configuration
net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')

# Load class labels
with open('coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Set threshold values for confidence and non-maximum suppression
confidence_threshold = 0.5
nms_threshold = 0.4

# Open the video clip
video = cv2.VideoCapture(input_video)
frame_count = 0
detections = []

while True:
    # Read the next frame from the video
    ret, frame = video.read()
    if not ret:
        break

    # Create a blob from the frame and perform forward pass
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers)

    # Initialize lists to store detection results
    boxes = []
    confidences = []
    class_ids = []

    # Iterate over each output layer and detect objects
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > confidence_threshold:
                # Scale the bounding box coordinates to the original frame size
                box = detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                x_center, y_center, width, height = box.astype('int')

                # Calculate top-left coordinates of the bounding box
                x = int(x_center - (width / 2))
                y = int(y_center - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Perform non-maximum suppression to eliminate redundant detections
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nms_threshold)
    # print(type(indices))
    print(indices)

    # Process each detected object
    for i in indices:
        i = i.item()
        class_id = class_ids[i]
        class_name = classes[class_id]
        confidence = confidences[i]
        x, y, width, height = boxes[i]

        # Save detection information
        detection_info = {
            'FrameID': frame_count,
            'Class': class_name,
            'BoundingBox': [x, y, width, height],
            'Confidence': confidence
        }
        detections.append(detection_info)

    frame_count += 1

# Release the video object
video.release()

# Save detections as JSON file
output_json = 'detections.json'
with open(output_json, 'w') as f:
    json.dump(detections, f)

print('Detection information saved as', output_json)
