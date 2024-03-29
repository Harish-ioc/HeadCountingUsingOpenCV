# %pip install ultralytics
import cv2
import numpy as np
from ultralytics import YOLO
import pandas as pd

hemang = YOLO('process/yolo/best (50).pt')
my_file = open("process/yolo/coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

def calculate_overlap(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    overlap_x = max(0, min(x1 + w1, x2 + w2) - max(x1, x2))
    overlap_y = max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
    overlap_area = overlap_x * overlap_y
    area_box1 = w1 * h1
    area_box2 = w2 * h2
    overlap_ratio = overlap_area / max(area_box1, area_box2)
    return overlap_ratio

def model(frame):
    frame = cv2.resize(frame, (1080, 920))
    results = hemang.predict(frame)
    a = results[0].boxes.data.cpu().numpy()
    px = pd.DataFrame(a).astype("float")
    students_count = 0
    drawn_boxes = []

    for i in range(len(px)):
        x1, y1, w1, h1, _, d = map(int, px.iloc[i][:6])
        c = class_list[d]

        if 'person' in c:
            is_inside = False

            for box in drawn_boxes:
                overlap_ratio = calculate_overlap((x1, y1, w1, h1), box)

                if overlap_ratio > 0.8:
                    is_inside = True
                    break

            if not is_inside:
                cv2.rectangle(frame, (x1, y1), (x1 + 75, y1 + 75), (0, 0, 255), 2)
                cv2.putText(frame, "Student", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                students_count += 1
                drawn_boxes.append((x1, y1, w1, h1))

    # cv2.putText(frame, f'Students Count: {students_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # cv2.imshow("YOLOv8 Student Counting", frame)

    return students_count

def main():
    print("Main from Model")

if __name__ == "__main__":
    main()
    