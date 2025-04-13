import React, { useState, useEffect } from 'react';

export default function Home({ username, setTarget, setPhase }) {
  const [input, setInput] = useState("");

  // Redirige vers login si username n'est pas défini
  useEffect(() => {
    if (!username) {
      setPhase("login");
    }
  }, [username, setPhase]);

  const handleStart = async () => {
    const targetValue = parseInt(input, 10);
    if (isNaN(targetValue) || targetValue <= 0) {
      alert("Veuillez saisir un nombre positif.");
      return;
    }

    // Enregistrer l'objectif
    try {
      const resGoal = await fetch("http://localhost:5000/set_goal", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          series: 1,
          reps: targetValue,
          target: "depth"
        })
      });
      if (!resGoal.ok) {
        const err = await resGoal.json();
        alert("Erreur goal: " + err.error);
        return;
      }
    } catch (err) {
      alert("Erreur de communication pour l'objectif.");
      return;
    }

    // Démarrer la session
    try {
      const res = await fetch("http://localhost:5000/start_session", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target: targetValue })
      });
      const data = await res.json();
      if (res.ok) {
        setTarget(targetValue);
        setPhase("session");
      } else {
        alert("Erreur session: " + data.error);
      }
    } catch (err) {
      alert("Erreur de communication avec le backend.");
    }
  };

  const styles = {
    page: {
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      backgroundImage: 'url("/Background.jpg")',
      backgroundSize: 'cover',
      backgroundPosition: 'center'
    },
    overlay: {
      backgroundColor: 'rgba(0, 0, 0, 0.6)',
      padding: '20px',
      borderRadius: '10px',
      boxShadow: '0 4px 8px rgba(0,0,0,0.3)',
      maxWidth: '500px',
      textAlign: 'center',
      animation: 'fadeIn 0.5s ease-out'
    },
    hero: {
      marginBottom: '20px'
    },
    heroTitle: {
      fontSize: '2rem',
      marginBottom: '10px'
    },
    heroSubtitle: {
      fontSize: '1rem',
      fontStyle: 'italic'
    },
    formGroup: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center'
    },
    label: {
      fontSize: '1.2rem',
      marginBottom: '10px'
    },
    input: {
      padding: '10px',
      fontSize: '1rem',
      width: '80%',
      marginBottom: '20px',
      borderRadius: '5px',
      border: 'none'
    },
    button: {
      padding: '12px 24px',
      fontSize: '1rem',
      backgroundColor: '#ff6600',
      color: '#fff',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
      transition: 'background-color 0.3s ease'
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.overlay}>
        <div style={styles.hero}>
          <h1 style={styles.heroTitle}>“The only bad workout is the one that didn’t happen.”</h1>
          <p style={styles.heroSubtitle}>- AMOA</p>
        </div>
        <div style={styles.formGroup}>
          <label style={styles.label}>Nombre de squats souhaité :</label>
          <input
            type="number"
            value={input}
            onChange={e => setInput(e.target.value)}
            style={styles.input}
          />
          <button onClick={handleStart} style={styles.button}>
            Activer la caméra
          </button>
        </div>
      </div>
    </div>
  );
}
