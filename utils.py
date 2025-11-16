# import cv2
# import time
# import threading
# from playsound  import playsound

# #------variables-------
# EAR_THRESHOLD=0.23
# EYES_CLOSED_SECONDS=5
# #_---------------------

# from attention import check_eye_status
# def get_eye_status(landmarks,frame_shape,eyes_closed_start,alarm_on):
#             LEFT_EYE = [33, 160, 158, 133, 153, 144]
#             RIGHT_EYE = [362, 385, 387, 263, 373, 380]

#             left_eye_status = check_eye_status(landmarks.landmark,LEFT_EYE ,frame.shape[1], frame.shape[0])
#             right_eye_status = check_eye_status(landmarks.landmark,RIGHT_EYE ,frame.shape[1], frame.shape[0])
#             avg_ear=(left_eye_status+right_eye_status)/2.0
            
#             if avg_ear < EAR_THRESHOLD:
#                 eye_score=0.0
#                 if eyes_closed_start is None:
#                     eyes_closed_start = time.time()  # start the timer
                
#                 if time.time() - eyes_closed_start >= EYES_CLOSED_SECONDS:
                    
#                     if not alarm_on:
#                         threading.Thread(target=playsound("fifths.wav"),daemon=True).start()
#                         alarm_on=True
#                     alert_text="Dot Sleep"
                   
#             else:
#                 eye_score=1.0
#                 eyes_closed_start = None  
#                 alarm_on=False
#             return avg_ear,eyes_closed_start,alarm_on,alert_text