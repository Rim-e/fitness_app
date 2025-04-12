# app.py
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from routes import bp as routes_bp
from models import db

app = Flask(__name__)
app.secret_key = "changez_cette_valeur_pour_la_prod"
CORS(app, supports_credentials=True)

# Configuration MySQL (adaptez les identifiants)
MYSQL_USER     = "squat_user"
MYSQL_PASSWORD = "strong_password"
MYSQL_HOST     = "localhost"
MYSQL_DB       = "squat_app"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
