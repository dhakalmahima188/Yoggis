import mediapipe as mp
import cv2
import csv
import pickle
import math
import numpy as np
import pandas
import warnings
# from gtts import gTTS
import os
import time
from asgiref.sync import async_to_sync
from django.conf import settings
import asyncio
from channels.layers import get_channel_layer
from django.http import HttpResponse
import pyttsx3
from .models import YogaScore, Yoga
import time


class PoseDetection:

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

    series_poses = {
        "series_1": ['tree', 't', 'warrior','extended_triangl'],
        "series_2": ['warrior', 'tree'],
    }

    arms_err_msgs = ['move left arm up', 'move left arm down',
                     'move right arm up', 'move right arm down',
                     'straighten your left arm', 'straighten your right arm']

    elbow_err_msgs = ["bend  left elbow", "bend  right elbow"
                      "straighten your left elbow", "straighten your right elbow", "1", "2"]

    legs_err_msgs = ['move left leg up', 'move left leg down',
                     'move right leg up', 'move right leg down'
                     'straighten your left leg', 'straighten your right leg'
                     'bend your knees', 'bend your left knee', 'bend your right knee', 'move your legs apart',
                     'bring your legs closer']

    hips_error_message = ['lean to the left',
                          'lean to the right', 'stand straight']

    back_error_message = ['bend your back', 'straighten your back']

    yoga_id_to_name = {
        6 : "t",
        23 : "tree",
        100:"series_1"
    }
    
    def __init__(self, pose_name, is_series=False):
     
        self.user = None
        self.pose_name = self.yoga_id_to_name[pose_name]
        # load model accordint go the pose_name
        self.model_name = self.pose_name+".pkl"
        self.model_path = "..\mediapipe\models\\" + self.model_name
        print(os.listdir('..\mediapipe\models\.'))
        self.is_series = is_series
        warnings.filterwarnings("ignore")
        self.ideal_angles = self.actual_refrence_angles()
        self.load_model()
        os.getcwd()

    def return_angle(self, landmark1, landmark2, landmark3):
        x1, y1 = landmark1.x, landmark1.y
        x2, y2 = landmark2.x, landmark2.y
        x3, y3 = landmark3.x, landmark3.y

        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))

        if angle < 0:
            angle += 360

        # Return the calculated angle.
        return angle

    def load_model(self):
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
                print(f"Loaded Model")
        except Exception as e:
            print("Exception raised while loading model: ", e)

    def actual_refrence_angles(self):

        real_pose_angles = {
            x+"_angle": None for x in self.joints
        }
        path_to_csv = os.path.join('data.csv')
        keys = [x+"_angle" for x in self.joints]
        try:
            with open(path_to_csv, 'r') as file:
                reader = csv.reader(file)
                i = 0
                for row in reader:
                    print(self.pose_name)
                    if row[0] == self.pose_name:
                        for i in range(1, len(row)):
                            real_pose_angles.update({keys[i-1]: float(row[i])})
                print(f"Loaded ideal angles")
                # none return bhairako chha sab nai
                print(real_pose_angles)
                return real_pose_angles
        except Exception as e:
            print("Exception raised while loading angles: ", e)

    def generate_errors(self, pose):
        actual_angles = self.compute_joint_angles(pose)
        max_diff = 0
        diff_joint = ""
        for angles in actual_angles.keys():
            if self.ideal_angles[angles] is not None:
                diff = abs(actual_angles[angles] - self.ideal_angles[angles])
                if diff > abs(max_diff):
                    max_diff = actual_angles[angles] - \
                        self.ideal_angles[angles]
                    diff_joint = angles
        return max_diff, diff_joint

    def compute_joint_angles(self, pose):
        left_elbow_angle = self.return_angle(pose[self.landmark_names.index('left_wrist')],
                                             pose[self.landmark_names.index(
                                                 'left_elbow')],
                                             pose[self.landmark_names.index('left_shoulder')])
        right_elbow_angle = self.return_angle(pose[self.landmark_names.index('right_shoulder')],
                                              pose[self.landmark_names.index(
                                                  'right_elbow')],
                                              pose[self.landmark_names.index('right_wrist')])
        left_shoulder_angle = self.return_angle(pose[self.landmark_names.index('left_elbow')],
                                                pose[self.landmark_names.index(
                                                    'left_shoulder')],
                                                pose[self.landmark_names.index('left_hip')])
        right_shoulder_angle = self.return_angle(pose[self.landmark_names.index('right_hip')],
                                                 pose[self.landmark_names.index(
                                                     'right_shoulder')],
                                                 pose[self.landmark_names.index('right_elbow')])
        left_hip_angle = self.return_angle(pose[self.landmark_names.index('left_knee')],
                                           pose[self.landmark_names.index(
                                               'left_hip')],
                                           pose[self.landmark_names.index('left_shoulder')])
        right_hip_angle = self.return_angle(pose[self.landmark_names.index('right_shoulder')],
                                            pose[self.landmark_names.index(
                                                'right_hip')],
                                            pose[self.landmark_names.index('right_knee')])
        left_knee_angle = self.return_angle(pose[self.landmark_names.index('left_ankle')],
                                            pose[self.landmark_names.index(
                                                'left_knee')],
                                            pose[self.landmark_names.index('left_hip')])
        right_knee_angle = self.return_angle(pose[self.landmark_names.index('right_hip')],
                                             pose[self.landmark_names.index(
                                                 'right_knee')],
                                             pose[self.landmark_names.index('right_ankle')])

        computed_angles = {'left_elbow_angle': left_elbow_angle,
                           'right_elbow_angle': right_elbow_angle,
                           'left_shoulder_angle': left_shoulder_angle,
                           'right_shoulder_angle': right_shoulder_angle,
                           'left_hip_angle': left_hip_angle,
                           'right_hip_angle': right_hip_angle,
                           'left_knee_angle': left_knee_angle,
                           'right_knee_angle': right_knee_angle}
        return computed_angles

    def draw_on_image(self, image, pose_name: str, pose_prob):
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

    def get_pose_prediction(self, pose):
        try:
            pose_row = list(np.array(
                [[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            X = pandas.DataFrame([pose_row])
            pose_detection_class = self.model.predict(X)[0]
            pose_detection_probability = self.model.predict_proba(X)[0]
            return pose_detection_class, pose_detection_probability
        except Exception as e:
            print("Error getting predictions: ", e)

    def get_coordinate(self, joint_name, landmarks):
        if joint_name in self.landmark_names:
            return landmarks[self.landmark_names.index(self.landmark_names[self.landmark_names.index(joint_name)])][0], landmarks[self.landmark_names.index(self.landmark_names[self.landmark_names.index(joint_name)])][1]
        else:
            return None

    async def speak(self, message):
        engine = pyttsx3.init()
        engine.say(message)

    def correct_screen(self, image):
        dimensions = image.shape
        overlay = image.copy()
        cv2.rectangle(overlay, (0, 0),
                      (dimensions[1], dimensions[0]), (0, 255, 0), -1)
        # cv2.putText(overlay, "Maintain Pose",
        #             (dimensions[0]/2, dimensions[1]/2),  cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
        cv2.addWeighted(overlay, 0.5, image, 1-0.5, 0, image)

    def generate_error_message(self, pose):

        difference, joint_name = self.generate_errors(pose)
        #print(difference, joint_name)
        error_msg = ""

        if (joint_name == 'left_shoulder_angle'):
            if (difference > 0):
                error_msg = self.arms_err_msgs[1]
            else:
                error_msg = self.arms_err_msgs[0]

        elif (joint_name == 'right_shoulder_angle'):
            if (difference > 0):
                error_msg = self.arms_err_msgs[3]
            else:
                error_msg = self.arms_err_msgs[2]

        elif (joint_name == 'left_elbow_angle'):
           error_msg = self.elbow_err_msgs[0]

        elif (joint_name == 'right_elbow_angle'):
            error_msg = self.elbow_err_msgs[1]

        elif (joint_name == 'left_hip_angle'):
            error_msg = self.hips_error_message[0]

        elif (joint_name == 'right_hip_angle'):
            error_msg = self.hips_error_message[1]

        elif (joint_name == 'left_knee_angle'):
            error_msg = "error in the left knee"

        elif (joint_name == 'right_knee_angle'):
            error_msg = "error in the right knee"
        else:
            error_msg = "move back"
        return joint_name, error_msg

    def generate_frames(self, request, yoga_id, debug=False):
        start_time = time.time()
        cap = cv2.VideoCapture(0)
        count = 0
        print("hello", request.user)
        user = request.user
        yoga = Yoga.objects.get(id=yoga_id)
        try:
            yoga_score = YogaScore.objects.get(user=user, yoga=yoga)
        except YogaScore.DoesNotExist:
            yoga_score = YogaScore.objects.create(user=user, score=1, yoga=yoga)

        series_count = 0
        current_pose_name=None   
        if self.is_series:     
            current_pose_name = self.series_poses[self.pose_name][0]
       # correct_frames = 0
        series_time_1 = time.time()

        with self.mp_pose.Pose() as pose_tracker:

            if not self.is_series:
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
                            landmarks.append(
                                (int(landmark.x * width), int(landmark.y * height)))

                    # Recolor image back to BGR for rendering
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    output_frame = image.copy()
                    message = ""

                    try:
                        pose = pose_landmarks.landmark
                        pose_class, pose_probability = self.get_pose_prediction(
                            pose)
                        # self.draw_on_image(
                        #    output_frame, pose_class, pose_probability[2])
                        if pose_class == self.pose_name and pose_probability[2] > 0.5:
                            message = "Maintain Pose"
                            yoga_score.score += 1
                            yoga_score.save()
                            self.correct_screen(output_frame)
                        else:
                            message = "Pose Incorrect"
                            error_joint, error_msg = self.generate_error_message(
                                pose)
                            error_msg_coords = self.get_coordinate(
                                "_".join(error_joint.split("_")[:2]), landmarks)
                            cv2.putText(output_frame,
                                        error_msg,
                                        error_msg_coords,
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (255, 255, 255), 2,
                                        cv2.LINE_AA)

                            if pose_landmarks:
                                self.mp_drawing.draw_landmarks(
                                    output_frame,
                                    pose_landmarks,
                                    self.mp_pose.POSE_CONNECTIONS,
                                    self.mp_drawing.DrawingSpec(
                                        color=(0, 0, 150), thickness=2, circle_radius=2),
                                    self. mp_drawing.DrawingSpec(
                                        color=(0, 0, 200), thickness=2, circle_radius=2)
                                )

                    except Exception as e:
                        pass

                    ret, buffer = cv2.imencode('.jpg', output_frame)
                    frame = buffer.tobytes()
                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    # yo jati chaincha rakhne
                    # if elapsed_time >= 20:
                    #     print("This message is printed after a 20-second delay. espachi session sakincha")
                    #     yoga_score.my_list.append(yoga_score.score-int(yoga_score.my_list[-1]))
                    #     yoga_score.save()
                    #     break

                    count += 1
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

            else:
                print("Not series")
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
                        pose_class, pose_probability = self.get_pose_prediction(pose)
                        print(current_pose_name)
                        if pose_class == current_pose_name and pose_probability[2] > 0.5:
                            correct_frames +=1
                            self.correct_screen(output_frame)
                        else:
                            error_joint, error_msg = self.generate_error_message(pose)
                            #print(error_joint, error_msg)
                            error_msg_coords = self.get_coordinate(
                                "_".join(error_joint.split("_")[:2]), landmarks)
                            cv2.putText(output_frame,
                                        error_msg,
                                        error_msg_coords,
                                        cv2.FONT_HERSHEY_SIMPLEX,
                                        0.5, (255, 255, 255), 2,
                                        cv2.LINE_AA)
                            if pose_landmarks:
                                self.mp_drawing.draw_landmarks(
                                    output_frame,
                                    pose_landmarks,
                                    self.mp_pose.POSE_CONNECTIONS,
                                    self.mp_drawing.DrawingSpec(
                                        color=(0, 0, 150), thickness=2, circle_radius=2),
                                    self. mp_drawing.DrawingSpec(
                                        color=(0, 0, 200), thickness=2, circle_radius=2)
                                )
                    except Exception as e:
                        pass

                    ret, buffer = cv2.imencode('.jpg', output_frame)
                    frame = buffer.tobytes()
                    current_time = time.time()
                    series_time_2=time.time()
                    elapsed_time = current_time - start_time
                    series_time_3=series_time_2-series_time_1

                    #if correct_frames > 60:
                    if  abs(series_time_3) > 5:
                        print("not waiting",series_time_3)
                        
                        if self.series_poses[self.pose_name][-1] == current_pose_name:
                            #draw next pose
                            # print("hello",series_time_3)
                            # series_count = 0
                            pass
                        
                        else:
                            correct_frames = 0
                            series_time_1=time.time()
                            series_count +=1
                            print(f"Completed: {self.series_poses[self.pose_name][series_count-1]}")
                            current_pose_name = self.series_poses[self.pose_name][series_count]  
                    else:
                        print("waiting",series_time_3)

                    # yo jati chaincha rakhne
                    if elapsed_time >= 20:
                        print("This message is printed after a 20-second delay. espachi session sakincha")
                        yoga_score.my_list.append(yoga_score.score-int(yoga_score.my_list[-1]))
                        yoga_score.save()
                        break

                    count += 1
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')