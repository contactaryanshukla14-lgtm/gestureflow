import React from 'react';

const DEMO_SAMPLES = [
  { label: 'open_palm', name: '✋ Open Palm' },
  { label: 'peace', name: '✌️ Peace Sign' },
  { label: 'index_up', name: '👆 Index Up' },
  { label: 'metal', name: '🤘 Metal Sign' },
  { label: 'pinky_up', name: '🤙 Pinky Up' },
  { label: 'ok_sign', name: '👌 OK Sign' },
  { label: 'thumbs_up', name: '👍 Thumbs Up' },
  { label: 'thumbs_down', name: '👎 Thumbs Down' },
  { label: 'none', name: '🤖 Clear / Idle' }
];

export default function ControlsPanel({ onInfer }) {
  return (
    <section className="card">
      <h2>🎮 Cyber-Deck Simulator Controls</h2>
      <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '16px' }}>
        No webcam available or want to test OS automation commands instantly? Click any gesture button below to simulate an optical detection feed:
      </p>
      <div className="buttonGrid">
        {DEMO_SAMPLES.map((item) => (
          <button 
            key={item.label} 
            className="demo-btn"
            onClick={() => onInfer(item.label)}
          >
            {item.name}
          </button>
        ))}
      </div>
    </section>
  );
}
