import cv2

from detector import detect_face
from attention import check_attention
#from gaze import check_gaze
from attention import check_eye_status
import time
from playsound import playsound

EAR_THRESHOLD=0.18
EYES_CLOSED_SECONDS = 10.0  

def main():
    cv2.namedWindow("AURA")
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        rval, frame = cap.read()
        
    else:
        rval = False
        print("Error! Couldn't open the webcam")
    eyes_closed_start = None
    while rval:
        frame=cv2.flip(frame,1)
        frame, landmarks = detect_face(frame)
        if landmarks:
            attention_status = check_attention(landmarks.landmark, frame.shape[1], frame.shape[0])
            cv2.putText(frame, attention_status, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0) if attention_status == "Attentive" else (0, 0, 255), 2)
            
            # gaze_status = check_gaze(landmarks.landmark, frame.shape[1], frame.shape[0])
            # cv2.putText(frame, gaze_status, (30, 90),
            # cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            LEFT_EYE = [33, 160, 158, 133, 153, 144]
            RIGHT_EYE = [362, 385, 387, 263, 373, 380]

            left_eye_status = check_eye_status(landmarks.landmark,LEFT_EYE ,frame.shape[1], frame.shape[0])
            right_eye_status = check_eye_status(landmarks.landmark,RIGHT_EYE ,frame.shape[1], frame.shape[0])
            avg_ear=(left_eye_status+right_eye_status)/2.0
                
            if avg_ear < EAR_THRESHOLD:
                if eyes_closed_start is None:
                    eyes_closed_start = time.time()  # start the timer
                
                if time.time() - eyes_closed_start >= EYES_CLOSED_SECONDS:
                    cv2.putText(frame, "Don't sleep!", (30, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                eyes_closed_start = None  


            cv2.putText(frame, attention_status, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0) if attention_status == "Attentive" else (0, 0, 255), 2)
            
        cv2.imshow("AURA", frame)
        rval, frame = cap.read()
        key = cv2.waitKey(20)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
