# models.py
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.linear_model import LogisticRegression

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(64), primary_key=True)
    pw_hash  = db.Column(db.Text, nullable=False)
    age      = db.Column(db.Integer)
    weight   = db.Column(db.Float)
    goal     = db.relationship('Goal', backref='user', uselist=False)

class Goal(db.Model):
    __tablename__ = 'goals'
    id       = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), db.ForeignKey('users.username'), nullable=False)
    series   = db.Column(db.Integer)
    reps     = db.Column(db.Integer)
    target   = db.Column(db.String(32))

# Pour la classification, on utilise 9 landmarks (soit 36 features)
CLASSIFIER_LMS = [
    "NOSE", "LEFT_SHOULDER", "RIGHT_SHOULDER",
    "LEFT_HIP", "RIGHT_HIP", "LEFT_KNEE",
    "RIGHT_KNEE", "LEFT_ANKLE", "RIGHT_ANKLE"
]
CLASSIFIER_HEADERS = []
for lm in CLASSIFIER_LMS:
    CLASSIFIER_HEADERS += [f"{lm.lower()}_x", f"{lm.lower()}_y", f"{lm.lower()}_z", f"{lm.lower()}_v"]

def load_trained_model(csv_path="train.csv") -> LogisticRegression:
    df = pd.read_csv(csv_path)
    df["label"] = df["label"].map({"down": 0, "up": 1})
    missing = [col for col in CLASSIFIER_HEADERS if col not in df.columns]
    if missing:
        raise Exception(f"Dataset missing columns: {missing}")
    X = df[CLASSIFIER_HEADERS]
    y = df["label"]
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    score = model.score(X, y)
    print("Model trained (score):", score)
    return model

# Charger le modèle pour le comptage (accessible globalement)
count_model = load_trained_model()
