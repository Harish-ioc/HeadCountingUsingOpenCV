import cv2

# ls=[163]+list(range(165,178))
#163-177

# ls=list(range(131,163))
ls=[17]
#172.16.102.158
while True:
    for i in ls:
        video_source = "rtsp://admin:rms@12345@172.16.115."+str(i)
        print(i)

        text = str(i)
        position = (50, 50)  # Coordinates of the text (x, y)

        # Define font settings
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (255, 255, 255)  # White color in BGR
        thickness = 2

    
        # while True:
    try:
        cap = cv2.VideoCapture(video_source)
    except Exception as e:
        print(e)
        # break

    if not cap.isOpened():
        print("Error: Couldn't open the video source.")
        # break

    ret, frame = cap.read()

    if not ret:
        print("Video ended.")
        # break

    # cv2.imwrite("hiiii.png", frame)
    # cv2.putText(frame, text, position, font, font_scale, font_color, thickness)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
