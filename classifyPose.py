import mediapipe as mp
import matplotlib.pyplot as plt
import cv2
# from calculateAngle import calculateAngle

# Initializing mediapipe pose class.
mp_pose = mp.solutions.pose

# Setting up the Pose function.
pose = mp_pose.Pose(static_image_mode=True,
                    min_detection_confidence=0.5, model_complexity=2)

# Initializing mediapipe drawing class, useful for annotation.
mp_drawing = mp.solutions.drawing_utils

import math

def calculateAngle(landmark1, landmark2, landmark3):
    

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
def getPoseCorrection(landmarks, label):
    corrections = []
    angle_display = []
    
    # Get required angles
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])
    
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
    
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
    
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])
    
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                   landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])
    
    left_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                  landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                  landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
    
    right_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                   landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                   landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
    
    # Store angle information for display
    angle_display.append(f"L Elbow: {int(left_elbow_angle)}°")
    angle_display.append(f"R Elbow: {int(right_elbow_angle)}°")
    angle_display.append(f"L Shoulder: {int(left_shoulder_angle)}°")
    angle_display.append(f"R Shoulder: {int(right_shoulder_angle)}°")
    angle_display.append(f"L Knee: {int(left_knee_angle)}°")
    angle_display.append(f"R Knee: {int(right_knee_angle)}°")
    angle_display.append(f"L Hip: {int(left_hip_angle)}°")
    angle_display.append(f"R Hip: {int(right_hip_angle)}°")



    # Pose-specific corrections
    if label == 'Warrior II Pose':
        if left_knee_angle < 90 or right_knee_angle < 90:
            corrections.append("Bend your front knee more deeply (should be at 90 degrees)")
        if left_knee_angle > 120 or right_knee_angle > 120:
            corrections.append("Straighten your front leg more")
        if left_shoulder_angle < 80 or right_shoulder_angle < 80:
            corrections.append("Raise your arms higher")
        if left_shoulder_angle > 110 or right_shoulder_angle > 110:
            corrections.append("Lower your arms slightly")
    
    elif label == 'Tree Pose':
        if left_knee_angle < 315 or right_knee_angle > 45:
            corrections.append("Bring your foot higher on your inner thigh")
        if left_knee_angle > 335 or right_knee_angle < 25:
            corrections.append("Lower your foot slightly on your leg")
        if left_shoulder_angle < 80 or right_shoulder_angle < 80:
            corrections.append("Bring your hands higher above your head")
    
    elif label == 'Bhujangasana':
        if right_hip_angle < 110 or left_hip_angle < 100:
            corrections.append("Arch your back more")
        if right_hip_angle > 140 or left_hip_angle > 140:
            corrections.append("Reduce the arch in your back slightly")
        if left_shoulder_angle > 30 or right_shoulder_angle > 30:
            corrections.append("Relax your shoulders down")
    
    elif label == 'T Pose':
        if left_elbow_angle < 165 or right_elbow_angle < 165:
            corrections.append("Straighten your arms more")
        if left_shoulder_angle < 80 or right_shoulder_angle < 80:
            corrections.append("Raise your arms to shoulder height")
    
    elif label == 'Trikonasana':
        if left_hip_angle < 230 or right_hip_angle < 230:
            corrections.append("Lean more to the side")
        if left_hip_angle > 260 or right_hip_angle > 260:
            corrections.append("Reduce your side bend slightly")
        if left_elbow_angle < 150 or right_elbow_angle < 150:
            corrections.append("Straighten your arms more")
    
    elif label == 'cat-cow pose':
        if left_knee_angle < 75 or right_knee_angle < 75:
            corrections.append("Flatten your back more")
        if left_knee_angle > 110 or right_knee_angle > 110:
            corrections.append("Arch your back more")
    
    elif label == 'savsana':
        if left_hip_angle < 165 or right_hip_angle < 165:
            corrections.append("Relax your legs completely")
        if left_shoulder_angle > 20 or right_shoulder_angle > 20:
            corrections.append("Relax your arms more by your sides")
    
    elif label == 'Halasana':
        if right_knee_angle < 70 or left_knee_angle < 70:
            corrections.append("Straighten your legs more")
        if right_hip_angle > 55 or left_hip_angle > 55:
            corrections.append("Lift your hips higher")
    
    elif label == 'camel pose':
        if right_knee_angle < 80 or left_knee_angle < 80:
            corrections.append("Align your knees directly under your hips")
        if right_shoulder_angle < 60 or left_shoulder_angle < 60:
            corrections.append("Reach back more with your hands")
    
    elif label == 'peacock pose':
        if left_elbow_angle < 80 or right_elbow_angle < 80:
            corrections.append("Keep your elbows closer to your body")
        if left_hip_angle < 165 or right_hip_angle < 165:
            corrections.append("Lift your legs higher")

    return corrections if corrections else ["Good form! Keep it up!"],angle_display


