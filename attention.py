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