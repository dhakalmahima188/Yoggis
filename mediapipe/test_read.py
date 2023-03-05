import csv
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
    with open('data.csv', 'r') as file:
            reader = csv.reader(file)
            i=0
            for row in reader:
                for i in range(1,len(row)):
                    tree_pose_angles.update({keys[i-1]:float(row[i])})
            

    tree_pose_angles['left_elbow_angle'] = 180
    tree_pose_angles['right_elbow_angle'] = 180
    tree_pose_angles['left_shoulder_angle'] = 180
    tree_pose_angles['right_shoulder_angle'] = 180
    tree_pose_angles['left_hip_angle'] = 180
    tree_pose_angles['right_hip_angle'] = 180

    return tree_pose_angles
