import cv2
from ultralytics import YOLO

def getColors(cls_num):
    base_colors = [(255,0,0),(0,255,0),(0,0,255)]
    color_index = cls_num % len(base_colors)
    increments = [(1,-2,1),(-2,1,-1),(1,-1,-2)]
    color = [base_colors[color_index][i] + increments[color_index][i]* (cls_num // len(base_colors)) % 256 for i in range(3)]
    return tuple(color)

yolo = YOLO('yolov8n.pt')

video = cv2.VideoCapture(1)

while True:
    ret, frame = video.read()
    if not ret:
        continue

    results = yolo.track(frame, stream = True)
    for result in results:
        classes_names = result.names

        for box in result.boxes:
            if box.conf[0] > 0.1:
                [x1,x2, y1,y2] = box.xyxy[0]
                x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
                cls = int(box.cls[0])
                class_name = classes_names[cls]
                color = getColors(cls)
                cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
                cv2.putText(frame, f'{classes_names[int(box.cls[0])]} {box.conf[0]:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
