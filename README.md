# Squat Fitness

Squat Fitness est une application complète qui aide les utilisateurs à améliorer leur technique de squat grâce à une analyse en temps réel via la caméra. L'application fournit un feedback technique sur le placement des pieds, l'espacement des genoux et la position du dos, tout en comptabilisant automatiquement les squats effectués et en stockant l'historique des sessions.

---

## Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Architecture du Projet](#architecture-du-projet)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Technologies Utilisées](#technologies-utilisées)
- [Installation et Lancement](#installation-et-lancement)
  - [Backend](#installation-backend)
  - [Frontend](#installation-frontend)
- [Utilisation](#utilisation)



---

## Fonctionnalités

- **Détection en Temps Réel**  
  Analyse la pose de squat via la caméra et Mediapipe.
  
- **Feedback Technique**  
  Fournit un retour instantané sur :
  - **Feet (Pieds) :** Vérifie que la distance entre les pieds et la largeur des épaules est optimale.
  - **Knees (Genoux) :** Évalue l'espacement des genoux par rapport aux pieds en fonction de la phase (UP, MIDDLE, DOWN).
  - **Back (Dos) :** Vérifie que la position du dos est correcte en comparant la profondeur des épaules et des hanches.

- **Comptage Automatique**  
  Détecte les cycles complets "down → up" pour incrémenter le nombre de squats et fournit des feedbacks détaillés.

- **Historique des Sessions**  
  Enregistre un rapport de session complet (nombre de squats, score, durée, feedbacks) et permet de consulter l'historique.

- **Application Mobile Hybride**  
  Le frontend web (développé en React) est converti en application mobile Android via Capacitor.

---

## Architecture du Projet

### Backend

Le backend est structuré de façon modulaire et se compose des fichiers suivants :

- **models.py**  
  - **User:** Stocke les informations utilisateur (username, mot de passe haché, âge, poids).  
  - **Goal:** Définit les objectifs d'exercice (séries, répétitions, cible) pour un utilisateur.
  - **Machine Learning:**  
    - Définit les constantes `CLASSIFIER_LMS` et `CLASSIFIER_HEADERS` qui permettent de préparer les données pour la classification.  
    - La fonction `load_trained_model()` charge un modèle de régression logistique entraîné sur un dataset (train.csv) afin d’identifier les phases "down" et "up".
  
- **detection.py**  
  - **calculate_distance():** Calcule la distance Euclidienne entre deux points 2D.  
  - **extract_keypoints():** Extrait les coordonnées (x, y, z) et la visibilité des landmarks spécifiés.  
  - **analyze_foot_knee_placement():** Calcule des ratios pour évaluer la position des pieds (ratio feet/shoulder) et des genoux (ratio knees/foot), avec des seuils ajustés pour différentes phases du squat (UP, MIDDLE, DOWN).  
  - **analyze_back_position():** Compare la profondeur (coordonnée z) des épaules et des hanches pour détecter si le dos est trop penché.
  
- **session.py**  
  - Gère l’état d’une session d'exercice via un dictionnaire global `session_data` (comprenant le nombre de squats, le feedback, la durée, etc.).
  - Fonctions principales :
    - `start_session(target)`: Initialise une nouvelle session.
    - `complete_session()`: Marque la fin d'une session et enregistre le rapport dans `all_session_reports`.
    - `get_report()`: Compile et retourne un rapport détaillé de la session.
    - `logout_session()`: Réinitialise l'état de la session.
  
- **routes.py**  
  - Définit l’ensemble des endpoints REST pour l’authentification, la gestion des objectifs, le streaming vidéo (avec la fonction `generate_frames()` qui intègre la détection de pose et le feedback en temps réel) et la consultation des rapports.
  
- **app.py**  
  - Point d'entrée de l’application Flask.
  - Configure CORS, SQLAlchemy et la connexion à la base de données MySQL.
  - Enregistre le blueprint des routes.

### Frontend

Le frontend est développé en React et se compose des principaux fichiers suivants :

- **App.js**  
  Gère la navigation entre les différentes phases (login, register, home, session, reports).
  
- **Home.js**  
  Permet à l'utilisateur de définir ses objectifs et affiche une interface inspirante.
  
- **Login.js et Register.js**  
  Fournissent des pages de connexion et d'inscription modernes et élégantes.
  
- **Session.js**  
  Affiche le flux vidéo en temps réel avec le feedback (Count, Stage, Feet, Knees, Back).
  
- **ReportsDashboard.js**  
  Permet de consulter l’historique des rapports et présente un graphique d'évolution des performances.
  
- **App.css**  
  Définit les styles globaux pour une interface cohérente avec le thème fitness.

---

## Technologies Utilisées

- **Backend :**  
  - Python, Flask, SQLAlchemy, Mediapipe, scikit-learn, Pandas  
- **Frontend :**  
  - React, HTML, CSS

---

## Utilisation

- **Authentification:** Créez un compte, connectez-vous et déconnectez-vous via l'interface.

- **Configuration d'Objectifs:** Définissez le nombre de squats souhaité.

- **Session en Direct:** La caméra capture la pose et fournit un feedback en temps réel sur le placement des pieds, des genoux et la position du dos, tout en comptant les squats.

- **Historique:** Consultez les rapports détaillés après chaque session pour suivre votre progression.





