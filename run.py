import cv2

from detector import detect_face
from attention import check_attention
#from gaze import check_gaze
from attention import check_eye_status
import time
from playsound import playsound
import threading

EAR_THRESHOLD=0.23
EYES_CLOSED_SECONDS = 5.0  

def main():
    cv2.namedWindow("AURA")
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        rval, frame = cap.read()
        
    else:
        rval = False
        print("Error! Couldn't open the webcam")



     #----variables---   
    eyes_closed_start = None
    alarm_on=False
    smooth_score = 100
    attention_percent = 0.0

    #---------------------


    while rval:
        frame=cv2.flip(frame,1)
        frame, landmarks = detect_face(frame)
        if landmarks:
            attention_status = check_attention(landmarks.landmark, frame.shape[1], frame.shape[0])
            if attention_status=="Attentive":
                att_score=1.0
            else:
                att_score=0.0
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
                eye_score=0.0
                if eyes_closed_start is None:
                    eyes_closed_start = time.time()  # start the timer
                
                if time.time() - eyes_closed_start >= EYES_CLOSED_SECONDS:
                    
                    if not alarm_on:
                        threading.Thread(target=playsound("fifths.wav"),daemon=True).start()
                        alarm_on=True
                    cv2.putText(frame, "Don't sleep!", (30, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                eye_score=1.0
                eyes_closed_start = None  
                alarm_on=False
           
            cv2.putText(frame, f"Attention: {attention_percent:.1f}",
                (30, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255,255,0), 2)


            cv2.putText(frame, attention_status, (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0) if attention_status == "Attentive" else (0, 0, 255), 2)
                        # ------------------ HEAD PRESENCE (Face size in frame) ------------------
            xs = [lm.x for lm in landmarks.landmark]
            ys = [lm.y for lm in landmarks.landmark]

            box_area = (max(xs) - min(xs)) * (max(ys) - min(ys))  
            # 0.18 = average face size (you can tune)
            head_presence = min(1.0, box_area / 0.18)


            # ------------------ EYE OPENNESS ------------------
            eye_openness = 1.0 if avg_ear > EAR_THRESHOLD else 0.0

            # --- HEAD ORIENTATION (STRONGER DROP) ---
            nose = landmarks.landmark[1]

            xs = [lm.x for lm in landmarks.landmark]
            face_left  = min(xs)
            face_right = max(xs)
            face_center = (face_left + face_right) / 2

            offset = abs(nose.x - face_center)

            face_width = face_right - face_left
            normalized_offset = offset / (face_width / 2)

            # aggressive drop-off curve
            head_orientation = 1.0 - (normalized_offset ** 2) * 2.5
            head_orientation = max(0.0, min(1.0, head_orientation))


            # Normalize → more than 0.12 means looking far right/left
            head_orientation = max(0.0, 1.0 - (offset / 0.12))


            # ------------------ FINAL ATTENTION SCORE ------------------
            attention_score = (
                0.4 * head_presence +
                0.3 * eye_openness +
                0.3 * head_orientation
            )

            attention_percent = max(0, min(100, attention_score * 100))

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
