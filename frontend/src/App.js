import React, { useState } from 'react';
import Home from './Home';
import Session from './Session';
import Report from './Report';
import ReportsDashboard from './ReportsDashboard';
import Login from './Login';
import Register from './Register';
import './App.css';

function App() {
  const [phase, setPhase] = useState("login");  // "login", "register", "home", "session", "report", "reports"
  const [username, setUsername] = useState("");
  const [target, setTarget] = useState(0);
  const [report, setReport] = useState(null);

  const handleLogout = () => {
    setUsername("");
    setPhase("login");
  };

  const handleViewReports = () => {
    setPhase("reports");
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>Squat Fitness</h1>
        {username && (
          <nav className="navbar">
            <span className="username">Bienvenue, {username}</span>
            <button onClick={handleViewReports} className="nav-button">Voir mes rapports</button>
            <button onClick={handleLogout} className="nav-button logout-button">Déconnexion</button>
          </nav>
        )}
      </header>

      <main className="app-main">
        {phase === "login" && (
          <Login 
            onLogin={(user) => {
              setUsername(user);
              setPhase("home");
            }}
            onRegisterClick={() => setPhase("register")}
          />
        )}
        {phase === "register" && (
          <Register
            onRegister={(user) => {
              setUsername(user);
              setPhase("home");
            }}
            onLoginClick={() => setPhase("login")}
          />
        )}
        {phase === "home" && (
          <Home 
            username={username} 
            setTarget={setTarget} 
            setPhase={setPhase}
          />
        )}
        {phase === "session" && (
          <Session 
            username={username} 
            target={target} 
            setPhase={setPhase} 
            setReport={setReport}
          />
        )}
        {phase === "report" && (
          <Report 
            report={report} 
            onRestart={() => setPhase("home")}
          />
        )}
        {phase === "reports" && (
          <ReportsDashboard onBackHome={() => setPhase("home")} />
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 Squat Fitness App</p>
      </footer>
    </div>
  );
}

export default App;
