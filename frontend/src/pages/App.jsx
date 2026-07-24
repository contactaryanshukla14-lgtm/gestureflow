import React, { useEffect, useState, useRef } from 'react';
import WebcamPanel from '../components/WebcamPanel';
import PredictionCard from '../components/PredictionCard';
import InstructionsCard from '../components/InstructionsCard';
import { healthCheck, inferGesture } from '../services/api';

export default function App() {
  const [prediction, setPrediction] = useState(null);
  const [status, setStatus] = useState('Checking backend...');
  
  const isInferring = useRef(false);

  useEffect(() => {
    healthCheck().then(() => setStatus('Backend online')).catch(() => setStatus('Backend offline'));
  }, []);

  async function handleFrame(imageB64) {
    if (isInferring.current) return;
    isInferring.current = true;
    try {
      const response = await inferGesture({ image: imageB64 });
      setPrediction(response.data);
    } catch (e) {
      console.error(e);
    } finally {
      isInferring.current = false;
    }
  }

  return (
    <main className="layout">
      <header className="hero">
        <div>
          <h1>GestureFlow</h1>
          <p>Human-computer interaction with real-time gesture recognition.</p>
        </div>
        <span className="status">{status}</span>
      </header>
      <section className="grid" style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px' }}>
        <WebcamPanel onFrame={handleFrame} />
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <PredictionCard prediction={prediction} />
          <InstructionsCard />
        </div>
      </section>
    </main>
  );
}
