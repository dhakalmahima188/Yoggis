from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse
import cv2
import math
from time import time
import mediapipe as mp
import matplotlib.pyplot as plt
import statistics
import numpy as np
import csv
import os
from django.conf import settings

# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose
results=0
# Setting up the Pose function.
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3, model_complexity=2)

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils 

def detectPose(image, pose, display=True):
    '''
    This function performs pose detection on an image.
    Args:
        image: The input image with a prominent person whose pose landmarks needs to be detected.
        pose: The pose setup function required to perform the pose detection.
        display: A boolean value that is if set to true the function displays the original input image, the resultant image, 
                 and the pose landmarks in 3D plot and returns nothing.
    Returns:
        output_image: The input image with the detected pose landmarks drawn.
        landmarks: A list of detected landmarks converted into their original scale.
    '''
    
    # Create a copy of the input image.
    output_image = image.copy()
    
    # Convert the image from BGR into RGB format.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Perform the Pose Detection.
    results = pose.process(imageRGB)
    
    # Retrieve the height and width of the input image.
    height, width, _ = image.shape
    
    # Initialize a list to store the detected landmarks.
    landmarks = []
    
    # Check if any landmarks are detected.
    if results.pose_landmarks:
    
        # Draw Pose landmarks on the output image.
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)
        
        # Iterate over the detected landmarks.
        for landmark in results.pose_landmarks.landmark:
            
            # Append the landmark into the list.
            landmarks.append((int(landmark.x * width), int(landmark.y * height),
                                  (landmark.z * width)))
    
    # Check if the original input image and the resultant image are specified to be displayed.
    if display:
    
        # Display the original input image and the resultant image.
        plt.figure(figsize=[22,22])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
        
        # Also Plot the Pose landmarks in 3D.
        mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
        
    # Otherwise
    else:
        
        # Return the output image and the found landmarks.
        return output_image, landmarks   

def calculateAngle(landmark1, landmark2, landmark3):
    '''
    This function calculates angle between three different landmarks.
    Args:
        landmark1: The first landmark containing the x,y and z coordinates.
        landmark2: The second landmark containing the x,y and z coordinates.
        landmark3: The third landmark containing the x,y and z coordinates.
    Returns:
        angle: The calculated angle between the three landmarks.

    '''

    # Get the required landmarks coordinates.
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    # Calculate the angle between the three points
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    
    # Check if the angle is less than zero.
    if angle < 0:

        # Add 360 to the found angle.
        angle += 360
    
    # Return the calculated angle.
    return angle

def get_cordinate(i,landmarks):
    return landmarks[mp_pose.PoseLandmark(i).value][0],landmarks[mp_pose.PoseLandmark(i).value][1],landmarks[mp_pose.PoseLandmark(i).value][2]

