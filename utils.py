import cv2
import time
import threading
from playsound  import playsound
from attention import check_eye_status
from attention import check_head_status

#------variables-------
EAR_THRESHOLD=0.23
EYES_CLOSED_SECONDS=5
#_---------------------


from attention import check_eye_status
def get_eye_status(landmarks,frame_shape,eyes_closed_start,alarm_on):
            LEFT_EYE = [33, 160, 158, 133, 153, 144]
            RIGHT_EYE = [362, 385, 387, 263, 373, 380]

            left_eye_status = check_eye_status(landmarks,LEFT_EYE ,frame_shape[1], frame_shape[0])
            right_eye_status = check_eye_status(landmarks,RIGHT_EYE ,frame_shape[1], frame_shape[0])
            avg_ear=(left_eye_status+right_eye_status)/2.0
            alert_text=""
            if avg_ear < EAR_THRESHOLD:
                eye_score=0.0
                if eyes_closed_start is None:
                    eyes_closed_start = time.time()  # start the timer
                
                if time.time() - eyes_closed_start >= EYES_CLOSED_SECONDS:
                    
                    if not alarm_on:
                        threading.Thread(target=playsound("fifths.wav"),daemon=True).start()
                        alarm_on=True
                    alert_text="Dot Sleep"
                   
            else:
                eye_score=1.0
                eyes_closed_start = None  
                alarm_on=False
            return avg_ear,eyes_closed_start,alarm_on,alert_text


def get_head_status(landmarks,frame_shape):
            head_status = check_head_status(landmarks, frame_shape[1], frame_shape[0])
            if head_status=="Attentive":
                att_score=1.0
            else:
                att_score=0.0
            return head_status
            
def get_attention_level(landmarks,avg_ear,frame):
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
            return attention_percent
