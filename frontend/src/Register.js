import React, { useState } from 'react';

export default function Register({ onRegister, onLoginClick }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [age, setAge] = useState("");
  const [weight, setWeight] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          password,
          age: parseInt(age, 10),
          weight: parseFloat(weight)
        })
      });
      const data = await res.json();
      if (res.ok) {
        onRegister(data.username || username);
      } else {
        alert("Erreur d'inscription: " + data.error);
      }
    } catch (error) {
      alert("Erreur de communication avec le backend");
    }
  };

  const styles = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '100vh',
      backgroundImage: 'url("/background.jpeg")',
      backgroundSize: 'cover',
      backgroundPosition: 'center'
    },
    card: {
      backgroundColor: 'rgba(0, 0, 0, 0.75)',
      padding: '40px',
      borderRadius: '10px',
      boxShadow: '0 4px 8px rgba(0,0,0,0.3)',
      maxWidth: '400px',
      width: '90%',
      textAlign: 'center',
      animation: 'fadeIn 0.5s ease-out'
    },
    header: {
      color: '#fff',
      marginBottom: '20px',
      fontSize: '1.8rem'
    },
    formGroup: {
      marginBottom: '20px',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'flex-start'
    },
    label: {
      color: '#fff',
      marginBottom: '5px',
      fontSize: '1rem'
    },
    input: {
      width: '100%',
      padding: '10px',
      borderRadius: '5px',
      border: 'none',
      fontSize: '1rem'
    },
    button: {
      width: '100%',
      padding: '12px',
      fontSize: '1rem',
      backgroundColor: '#ff6600',
      color: '#fff',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer'
    },
    switchLink: {
      marginTop: '15px',
      color: '#ff6600',
      cursor: 'pointer'
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.header}>S'inscrire</h2>
        <form onSubmit={handleSubmit}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Nom d'utilisateur</label>
            <input 
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={styles.input}
            />
          </div>
          <div style={styles.formGroup}>
            <label style={styles.label}>Mot de passe</label>
            <input 
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
            />
          </div>
          <div style={styles.formGroup}>
            <label style={styles.label}>Âge</label>
            <input 
              type="number"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              style={styles.input}
            />
          </div>
          <div style={styles.formGroup}>
            <label style={styles.label}>Poids (kg)</label>
            <input 
              type="number"
              value={weight}
              onChange={(e) => setWeight(e.target.value)}
              style={styles.input}
            />
          </div>
          <button type="submit" style={styles.button}>S'inscrire</button>
        </form>
        <p style={styles.switchLink} onClick={onLoginClick}>
          Vous avez déjà un compte ? Connectez-vous
        </p>
      </div>
    </div>
  );
}
