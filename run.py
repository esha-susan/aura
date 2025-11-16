import cv2
import threading
import time
from playsound import playsound
from detector import detect_face
from attention import check_head_status,check_eye_status
from utils import get_head_status,get_eye_status,get_attention_level
#from gaze import check_gaze

#--------------------main body---------------------------------------

def main():
    cv2.namedWindow("AURA")
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        rval, frame = cap.read()
        
    else:
        rval = False
        print("Error! Couldn't open the webcam")


#------------------variables------------------------  
    eyes_closed_start = None
    alarm_on=False
    smooth_score = 100
    attention_percent = 0.0
#----------------------------------------------------


    while rval:
        frame=cv2.flip(frame,1)
        frame, landmarks = detect_face(frame)
        if landmarks:
            head_status=get_head_status(landmarks,frame.shape)
            cv2.putText(frame, head_status, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0) if head_status == "Attentive" else (0, 0, 255), 2)
            
           
            avg_ear, eyes_closed_start, alarm_on, alert_text = get_eye_status(
                landmarks.landmark, frame.shape, eyes_closed_start, alarm_on
            )

            if alert_text:
                cv2.putText(frame, alert_text, (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # gaze_status = check_gaze(landmarks.landmark, frame.shape[1], frame.shape[0])
            # cv2.putText(frame, gaze_status, (30, 90),
            # cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            # LEFT_EYE = [33, 160, 158, 133, 153, 144]
            # RIGHT_EYE = [362, 385, 387, 263, 373, 380]

            # left_eye_status = check_eye_status(landmarks.landmark,LEFT_EYE ,frame.shape[1], frame.shape[0])
            # right_eye_status = check_eye_status(landmarks.landmark,RIGHT_EYE ,frame.shape[1], frame.shape[0])
            # avg_ear=(left_eye_status+right_eye_status)/2.0
            
            # if avg_ear < EAR_THRESHOLD:
            #     eye_score=0.0
            #     if eyes_closed_start is None:
            #         eyes_closed_start = time.time()  # start the timer
                
            #     if time.time() - eyes_closed_start >= EYES_CLOSED_SECONDS:
                    
            #         if not alarm_on:
            #             threading.Thread(target=playsound("fifths.wav"),daemon=True).start()
            #             alarm_on=True
            #         cv2.putText(frame, "Don't sleep!", (30, 90),
            #                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # else:
            #     eye_score=1.0
            #     eyes_closed_start = None  
            #     alarm_on=False
            attention_percent=get_attention_level(landmarks,avg_ear,frame)
                        # ------------------ DISPLAY ------------------
            cv2.putText(frame, f"Attention: {attention_percent:.1f}",
                        (30, 130),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (255, 255, 0), 2)

            

        cv2.imshow("AURA", frame)
        rval, frame = cap.read()
        key = cv2.waitKey(20)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
