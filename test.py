from flask import render_template, Flask,  request, Response, jsonify, session
import cv2
import requests
import serial # 
import torch
from ultralytics import YOLO  # Import YOLO directly

# ... other imports (MySQL, etc.)

ESP8266_IP = "172.18.72.25"
ESP_PORT = 8080

# Load the YOLO model (assuming 'best.pt' is in the same directory)
model = YOLO('best.pt')  # Removed the 'detect' function from yolov5

def gen_frames():
  cap = cv2.VideoCapture(0)  # Use camera index 0 for default webcam
  while True:
    success, frame = cap.read()
    if not success:
      break
      
    # Perform inference using YOLO model
    results = model(frame)
    
    # Process results (extract labels, confidences)
    labels = results.pandas().xyxy[0]['name'].tolist()
    confidences = results.pandas().xyxy[0]['confidence'].tolist()
    
    if confidences:
        global label  # Assuming 'label' is used elsewhere in your code
        max_conf_idx = confidences.index(max(confidences))
        label = str(labels[max_conf_idx])
    
    # Encode frame as JPEG
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    
    yield (b'--frame\r\n'
           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
           
# ... other routes (login, register, handle_command)

@app.route('/video_feed/')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
  app.run(debug=True)
