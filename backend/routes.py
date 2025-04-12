# routes.py
import cv2
import mediapipe as mp
import pandas as pd
import time
import numpy as np
from flask import Blueprint, Response, request, jsonify
from models import count_model, CLASSIFIER_HEADERS, User, Goal, db, CLASSIFIER_LMS
from detection import (
    extract_keypoints,
    analyze_foot_knee_placement,
    analyze_back_position,
    mp_pose,
    mp_drawing
)
from session import session_data, start_session, complete_session, get_report, all_session_reports, logout_session
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('routes', __name__)

# --- Endpoints Auth & Goal ---
@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    u = data.get("username")
    if not u or User.query.get(u):
        return jsonify({"error": "Username invalide ou déjà pris"}), 400
    user = User(
        username=u,
        pw_hash=generate_password_hash(data.get("password")),
        age=data.get("age"),
        weight=data.get("weight")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "Inscription réussie"}), 200

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.get(data.get("username"))
    if not user or not check_password_hash(user.pw_hash, data.get("password")):
        return jsonify({"error": "Identifiants incorrects"}), 401
    return jsonify({
        "username": user.username,
        "age": user.age,
        "weight": user.weight
    }), 200

@bp.route("/logout", methods=["POST"])
def logout():
    logout_session()
    return jsonify({"msg": "Déconnexion réussie"}), 200

@bp.route("/set_goal", methods=["POST"])
def set_goal():
    """
    Enregistre l'objectif de l'utilisateur.
    Expects JSON: { "username": <str>, "series": <int>, "reps": <int>, "target": <str> }
    """
    data = request.get_json()
    u = data.get("username")
    user = User.query.get(u)
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404
    g = Goal.query.filter_by(username=u).first()
    if not g:
        g = Goal(username=u)
        db.session.add(g)
    g.series = data.get("series")
    g.reps = data.get("reps")
    g.target = data.get("target")
    db.session.commit()
    return jsonify({"msg": "Objectif enregistré"}), 200

@bp.route("/get_goal/<username>", methods=["GET"])
def get_goal(username):
    g = Goal.query.filter_by(username=username).first()
    if not g:
        return jsonify({}), 200
    return jsonify({
        "series": g.series,
        "reps": g.reps,
        "target": g.target
    }), 200

@bp.route("/all_reports", methods=["GET"])
def all_reports():
    return jsonify({"reports": all_session_reports}), 200

# --- Endpoints Session & Stream ---
@bp.route('/start_session', methods=['POST'])
def start_session_route():
    data = request.get_json()
    t = data.get("target")
    try:
        t = int(t)
    except:
        return jsonify({"error": "'target' doit être un entier."}), 400
    start_session(t)
    return jsonify({"message": "Session démarrée.", "target": t}), 200

@bp.route('/get_report', methods=['GET'])
def get_report_route():
    if session_data["start_time"] is None:
        return jsonify({"error": "Aucune session démarrée."}), 400
    report = get_report()
    return jsonify(report), 200

def generate_frames():
    cap = cv2.VideoCapture(0)
    squat_phase = 0  # 0 : position "up" (repos), 1 : phase "down" détectée
    PREDICTION_THRESHOLD = 0.7

    # Paramètres d'affichage du header pour le texte en gras
    HEADER_HEIGHT = 170    # Augmenté pour contenir toutes les lignes
    FONT = cv2.FONT_HERSHEY_DUPLEX  # Police plus "gras"
    FONT_SCALE = 1.0       # Taille de police d'origine
    FONT_THICKNESS = 3     # Pour effet bold
    LINE_SPACING = 30      # Espacement vertical entre chaque ligne

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Redimensionnement de la frame (par exemple, 640 x 480)
        frame = cv2.resize(frame, (640, 480))
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        with mp.solutions.pose.Pose(min_detection_confidence=0.5,
                                    min_tracking_confidence=0.5) as pose:
            results = pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Création d'un header noir de HEADER_HEIGHT pixels
        header = np.zeros((HEADER_HEIGHT, image.shape[1], 3), dtype=np.uint8)
        header[:] = (0, 0, 0)

        fb_feet = "No data"
        fb_knees = "No data"
        fb_back = "No data"
        current_stage = "none"

        if results.pose_landmarks:
            row = extract_keypoints(results, CLASSIFIER_LMS)
            X = pd.DataFrame([row], columns=CLASSIFIER_HEADERS)
            pred = count_model.predict(X)[0]  # 0: down, 1: up
            pred = "down" if pred == 0 else "up"
            prob = count_model.predict_proba(X)[0].max()
            stage = "middle" if prob < PREDICTION_THRESHOLD else pred

            if stage == "down":
                squat_phase = 1
            elif stage == "up" and squat_phase == 1:
                session_data["counter"] += 1
                fb_feet, fb_knees = analyze_foot_knee_placement(results, "up")
                fb_back = analyze_back_position(results)
                if fb_feet == "Correct form" and fb_knees == "Correct form" and fb_back == "Correct":
                    session_data["count_correct"] += 1
                else:
                    session_data["count_incorrect"] += 1
                feedback = (f"Squat {session_data['counter']}: Feet-{fb_feet}, Knees-{fb_knees}, Back-{fb_back}")
                session_data["feedbacks"].append(feedback)
                squat_phase = 0

            current_stage = stage
            fb_feet, fb_knees = analyze_foot_knee_placement(results, stage)
            fb_back = analyze_back_position(results)
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
            )
        else:
            cv2.putText(image, "No pose detected", (10, 30),
                        FONT, 1, (0, 0, 255), 2)

        # Affichage du texte dans le header
        y_pos = 30  # Position initiale
        cv2.putText(header, f"Count: {session_data['counter']}", (10, y_pos),
                    FONT, FONT_SCALE, (255, 255, 255), FONT_THICKNESS, cv2.LINE_AA)
        y_pos += LINE_SPACING
        cv2.putText(header, f"Stage: {current_stage}", (10, y_pos),
                    FONT, FONT_SCALE, (255, 255, 255), FONT_THICKNESS, cv2.LINE_AA)
        y_pos += LINE_SPACING
        cv2.putText(header, f"Feet: {fb_feet}", (10, y_pos),
                    FONT, FONT_SCALE, (255, 255, 255), FONT_THICKNESS, cv2.LINE_AA)
        y_pos += LINE_SPACING
        cv2.putText(header, f"Knees: {fb_knees}", (10, y_pos),
                    FONT, FONT_SCALE, (255, 255, 255), FONT_THICKNESS, cv2.LINE_AA)
        y_pos += LINE_SPACING
        cv2.putText(header, f"Back: {fb_back}", (10, y_pos),
                    FONT, FONT_SCALE, (255, 255, 255), FONT_THICKNESS, cv2.LINE_AA)

        # Concaténer le header avec l'image
        final_image = cv2.vconcat([header, image])

        ret, buffer = cv2.imencode('.jpg', final_image)
        if not ret:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        if session_data["target"] > 0 and session_data["counter"] >= session_data["target"]:
            complete_session()
            print("Session terminée.")
            break

    cap.release()


@bp.route('/video_feed')
def video_feed_route():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
