import React from 'react';

export default function PredictionCard({ prediction }) {
  return (
    <section className="card">
      <h2>Prediction</h2>
      <p className="big">{prediction?.label || 'none'}</p>
      <p>Confidence: {prediction?.confidence ?? 0}</p>
      <p>Action: {prediction?.action || 'No action'}</p>
    </section>
  );
}
