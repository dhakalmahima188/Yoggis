import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
import csv

#calculate angles
def calculateAngle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    
    #theta = atan2(P3.y - P1.y, P3.x - P1.x) - atan2(P2.y - P1.y, P2.x - P1.x);

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 


# For webcam input:
cap = cv2.VideoCapture(0)
## Setup mediapipe instance
def get_cordinate(i):
    return results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].x,results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].y,results.pose_landmarks.landmark[mp_pose.PoseLandmark(i).value].z
actual=[]
     
with open('data.csv', 'r') as file:
 reader = csv.reader(file)
 i=0
 for row in reader:
   for i in range(1,len(row)):        
    actual.append(float(row[i]))
  
setposition=0

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
                #left
            l11 = calculateAngle(get_cordinate(23), get_cordinate(11), get_cordinate(13))
            l13 = calculateAngle(get_cordinate(11), get_cordinate(13), get_cordinate(15))
            l15 = calculateAngle(get_cordinate(13), get_cordinate(15), get_cordinate(17))
            l23 = calculateAngle(get_cordinate(11), get_cordinate(23), get_cordinate(25))
            l25 = calculateAngle(get_cordinate(23), get_cordinate(25), get_cordinate(27))
            # print(l11,l13,l15,l23,l25)
        #right
            r12 = calculateAngle(get_cordinate(24), get_cordinate(12), get_cordinate(14))
            r14 = calculateAngle(get_cordinate(12), get_cordinate(14), get_cordinate(16))
            r16 = calculateAngle(get_cordinate(18), get_cordinate(16), get_cordinate(14))
            r24 = calculateAngle(get_cordinate(12), get_cordinate(24), get_cordinate(26))
            r26 = calculateAngle(get_cordinate(24), get_cordinate(26), get_cordinate(28))
            # print(r12,r14,r16,r24,r26)
            print(get_cordinate(11)[0],get_cordinate(11)[1])
            e1=-(l11-actual[0])
            e2=-(l13-actual[1])
            e3=-(l15-actual[2])
            e4=-(r12-actual[5])
            e5=-(r14-actual[6])
            e6=-(r16-actual[7])
           
            # print(e2,e5)
                        
            lerror=' '    
            if(e2>10):
                lerror=lerror+"lift your left shoulder down"
                setposition=13
            elif(e2<-10):
                lerror=lerror+"lift your left shoulder up"
                setposition=13
            else:
                lerror=lerror+"0k"
                setposition=13
            
            rerror=' '    
            if(e5>10):
                rerror=rerror+"lift your left shoulder down"
                rsetposition=14
            elif(e5<-10):
                rerror=rerror+"lift your left shoulder up"
                rsetposition=14
            else:
                rerror=rerror+"ok"
                rsetposition=14
                   
                
      
            # Visualize angle
            cv2.putText(image, str(lerror), 
                           tuple(np.multiply( (get_cordinate(setposition)[0],get_cordinate(setposition)[1]) , [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )    
            cv2.putText(image, str(rerror), 
                           tuple(np.multiply( (get_cordinate(rsetposition)[0],get_cordinate(rsetposition)[1]) , [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )       
            cv2.putText(image, str("Welcome to yogis"), 
                          (10,10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA )


            
                     
        except Exception as e:
            print("caught",e)
        
      
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Yoggis', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()