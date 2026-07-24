import React from 'react';

export default function ControlsPanel({ onInfer }) {
  const demoSamples = [
    'open_palm', 'fist', 'thumbs_up', 'peace', 'ok', 'point_left', 'point_right', 'stop'
  ];

  return (
    <section className="card">
      <h2>Demo Controls</h2>
      <div className="buttonGrid">
        {demoSamples.map((label) => (
          <button key={label} onClick={() => onInfer(label)}>{label}</button>
        ))}
      </div>
    </section>
  );
}
