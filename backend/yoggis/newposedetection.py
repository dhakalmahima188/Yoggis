import mediapipe as mp
import cv2
import csv
import pickle
import math
import numpy as np
import pandas as pd
import warnings
# from gtts import gTTS
import os
import time
from asgiref.sync import async_to_sync
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
import pyttsx3
from .models import YogaScore, Yoga
import time

# TODO: add new pose from admin

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


# assign tree actual angles from csv file
def actual_refrence_angles(pose_name):

    real_pose_angles = {
        x+"_angle": None for x in joints
    }
    path_to_csv = os.path.join(settings.BASE_DIR, 'data.csv')
    keys = [x+"_angle" for x in joints]
    try:
        with open(path_to_csv, 'r') as file:
            reader = csv.reader(file)
            i = 0
            for row in reader:
                if row[0] == pose_name:
                    for i in range(1, len(row)):
                        real_pose_angles.update({keys[i-1]: float(row[i])})
            return real_pose_angles
    except Exception as e:
        print(e)
        


def return_angle(landmark1, landmark2, landmark3):
    x1, y1 = landmark1.x, landmark1.y
    x2, y2 = landmark2.x, landmark2.y
    x3, y3 = landmark3.x, landmark3.y

    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                         math.atan2(y1 - y2, x1 - x2))

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
                                       pose[landmark_names.index(
                                           'left_shoulder')],
                                       pose[landmark_names.index('left_hip')])
    right_shoulder_angle = return_angle(pose[landmark_names.index('right_hip')],
                                        pose[landmark_names.index(
                                            'right_shoulder')],
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

    computed_angles = {'left_elbow_angle': left_elbow_angle,
                       'right_elbow_angle': right_elbow_angle,
                       'left_shoulder_angle': left_shoulder_angle,
                       'right_shoulder_angle': right_shoulder_angle,
                       'left_hip_angle': left_hip_angle,
                       'right_hip_angle': right_hip_angle,
                       'left_knee_angle': left_knee_angle,
                       'right_knee_angle': right_knee_angle}
    return computed_angles


def get_pose_prediction(pose):
    pose_row = list(np.array([[landmark.x, landmark.y, landmark.z,
                    landmark.visibility] for landmark in pose]).flatten())
    X = pd.DataFrame([pose_row])
    pose_detection_class = model.predict(X)[0]
    pose_detection_probability = model.predict_proba(X)[0]
    return pose_detection_class, pose_detection_probability

    
def generate_errors(pose_name, pose):
    ideal_angles = actual_refrence_angles(pose_name)
    actual_angles = compute_joint_angles(pose)
    max_diff = 0
    diff_joint = ""
    for angles in actual_angles.keys():
        if ideal_angles[angles] is not None:
            diff = abs(actual_angles[angles] - ideal_angles[angles])
            if diff > abs(max_diff):
                max_diff = actual_angles[angles] - ideal_angles[angles]
                diff_joint = angles
    return max_diff, diff_joint


def generate_error_message(pose_name, pose):
    difference, joint_name = generate_errors(pose_name, pose)
    error_msg = ""

    arms_err_msgs = ['move left arm up', 'move left arm down',
                     'move right arm up', 'move right arm down',
                     'straighten your left arm', 'straighten your right arm']

    legs_err_msgs = ['move left leg up', 'move left leg down',
                     'move right leg up', 'move right leg down'
                     'straighten your left leg', 'straighten your right leg'
                     'bend your knees', 'bend your left knee', 'bend your right knee', 'move your legs apart',
                     'bring your legs closer']

    hips_error_message = ['lean to the left',
                          'lean to the right', 'stand straight']

    back_error_message = ['bend your back', 'straighten your back']

    if (joint_name == 'left_shoulder_angle'):
        if (difference > 0):
            error_msg = arms_err_msgs[0]
        else:
            error_msg = arms_err_msgs[1]

    elif (joint_name == 'right_shoulder_angle'):
        if (difference > 0):
            error_msg = arms_err_msgs[2]
        else:
            error_msg = arms_err_msgs[3]

    elif (joint_name == 'left_elbow_angle'):
        error_msg = "straighten your left arm"

    elif (joint_name == 'right_elbow_angle'):
        error_msg = "straighten your right arm"

    elif (joint_name == 'left_hip_angle'):
        error_msg = hips_error_message[0]

    elif (joint_name == 'right_hip_angle'):
        error_msg = hips_error_message[1]

    elif (joint_name == 'left_knee_angle'):
        error_msg = "error in the left knee"

    elif (joint_name == 'right_knee_angle'):
        error_msg = "error in the right knee"
    else:
        error_msg = "move back"
    return joint_name, error_msg


def get_coordinate(joint_name, landmarks):
    if joint_name in landmark_names:
        return landmarks[landmark_names.index(landmark_names[landmark_names.index(joint_name)])][0], landmarks[landmark_names.index(landmark_names[landmark_names.index(joint_name)])][1]
    else:
        return None

@async_to_sync
async def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def draw_on_image(image, pose_name: str, pose_prob):
    # Get status box
    cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)

    # Display Class
    cv2.putText(image, 'CLASS', (95, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, pose_name.split(' ')[
                0], (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display Probability
    cv2.putText(image, 'PROB', (15, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, str(pose_prob), (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)



def genFrames(request, yoga_id, debug=True):
    start_time = time.time() 
    print("hello dost")
    pose_name = "tree"
    cap = cv2.VideoCapture(0)
    curr_time = 0
    user = request.user
    yoga = Yoga.objects.get(id=yoga_id)

    #Update the user's Yoga score for the current pose
    try:
        yoga_score = YogaScore.objects.get(user=user, yoga=yoga)
    except YogaScore.DoesNotExist:
        yoga_score = YogaScore.objects.create(user=user, score=1, yoga=yoga)

    with mp_pose.Pose() as pose_tracker:

        while cap.isOpened():
            
            ret, frame = cap.read()

            # Recolor Feed
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            height, width, _ = image.shape

            # Make Detections
            result = pose_tracker.process(image)
            pose_landmarks = result.pose_landmarks

            landmarks = []
            if result.pose_landmarks:
                for landmark in result.pose_landmarks.landmark:
                    # Append the landmark into the list.
                    landmarks.append((int(landmark.x * width), int(landmark.y * height)))

            # Recolor image back to BGR for rendering
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            output_frame = image.copy()
            message = ""
                
            try:
                pose = pose_landmarks.landmark
                pose_class, pose_probability = get_pose_prediction(pose)
                draw_on_image(output_frame, pose_class, pose_probability[2])

                if pose_class == pose_name and pose_probability[2] > 0.5:
                    message = "Maintain Pose"
                    yoga_score.score += 1
                    yoga_score.save() 
                else:
                    message = "Pose Incorrect"
                    error_joint, error_msg = generate_error_message(pose_name, pose)
                    #print(error_joint, error_msg)
                    error_msg_coords = get_coordinate(
                        "_".join(error_joint.split("_")[:2]), landmarks)
                    cv2.putText(output_frame,
                                error_msg,
                                error_msg_coords,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (255, 255, 255), 2,
                                cv2.LINE_AA)

            except Exception as e:
                print(e)
            
            print(message)
            ret, buffer = cv2.imencode('.jpg', output_frame)
            frame = buffer.tobytes()
            
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time >= 20:
                print("This message is printed after a 20-second delay. espachi session sakincha")
                yoga_score.my_list.append(yoga_score.score-int(yoga_score.my_list[-1]))
                yoga_score.save() 
                break

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
