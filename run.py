import cv2
from detector import detect_face
from attention import check_attention
def main():
    cv2.namedWindow("AURA")
    cap=cv2.VideoCapture(0)

    if cap.isOpened():
        rval,frame=cap.read()
    else:
        rval=False
        print("Error! Couldn't open the webcam")


    while rval:
        frame,landmarks=detect_face(frame)
        if landmarks:
            attention_status=check_attention(landmarks.landmark,frame.shape[1],frame.shape[0])
            cv2.putText(frame, attention_status, (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0) if attention_status == "Attentive" else (0, 0, 255), 2)
        cv2.imshow("AURA",frame)
        rval,frame=cap.read()
        key=cv2.waitKey(20)
        if key==27:
            break
    cv2.destroyWindow("AURA")
    cap.release()

if __name__=="__main__":
    main()