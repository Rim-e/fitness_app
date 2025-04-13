import React, { useEffect } from 'react';

function Session({ target, setPhase, setReport }) {
  const fetchReport = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/get_report");
      const data = await res.json();
      if (data.duration_seconds) {
        setReport(data);
        setPhase("report");
      }
    } catch (err) {
      console.error("Erreur lors de la récupération du rapport", err);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      fetchReport();
    }, 2000);
    return () => clearInterval(interval);
  }, [setPhase, setReport]);

  return (
    <div className="session-container">
      <h2>Session en cours : {target} squats souhaités</h2>
      <div className="video-container">
        <img 
          src="http://127.0.0.1:5000/video_feed" 
          alt="Flux de détection en direct" 
          className="video-feed"
        />
      </div>
      <p>Effectuez vos squats. La session s'arrêtera automatiquement une fois le nombre cible atteint.</p>
    </div>
  );
}

export default Session;