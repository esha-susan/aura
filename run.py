import cv2
from detector import detect_face

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
        
        cv2.imshow("AURA",frame)
        rval,frame=cap.read()
        key=cv2.waitKey(20)
        if key==27:
            break
    cv2.destroyWindow("AURA")
    cap.release()

if __name__=="__main__":
    main()