
import os
print('a', os.getcwd())
# import v8_model
from process.yolo import v8_model
import cv2


def count(dict_input):     # {'IP': [username, password], 'IP2': [usr2, pass2]}
    count=[]
    for key, value in dict_input.items():  

        cap = cv2.VideoCapture("rtsp://"+str(value[0])+":"+str(value[1])+"@"+str(key))

        ret, frame = cap.read()

        if not ret:
            print("Frame Ended...")
            break

        student_count = v8_model.model(frame)
        count.append(student_count)
    
    return count

def main():
    print("Main from dict_in_list_out")

if __name__=="__main__":
    print(count({'172.16.102.200': ['admin', 'rms@12345']}))
    main()