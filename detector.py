import mediapipe as mp
import cv2

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,  # enables iris landmarks
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


def detect_face(frame):
    rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=face_mesh.process(rgb_frame)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing=mp.solutions.drawing_utils
            mp_drawing.draw_landmarks(
                frame,
                face_landmarks,
                mp_face_mesh.FACEMESH_TESSELATION,
                
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0),thickness=1,circle_radius=0)
            )
        return frame,results.multi_face_landmarks[0]
    return frame,None