import React from 'react';

export default function Report({ report, onRestart }) {
  if (!report) {
    return (
      <div style={styles.container}>
        <p>Aucun rapport disponible.</p>
        <button onClick={onRestart} style={styles.button}>
          ← Retour à l’accueil
        </button>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h2>Rapport de la session</h2>
      <p><strong>Squats souhaités :</strong> {report.target}</p>
      <p><strong>Total effectués :</strong> {report.total}</p>
      <p><strong>Squats corrects :</strong> {report.correct}</p>
      <p><strong>Squats incorrects :</strong> {report.incorrect}</p>
      <p><strong>Score :</strong> {report.score}%</p>
      <p><strong>Durée (secondes) :</strong> {report.duration_seconds}</p>
      <h3>Feedbacks par squat :</h3>
      <ul style={styles.list}>
        {report.feedbacks.map((fb, i) => (
          <li key={i}>{fb}</li>
        ))}
      </ul>
      <button onClick={onRestart} style={styles.button}>
        ← Retour à l’accueil
      </button>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 600,
    margin: '2rem auto',
    padding: '1.5rem',
    border: '2px solid #fff',
    borderRadius: 8,
    backgroundColor: 'rgba(0,0,0,0.6)',
    color: '#fff',
    textAlign: 'center',
    fontFamily: 'sans-serif'
  },
  list: {
    textAlign: 'left',
    maxHeight: 200,
    overflowY: 'auto',
    margin: '1rem 0',
    paddingLeft: '1.2rem'
  },
  button: {
    marginTop: '1.5rem',
    padding: '0.75rem 1.5rem',
    fontSize: '1rem',
    cursor: 'pointer'
  }
};