def getAccuracy(landmarks,image,display=False):
    actual=[]
    with open(os.path.join(settings.BASE_DIR, 'data.csv'), 'r') as file:
        reader = csv.reader(file)
        i=0
        for row in reader:
            for i in range(1,len(row)):        
                actual.append(float(row[i]))
    
    setposition=0   

                
    try:           # Get coordinates
                    #left
        l11 = calculateAngle(get_cordinate(23,landmarks), get_cordinate(11,landmarks), get_cordinate(13,landmarks))
        l13 = calculateAngle(get_cordinate(11,landmarks), get_cordinate(13,landmarks), get_cordinate(20,landmarks))
        l20 = calculateAngle(get_cordinate(13,landmarks), get_cordinate(20,landmarks), get_cordinate(17,landmarks))
        l23 = calculateAngle(get_cordinate(11,landmarks), get_cordinate(23,landmarks), get_cordinate(25,landmarks))
        l25 = calculateAngle(get_cordinate(23,landmarks), get_cordinate(25,landmarks), get_cordinate(27,landmarks))
        # print(l11,l13,l20,l23,l25)
       
    #right
        r12 = calculateAngle(get_cordinate(24,landmarks), get_cordinate(12,landmarks), get_cordinate(14,landmarks))
        r14 = calculateAngle(get_cordinate(12,landmarks), get_cordinate(14,landmarks), get_cordinate(16,landmarks))
        r16 = calculateAngle(get_cordinate(18,landmarks), get_cordinate(16,landmarks), get_cordinate(14,landmarks))
        r24 = calculateAngle(get_cordinate(12,landmarks), get_cordinate(24,landmarks), get_cordinate(26,landmarks))
        r26 = calculateAngle(get_cordinate(24,landmarks), get_cordinate(26,landmarks), get_cordinate(28,landmarks))
        # print(r12,r14,r16,r24,r26)
        # print(get_cordinate(11,landmarks)[0],get_cordinate(11,landmarks)[1])
        e1=-(l11-actual[0])
        e2=-(l13-actual[1])
        e3=-(l20-actual[2])
        e4=-(r12-actual[5])
        e5=-(r14-actual[6])
        e6=-(r16-actual[7])
                
        print(l11,l13,l20,l23,l25,r12,r14,r16,r24,r26)  
       # print(e1,e2,e3,e4,e5,e6)   
                    # print(e2,e5)
                                
        lerror=' '
        
        
            
        if(e1>20 or e1>300) :
            lerror=lerror+"lift your right shoulder down"
            setposition=11
        elif(e1<-20 or e1<-300) :
            lerror=lerror+"lift your right shoulder up"
            setposition=11
 
        else:
            lerror=lerror+"ok"
            setposition=11
            
        
        
        rerror=' '    
        if( e4>20 or e4>300):
            rerror=rerror+"lift your left shoulder up"
            rsetposition=12
        elif( e4<-20 or e4<-300):
            rerror=rerror+"lift your left shoulder down"
            rsetposition=12
      
        else:
            rerror=rerror+"ok"
            rsetposition=12
    
        
        
        lerror_elbow=' '    
        if( e2>20):
            lerror_elbow=lerror_elbow+"make your elbow straight"
            lelbow=13
        elif( e2<-20):
            lerror_elbow=lerror_elbow+"make your elbow straight"
            lelbow=13
      
        else:
            lerror_elbow=lerror_elbow+"ok"
            lelbow=13
        
        rerror_elbow=' '    
        if( e5>20):
            rerror_elbow=rerror_elbow+"make your elbow straight"
            relbow=14
        elif( e5<-20):
            rerror_elbow=rerror_elbow+"make your elbow straight"
            relbow=14
      
        else:
            rerror_elbow=rerror_elbow+"ok"
            relbow=14
            
        
        error={
            "lerror": lerror,
            "rerror": rerror,
            "lerror_elbow":lerror_elbow,
            "rerror_elbow":rerror_elbow
        }

        # Visualize angle
        cv2.putText(image, str(rerror_elbow), 
                     (get_cordinate(relbow,landmarks)[0],get_cordinate( relbow,landmarks)[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )    
        cv2.putText(image, str(lerror_elbow), 
                    (get_cordinate(lelbow,landmarks)[0],get_cordinate(lelbow,landmarks)[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )    
        cv2.putText(image, str(lerror), 
                     (get_cordinate(setposition,landmarks)[0],get_cordinate(setposition,landmarks)[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )    
        cv2.putText(image, str(rerror), 
                    (get_cordinate(rsetposition,landmarks)[0],get_cordinate(rsetposition,landmarks)[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )      
        cv2.putText(image, str("Welcome to yogis"), 
                    (10,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA )

        if display:
    
        # Display the resultant image.
            plt.figure(figsize=[10,10])
            plt.imshow(image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
            
        else:
            
            # Return the output image and the classified label.
            return image, error

        
            
    except Exception as e:
        print("caught",e)
                
   



def gen_frames():
    # Setup Pose function for video.
    pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)

    # Initialize the VideoCapture object to read from the webcam.
    
    camera_video = cv2.VideoCapture(0)

    # Initialize a variable to store the time of the previous frame.
    time1 = 0

    # Iterate until the video is accessed successfully.
    while camera_video.isOpened():
        # Read a frame.
        ok, frame = camera_video.read()
        # try: 
        # Check if frame is not read properly.
        if not ok:
            # Continue to the next iteration to read the next frame and ignore the empty camera frame.
            continue
        # Flip the frame horizontally for natural (selfie-view) visualization.
        frame = cv2.flip(frame, 1)
        # Get the width and height of the frame
        frame_height, frame_width, _ =  frame.shape
        # Resize the frame while keeping the aspect ratio.
        frame = cv2.resize(frame, (int(frame_width * (640 / frame_height)), 640))
        # Perform Pose landmark detection.
        frame, landmarks = detectPose(frame, pose_video, display=False)
        # Check if the landmarks are detected.
        if landmarks:
            # Perform the Pose Accuracy Stats.
            frame, _ = getAccuracy(landmarks, frame, display=False)
            # print(_)
        # Display the frame.

        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     'test',
        #     {
        #         'type': 'chat',
        #         'message': "nadika and mahima"
        #     }
        # )
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        #print("hi",frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
