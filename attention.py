import numpy as npy


def check_attention(landmarks,frame_width,frame_height):
    nose=landmarks[1]
    nose_x=nose.x*frame_width
    nose_y=nose.y*frame_height
    
    #attention logic
    left_x_threshold=0.4*frame_width
    right_x_threshold=0.6*frame_width
    top_y_threshold = 0.36 * frame_height
    bottom_y_threshold = 0.65 * frame_height

    if left_x_threshold<nose_x<right_x_threshold and top_y_threshold<nose_y<bottom_y_threshold:
        return "Attentive"
    else:
        return "Distracted"
    
def check_eye_status(landmarks,eye_indices,frame_width,frame_height):

    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]
    
    pt=((landmarks[i].x*frame_width,landmarks[i].y*frame_height)  for i in  eye_indices)
    pts=list(pt)
    
    p1, p2, p3, p4, p5, p6 = pts

    a = npy.linalg.norm(npy.array(p2) - npy.array(p6))
    b = npy.linalg.norm(npy.array(p3) - npy.array(p5))
    c = npy.linalg.norm(npy.array(p1) - npy.array(p4))
    EAR = (a + b) / (2.0 * c)
    return EAR