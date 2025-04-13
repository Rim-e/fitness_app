import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// Enregistrer les composants Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function ReportsDashboard({ onBackHome }) {
  const [reports, setReports] = useState([]);
  const [expandedIndex, setExpandedIndex] = useState(null);

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const res = await fetch("http://127.0.0.1:5000/all_reports");
      const data = await res.json();
      setReports(data.reports || []);
    } catch (error) {
      console.error("Erreur lors de la récupération des rapports:", error);
    }
  };

  // Préparer les données du graphique : x= index de session, y= score
  const chartData = {
    labels: reports.map((_, idx) => `Session ${idx + 1}`),
    datasets: [
      {
        label: 'Score (%)',
        data: reports.map(report => report.score),
        fill: false,
        backgroundColor: '#ff6600',
        borderColor: '#ff6600'
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        suggestedMin: 0,
        suggestedMax: 100
      }
    }
  };

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  return (
    <div className="reports-dashboard">
      <div className="dashboard-left">
        <h2>Évolution des scores</h2>
        <div className="chart-container">
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>
      <div className="dashboard-right">
        <h2>Historique des rapports</h2>
        {reports.length === 0 ? (
          <p>Aucun rapport disponible.</p>
        ) : (
          reports.map((report, idx) => (
            <div key={idx} className="report-card" onClick={() => toggleExpand(idx)}>
              <div className="report-summary">
                <p><strong>Session {idx + 1}</strong> - Score : {report.score}%</p>
              </div>
              {expandedIndex === idx && (
                <div className="report-details">
                  <p><strong>Total squats :</strong> {report.total}</p>
                  <p><strong>Corrects :</strong> {report.correct} - <strong>Incorrects :</strong> {report.incorrect}</p>
                  <p><strong>Durée :</strong> {report.duration_seconds} sec</p>
                  <h4>Feedbacks :</h4>
                  <ul className="feedback-list">
                    {report.feedbacks && report.feedbacks.map((fb, i) => (
                      <li key={i}>{fb}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))
        )}
        <button onClick={onBackHome} className="back-button">Retour à l'accueil</button>
      </div>
    </div>
  );
}

export default ReportsDashboard;
