import math
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_distance(pointA, pointB) -> float:
    """
    Calcule la distance Euclidienne entre deux points en 2D.
    """
    return math.hypot(pointB[0] - pointA[0], pointB[1] - pointA[1])

def extract_keypoints(results, landmarks_list) -> list:
    """
    Extrait, pour chaque landmark de landmarks_list, les valeurs (x, y, z, visibilité).
    """
    landmarks = results.pose_landmarks.landmark
    data = []
    for lm in landmarks_list:
        idx = mp_pose.PoseLandmark[lm].value
        kp = landmarks[idx]
        data.extend([kp.x, kp.y, kp.z, kp.visibility])
    return data

def analyze_foot_knee_placement(results, stage: str) -> tuple:
    """
    Analyse le placement des pieds et des genoux.

    - Feet: 
         Ratio = foot_distance / shoulder_width
         → Si ratio < 1.2, retourne "Foot placement is too tight"
         → Si ratio entre 1.2 et 2.8, retourne "Correct form"
         → Si ratio > 2.8, retourne "Foot placement is too wide"
         
    - Knees (en fonction de la position) :  
         En UP position:
              if knee_distance/foot_distance < 0.5  → "2 Knees are too tight"
              if knee_distance/foot_distance > 1.0  → "2 Knees are too wide"
              else → "Correct form"
         En MIDDLE position:
              if knee_distance/foot_distance < 0.7  → "2 Knees are too tight"
              if knee_distance/foot_distance > 1.0  → "2 Knees are too wide"
              else → "Correct form"
         En DOWN position:
              if knee_distance/foot_distance < 0.7  → "2 Knees are too tight"
              if knee_distance/foot_distance > 1.1  → "2 Knees are too wide"
              else → "Correct form"
    """
    feedback_feet = "No feedback for feet"
    feedback_knees = "No feedback for knees"
    
    if not results.pose_landmarks:
        return feedback_feet, feedback_knees

    lms = results.pose_landmarks.landmark
    min_vis = 0.5
    required = [
        mp_pose.PoseLandmark.LEFT_SHOULDER,
        mp_pose.PoseLandmark.RIGHT_SHOULDER,
        mp_pose.PoseLandmark.LEFT_FOOT_INDEX,
        mp_pose.PoseLandmark.RIGHT_FOOT_INDEX,
        mp_pose.PoseLandmark.LEFT_KNEE,
        mp_pose.PoseLandmark.RIGHT_KNEE
    ]
    for p in required:
        if lms[p.value].visibility < min_vis:
            return feedback_feet, feedback_knees

    # Calcul du ratio Feet/Shoulder
    left_sh = [lms[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
               lms[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    right_sh = [lms[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                lms[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
    shoulder_width = calculate_distance(left_sh, right_sh)

    left_ft = [lms[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,
               lms[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
    right_ft = [lms[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,
                lms[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
    foot_distance = calculate_distance(left_ft, right_ft)

    ratio_fs = round(foot_distance / shoulder_width, 2) if shoulder_width else 0
    if ratio_fs < 1.2:
        feedback_feet = "Foot placement is too tight"
    elif ratio_fs > 2.8:
        feedback_feet = "Foot placement is too wide"
    else:
        feedback_feet = "Correct form"

    # Calcul du ratio Knees/Feet
    left_kn = [lms[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
               lms[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
    right_kn = [lms[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                lms[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
    knee_distance = calculate_distance(left_kn, right_kn)
    ratio_kf = round(knee_distance / foot_distance, 2) if foot_distance else 0
    
    if stage.lower() == "up":
        if ratio_kf < 0.5:
            feedback_knees = "2 Knees are too tight"
        elif ratio_kf > 1.0:
            feedback_knees = "2 Knees are too wide"
        else:
            feedback_knees = "Correct form"
    elif stage.lower() == "middle":
        if ratio_kf < 0.7:
            feedback_knees = "2 Knees are too tight"
        elif ratio_kf > 1.0:
            feedback_knees = "2 Knees are too wide"
        else:
            feedback_knees = "Correct form"
    elif stage.lower() == "down":
        if ratio_kf < 0.7:
            feedback_knees = "2 Knees are too tight"
        elif ratio_kf > 1.1:
            feedback_knees = "2 Knees are too wide"
        else:
            feedback_knees = "Correct form"
    else:
        feedback_knees = "Not evaluated"

    return feedback_feet, feedback_knees

def analyze_back_position(results) -> str:
    """
    Analyse la position du dos en utilisant les coordonnées z (profondeur) des épaules et des hanches.
    Si la moyenne des z des hanches dépasse celle des épaules d'au moins 0.08,
    le dos est considéré comme trop penché vers l'avant.
    """
    if not results.pose_landmarks:
        return "No data for back"
    
    lms = results.pose_landmarks.landmark
    min_vis = 0.5
    for name in ["LEFT_SHOULDER", "RIGHT_SHOULDER", "LEFT_HIP", "RIGHT_HIP"]:
        if lms[getattr(mp_pose.PoseLandmark, name).value].visibility < min_vis:
            return "Insufficient data for back"
    
    left_sh_z = lms[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z
    right_sh_z = lms[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z
    avg_sh_z = (left_sh_z + right_sh_z) / 2

    left_hp_z = lms[mp_pose.PoseLandmark.LEFT_HIP.value].z
    right_hp_z = lms[mp_pose.PoseLandmark.RIGHT_HIP.value].z
    avg_hp_z = (left_hp_z + right_hp_z) / 2

    if (avg_hp_z - avg_sh_z) > 0.08:
        return "Back: Incorrect"
    else:
        return "Correct"
