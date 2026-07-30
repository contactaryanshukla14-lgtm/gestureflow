import React, { useEffect, useState, useRef } from 'react';
import WebcamPanel from '../components/WebcamPanel';
import PredictionCard from '../components/PredictionCard';
import InstructionsCard from '../components/InstructionsCard';
import { healthCheck, inferGesture } from '../services/api';

export default function App() {
  const [prediction, setPrediction] = useState(null);
  const [status, setStatus] = useState('Checking backend...');
  const [isOnline, setIsOnline] = useState(false);
  
  const isInferring = useRef(false);

  useEffect(() => {
    let isMounted = true;
    const checkBackend = () => {
      healthCheck()
        .then(() => {
          if (isMounted) {
            setStatus('Backend online');
            setIsOnline(true);
          }
        })
        .catch(() => {
          if (isMounted) {
            setStatus('Backend offline (retrying...)');
            setIsOnline(false);
          }
        });
    };
    checkBackend();
    const interval = setInterval(checkBackend, 3000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  async function handleFrame(imageB64) {
    if (isInferring.current || !isOnline) return;
    isInferring.current = true;
    try {
      const response = await inferGesture({ image: imageB64 });
      setPrediction(response.data);
    } catch (e) {
      console.error('Inference error:', e);
    } finally {
      isInferring.current = false;
    }
  }

  return (
    <main className="layout">
      <header className="hero">
        <div>
          <h1>GestureFlow AI Cockpit</h1>
          <p>Real-time optical hand gesture automation & OS control</p>
        </div>
        <span className={`status ${!isOnline ? 'offline' : ''}`}>
          <span className="status-dot" />
          {status}
        </span>
      </header>
      
      <section className="grid main-grid">
        <div className="left-panel">
          <WebcamPanel onFrame={handleFrame} />
          <PredictionCard prediction={prediction} />
        </div>
        <div className="right-panel">
          <InstructionsCard />
        </div>
      </section>
    </main>
  );
}
