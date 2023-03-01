import mediapipe as mp
import cv2
import pickle
import math
import numpy as np
import pandas as pd
import warnings
#from gtts import gTTS
import os
import time
from asgiref.sync import async_to_sync
#from django.conf import settings
from asgiref.sync import async_to_sync
#from channels.layers import get_channel_layer
from django.http import HttpResponse
import pyttsx3

warnings.filterwarnings("ignore")

with open('../mediapipe/mid_poses.pkl', 'rb') as f:
    model = pickle.load(f)

mp_drawing = mp.solutions.drawing_utils  # Drawing helpers
mp_pose = mp.solutions.pose  # Mediapipe Solutions

landmark_names = [
        'nose',
        'left_eye_inner', 'left_eye', 'left_eye_outer',
        'right_eye_inner', 'right_eye', 'right_eye_outer',
        'left_ear', 'right_ear',
        'mouth_left', 'mouth_right',
        'left_shoulder', 'right_shoulder',
        'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist',
        'left_pinky_1', 'right_pinky_1',
        'left_index_1', 'right_index_1',
        'left_thumb_2', 'right_thumb_2',
        'left_hip', 'right_hip',
        'left_knee', 'right_knee',
        'left_ankle', 'right_ankle',
        'left_heel', 'right_heel',
        'left_foot_index', 'right_foot_index'
    ]

joints = [
    'left_elbow',
    'right_elbow',
    'right_shoulder',
    'left_shoulder',
    'left_knee',
    'right_knee',
    'head',
    'left_hip',
    'right_hip',
    'left_ankle',
    'right_ankle'
]

def tree_actual_angles():
    tree_pose_angles = {
        x+"_angle" : None for x in joints
    }


    tree_pose_angles['left_elbow_angle'] = 180
    tree_pose_angles['right_elbow_angle'] = 180
    tree_pose_angles['left_shoulder_angle'] = 180
    tree_pose_angles['right_shoulder_angle'] = 180
    tree_pose_angles['left_hip_angle'] = 180
    tree_pose_angles['right_hip_angle'] = 180

    return tree_pose_angles

def return_angle(landmark1, landmark2, landmark3):
    x1, y1 = landmark1.x, landmark1.y
    x2, y2 = landmark2.x, landmark2.y
    x3, y3 = landmark3.x, landmark3.y
    
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    if angle < 0:
        angle += 360
        
    # Return the calculated angle.
    return angle

def compute_joint_angles(pose):
    left_elbow_angle = return_angle(pose[landmark_names.index('left_wrist')], 
                                       pose[landmark_names.index('left_elbow')], 
                                       pose[landmark_names.index('left_shoulder')])
    right_elbow_angle = return_angle(pose[landmark_names.index('right_shoulder')], 
                                       pose[landmark_names.index('right_elbow')], 
                                       pose[landmark_names.index('right_wrist')])
    left_shoulder_angle = return_angle(pose[landmark_names.index('left_elbow')], 
                                       pose[landmark_names.index('left_shoulder')], 
                                       pose[landmark_names.index('left_hip')])
    right_shoulder_angle = return_angle(pose[landmark_names.index('right_hip')], 
                                        pose[landmark_names.index('right_shoulder')], 
                                        pose[landmark_names.index('right_elbow')])
    left_hip_angle = return_angle(pose[landmark_names.index('left_knee')], 
                                  pose[landmark_names.index('left_hip')], 
                                  pose[landmark_names.index('left_shoulder')])
    right_hip_angle = return_angle(pose[landmark_names.index('right_shoulder')], 
                                  pose[landmark_names.index('right_hip')], 
                                  pose[landmark_names.index('right_knee')])
    left_knee_angle = return_angle(pose[landmark_names.index('left_ankle')], 
                                  pose[landmark_names.index('left_knee')], 
                                  pose[landmark_names.index('left_hip')])
    right_knee_angle = return_angle(pose[landmark_names.index('right_hip')], 
                                  pose[landmark_names.index('right_knee')], 
                                  pose[landmark_names.index('right_ankle')])
    
    computed_angles = {'left_elbow_angle' : left_elbow_angle, 
                       'right_elbow_angle' :right_elbow_angle, 
                       'left_shoulder_angle' :left_shoulder_angle, 
                       'right_shoulder_angle' :right_shoulder_angle, 
                       'left_hip_angle' :left_hip_angle, 
                       'right_hip_angle' :right_hip_angle,
                       'left_knee_angle' :left_knee_angle, 
                       'right_knee_angle' :right_knee_angle}
    return computed_angles

def get_pose_prediction(pose):
    pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())                    
    X = pd.DataFrame([pose_row])
    pose_detection_class = model.predict(X)[0]
    pose_detection_probability = model.predict_proba(X)[0]
    return pose_detection_class, pose_detection_probability

def generate_errors(pose_name, pose):
    #calculate the angles
    tree_pose_angles = tree_actual_angles()
    actual_angles = compute_joint_angles(pose)
    max_diff = 0
    diff_joint = ""    
    if pose_name == "t":
        for angles in actual_angles.keys():
            
            if tree_pose_angles[angles] is not None:
                    diff = abs(actual_angles[angles] - tree_pose_angles[angles])
                    if diff > abs(max_diff):
                        max_diff = actual_angles[angles] - tree_pose_angles[angles]
                        diff_joint = angles
    return max_diff, diff_joint

@async_to_sync
async def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait() 

def genFrames(debug = False):
    cap = cv2.VideoCapture(0)
    curr_time = 0


    #pose model
    with mp_pose.Pose() as pose_tracker:

        while cap.isOpened():
            ret, frame = cap.read()

            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make Detections
            result= pose_tracker.process(image)
            pose_landmarks = result.pose_landmarks

            # Recolor image back to BGR for rendering
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            try:
                pose = pose_landmarks.landmark

                pose_name, score_arr = get_pose_prediction(pose)
                score = round(score_arr[np.argmax(score_arr)],2)

                line_color = mp_drawing.DrawingSpec(color=(0, 0, 150), thickness=2, circle_radius=2)
                circle_color = mp_drawing.DrawingSpec(color=(0, 0, 200), thickness=2, circle_radius=2)

                #put redirect bhako link ko number instead of pose name for the website
                if pose_name == "t" and score > 0.72:
                    line_color = mp_drawing.DrawingSpec(color=(0, 150, 0), thickness=2, circle_radius=2)
                    circle_color = mp_drawing.DrawingSpec(color=(0, 200, 0), thickness=2, circle_radius=2)
                    difference, name = generate_errors(pose_name, pose)
                    if curr_time >30:
                        speak("Maintain pose")
                        curr_time = 0

                elif pose_name == "t" and score <0.72:
                    if curr_time >30:
                        speak("Improve the pose")
                        curr_time = 0

                else:
                    if curr_time >= 50:
                        speak("Improve Pose")
                        curr_time = 0

                if debug:

                    coords = (100, 100)          

                                # Get status box
                    cv2.rectangle(frame, (0,0), (250, 60), (245, 117, 16), -1)

                                # Display Class
                    cv2.putText(frame, 'CLASS', (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(frame, pose_name.split(' ')[0], (90,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                                # Display Probability
                    cv2.putText(frame, 'PROB', (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(frame, str(score), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    if pose_landmarks is not None:
                        mp_drawing.draw_landmarks(
                        frame,
                        pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        line_color,
                        circle_color
                    )
                        



            except:
                if curr_time > 100:
                    speak("No pose detected")
                    curr_time = 0
            
            curr_time +=1

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
        
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


       
