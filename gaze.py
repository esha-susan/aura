# import cv2
# import numpy as np
# import mediapipe as mp

# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh(
#     max_num_faces=1,
#     refine_landmarks=True,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5
# )

# LEFT_IRIS = [474, 475, 476, 477]
# RIGHT_IRIS = [469, 470, 471, 472]
# LEFT_EYE = [33, 133]
# RIGHT_EYE = [362, 263]

# def eye_center(landmarks, indices, w, h):
#     points = np.array([[landmarks[i].x * w, landmarks[i].y * h] for i in indices])
#     return np.mean(points, axis=0).astype(int)

# def check_gaze(landmarks, w, h, frame=None, draw=True):
#     try:
#         left_center = eye_center(landmarks, LEFT_IRIS, w, h)
#         right_center = eye_center(landmarks, RIGHT_IRIS, w, h)

#         left_outer = np.array([landmarks[33].x * w, landmarks[33].y * h])
#         left_inner = np.array([landmarks[133].x * w, landmarks[133].y * h])
#         right_outer = np.array([landmarks[362].x * w, landmarks[362].y * h])
#         right_inner = np.array([landmarks[263].x * w, landmarks[263].y * h])

#         # Compute horizontal ratios for both eyes
#         left_ratio = (left_center[0] - left_outer[0]) / (left_inner[0] - left_outer[0])
#         right_ratio = (right_center[0] - right_outer[0]) / (right_inner[0] - right_outer[0])
#         avg_ratio = (left_ratio + right_ratio) / 2

#         # Interpret direction
#         if avg_ratio < 0.35:
#             direction = "Looking right"
#         elif avg_ratio > 0.52:
#             direction = "Looking left"
#         else:
#             direction = "Looking Center"

#         # Draw landmarks & direction text if needed
#         if draw and frame is not None:
#             cv2.circle(frame, tuple(left_center), 2, (0, 255, 0), -1)
#             cv2.circle(frame, tuple(right_center), 2, (0, 255, 0), -1)
#             cv2.putText(frame, direction, (50, 100),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#         return direction
#     except:
#         return "No Face"
