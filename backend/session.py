# session.py
import time

# Dictionnaire pour la session en cours
session_data = {
    "target": 0,
    "counter": 0,
    "count_correct": 0,
    "count_incorrect": 0,
    "feedbacks": [],
    "start_time": None,
    "end_time": None
}

# Liste globale pour stocker tous les rapports de session
all_session_reports = []

def start_session(target: int):
    session_data["target"] = target
    session_data["counter"] = 0
    session_data["count_correct"] = 0
    session_data["count_incorrect"] = 0
    session_data["feedbacks"] = []
    session_data["start_time"] = time.time()
    session_data["end_time"] = None
    print(f"Session started: target = {target} squats.")

def complete_session():
    session_data["end_time"] = time.time()
    # Sauvegarder le rapport courant dans la liste des rapports
    report = get_report()
    all_session_reports.append(report)
    print("Session completed. Report saved.")

def get_report() -> dict:
    total = session_data["counter"]
    correct = session_data["count_correct"]
    incorrect = session_data["count_incorrect"]
    score = (correct / total * 100) if total > 0 else 0
    duration = session_data["end_time"] - session_data["start_time"] if session_data["end_time"] else None
    return {
        "target": session_data["target"],
        "total": total,
        "correct": correct,
        "incorrect": incorrect,
        "score": round(score, 2),
        "duration_seconds": round(duration, 2) if duration else None,
        "feedbacks": session_data["feedbacks"]
    }


def logout_session():
    # Réinitialise session_data (vous pouvez adapter si vous avez plus de logique de session)
    session_data["target"] = 0
    session_data["counter"] = 0
    session_data["count_correct"] = 0
    session_data["count_incorrect"] = 0
    session_data["feedbacks"] = []
    session_data["start_time"] = None
    session_data["end_time"] = None
    print("Session logged out.")