def classifyPose(landmarks, output_image, display=False):

    # Initialize the label of the pose. It is not known at this stage.
    label = 'Unknown Pose'

    # Specify the color (Red) with which the label will be written on the image.
    color = (0, 0, 255)

    # Calculate the required angles.
    # ----------------------------------------------------------------------------------------------------------------

    # Get the angle between the left shoulder, elbow and wrist points.
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    # Get the angle between the right shoulder, elbow and wrist points.
    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])

    # Get the angle between the left elbow, shoulder and hip points.
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    # Get the angle between the right hip, shoulder and elbow points.
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])

    # Get the angle between the left hip, knee and ankle points.
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    # Get the angle between the right hip, knee and ankle points
    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    left_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])

    right_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])

    left_bend_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
    right_bend_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])

    left_wrist_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                                      landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value])

    right_wrist_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                                       landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value],)

    # ----------------------------------------------------------------------------------------------------------------

    # Check if it is the warrior II pose or the T pose.
    # As for both of them, both arms should be straight and shoulders should be at the specific angle.
    # ----------------------------------------------------------------------------------------------------------------

    # Check if the both arms are straight.
    if left_elbow_angle > 165 and left_elbow_angle < 195 and right_elbow_angle > 165 and right_elbow_angle < 195:

        # Check if shoulders are at the required angle.
        if left_shoulder_angle > 80 and left_shoulder_angle < 110 and right_shoulder_angle > 80 and right_shoulder_angle < 110:

            # Check if it is the warrior II pose.
            # ----------------------------------------------------------------------------------------------------------------

            # Check if one leg is straight.
            if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

                # Check if the other leg is bended at the required angle.
                if left_knee_angle > 90 and left_knee_angle < 120 or right_knee_angle > 90 and right_knee_angle < 120:

                    # Specify the label of the pose that is Warrior II pose.
                    label = 'Warrior II Pose'

    # ----------------------------------------------------------------------------------------------------------------

    # Check if it is the T pose.
    # ----------------------------------------------------------------------------------------------------------------

            # Check if both legs are straight
            if left_knee_angle > 160 and left_knee_angle < 195 and right_knee_angle > 160 and right_knee_angle < 195:

                # Specify the label of the pose that is tree pose.
                label = 'T Pose'

    # ----------------------------------------------------------------------------------------------------------------

    # Check if it is the tree pose.
    # ----------------------------------------------------------------------------------------------------------------

    # Check if one leg is straight
    if left_knee_angle > 165 and left_knee_angle < 195 or right_knee_angle > 165 and right_knee_angle < 195:

        # Check if the other leg is bended at the required angle.
        if left_knee_angle > 315 and left_knee_angle < 335 or right_knee_angle > 25 and right_knee_angle < 45:

            # Specify the label of the pose that is tree pose.
            label = 'Tree Pose'

    # ----------------------------------------------------------------------------------------------------------------

    # check if it is bhujangasana
    if right_hip_angle >= 110 and right_hip_angle <= 140 or left_hip_angle >= 100 and left_hip_angle <= 140:

        if left_shoulder_angle >= 15 and left_shoulder_angle <= 30 or right_shoulder_angle >= 15 and right_shoulder_angle <= 30:

            if right_knee_angle > 165 and right_knee_angle < 200 or left_knee_angle > 165 and left_knee_angle < 200:

                if right_elbow_angle > 165 and right_elbow_angle < 210 or left_elbow_angle > 165 and left_elbow_angle < 210:
                    label = 'Bhujangasana'

    # ----------------------------------------------------------------------------------------------------------------

    # #check if it is Artha Uttanasana
    if left_hip_angle > 75 and left_hip_angle < 100 or right_hip_angle > 75 and right_hip_angle < 100:
        if left_knee_angle > 175 and left_knee_angle < 190 or right_knee_angle > 175 and right_knee_angle <= 180:
            if left_shoulder_angle > 30 and left_shoulder_angle < 70 or right_shoulder_angle > 30 and right_shoulder_angle < 70:
                label = "Artha Uttanasana"

    # #check if it is uttanpadasana
            if left_shoulder_angle > 165 and left_shoulder_angle < 210 or right_shoulder_angle > 165 and right_shoulder_angle < 210:

                label = "ViraBadhrasana"
    # -----------------------------------------------------------------------------------------------------------------

    # check if trikonasana
    if left_shoulder_angle >= 80 and left_shoulder_angle <= 110 and right_shoulder_angle >= 80 and right_shoulder_angle < 110:
        # if right_bend_hip_angle> 50 and right_bend_hip_angle < 80 or left_bend_hip_angle >50 and left_bend_hip_angle<80:
        if left_hip_angle > 230 and left_hip_angle < 260 or right_hip_angle > 230 and right_hip_angle < 260:
            if left_elbow_angle > 150 and left_elbow_angle < 175 or right_elbow_angle > 150 and right_elbow_angle < 175:
                if left_knee_angle >= 170 and left_knee_angle <= 195 or right_knee_angle >= 170 and right_knee_angle <= 195:
                    label = "Trikonasana"

    # -----------------------------------------------------------------------------------------------------------------

    # check if it is cow pose

    if left_knee_angle > 75 and left_knee_angle <= 110 or right_knee_angle > 75 and right_knee_angle <= 110:
        if left_shoulder_angle > 75 and left_shoulder_angle <= 110 or right_shoulder_angle > 75 and right_shoulder_angle <= 110:
            if left_hip_angle > 75 and left_hip_angle < 100 or right_hip_angle > 75 and right_hip_angle < 100:
                label = "cat-cow pose"

    # -------------------------------------------------------------------------------------------------------------------
    # check for savasana

    # if left_shoulder_angle > 0 and left_shoulder_angle<20 or right_shoulder_angle>0 and right_shoulder_angle<20:
    if left_hip_angle > 165 and left_hip_angle < 210 or right_hip_angle > 165 and right_hip_angle < 210:
        if left_knee_angle > 165 and left_knee_angle < 210 or right_knee_angle > 165 and right_knee_angle <= 210:
            if left_shoulder_angle > 0 and left_shoulder_angle < 20 or right_shoulder_angle > 0 and right_shoulder_angle < 20:
                # if left_wrist_angle>100 and left_wrist_angle< 170 or right_wrist_angle>100 and right_wrist_angle<170:
                label = "savsana"

    # -------------------------------------------------------------------------------------------------------------------
    # check if halasana

    if right_knee_angle >= 70 and right_hip_angle <= 110 or left_knee_angle >= 70 and left_knee_angle <= 110:
        if right_hip_angle >= 30 and right_hip_angle <= 55 or left_hip_angle >= 30 and left_hip_angle <= 55:
            if right_shoulder_angle >= 60 and right_shoulder_angle <= 90 or left_shoulder_angle >= 60 and left_shoulder_angle <= 90:
                label = "Halasana"
    # ---------------------------------------------------------------------------------------------------------------------
     # check if camel pose

    if right_knee_angle >= 80 and right_knee_angle <= 100 or left_knee_angle >= 80 and left_knee_angle <= 100:
        if right_shoulder_angle >= 60 and right_shoulder_angle <= 80 or left_shoulder_angle >= 60 and left_shoulder_angle <= 80:
            if right_hip_angle >= 105 and right_hip_angle <= 145 or left_hip_angle >= 105 and left_hip_angle <= 145:
                label = "camel pose"

    # ---------------------------------------------------------------------------------------------------------------------
    # check if peacock pose

    if left_elbow_angle >= 80 and left_elbow_angle <= 110 or right_elbow_angle >= 80 and right_elbow_angle <= 110:
        if left_hip_angle > 165 and left_hip_angle < 210 or right_hip_angle > 165 and right_hip_angle < 210:
            if left_knee_angle > 165 and left_knee_angle < 210 or right_knee_angle > 165 and right_knee_angle <= 210:
                label = "peacock pose"

    # Get corrections and angles for the pose
    corrections, angle_display = getPoseCorrection(landmarks, label) if label != 'Unknown Pose' else ([], [])
    
    # Check if the pose is classified successfully
    if label != 'Unknown Pose':
        color = (0, 255, 0)
    
    # Write the label on the output image
    cv2.putText(output_image, label, (10, 30),
                cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    
    # Display angles on the right side of the image
    for i, angle in enumerate(angle_display[:6]):  # Show up to 6 angles
        cv2.putText(output_image, angle, (output_image.shape[1] - 200, 30 + i*30),
                    cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)
    
    # Add corrections to the image
    for i, correction in enumerate(corrections[:3]):  # Show up to 3 corrections
        cv2.putText(output_image, correction, (10, 70 + i*30),
                    cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)
    
    if display:
        plt.figure(figsize=[10, 10])
        plt.imshow(output_image[:, :, ::-1])
        plt.title("Output Image")
        plt.axis('off')
    else:
        return output_image, label, corrections, angle_display