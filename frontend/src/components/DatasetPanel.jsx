import React from 'react';

const GESTURE_NAMES = {
  open_palm: '✋ Open Palm',
  peace: '✌️ Peace Sign',
  index_up: '👆 Index Up',
  metal: '🤘 Metal Sign',
  pinky_up: '🤙 Pinky Up',
  ok_sign: '👌 OK Sign',
  thumbs_up: '👍 Thumbs Up',
  thumbs_down: '👎 Thumbs Down',
  none: '🤖 None (Idle)'
};

export default function DatasetPanel({ summary }) {
  const totalSamples = Object.values(summary || {}).reduce((acc, val) => acc + (typeof val === 'number' ? val : 0), 0);

  return (
    <section className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2 style={{ margin: 0, border: 'none', padding: 0 }}>📊 Training Dataset Summary</h2>
        <span style={{ fontSize: '14px', fontWeight: 'bold', color: '#34d399', background: 'rgba(52, 211, 153, 0.15)', padding: '6px 14px', borderRadius: '999px', border: '1px solid rgba(52, 211, 153, 0.3)' }}>
          Total Samples: {totalSamples}
        </span>
      </div>

      <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '24px' }}>
        Overview of captured raw image samples available in <code style={{ color: '#38bdf8', background: 'rgba(255,255,255,0.08)', padding: '2px 6px', borderRadius: '6px' }}>ml/data/raw</code> for training custom recognizer models:
      </p>

      <div className="dataset-stats">
        {Object.entries(summary || {}).map(([label, count]) => {
          const displayName = GESTURE_NAMES[label] || label.replace('_', ' ');
          return (
            <div key={label} className="stat-box">
              <div className="stat-num">{count}</div>
              <div className="stat-name">{displayName}</div>
            </div>
          );
        })}
      </div>

      <div style={{ marginTop: '24px', padding: '16px', background: 'rgba(56, 189, 248, 0.1)', border: '1px solid rgba(56, 189, 248, 0.25)', borderRadius: '16px', display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span style={{ fontSize: '24px' }}>🚀</span>
        <div style={{ fontSize: '13px', color: '#bae6fd' }}>
          <strong>Custom Model Training:</strong> Want to train or re-train your own classifier on these samples? Run <code style={{ background: 'rgba(0,0,0,0.3)', padding: '2px 8px', borderRadius: '4px', fontFamily: 'JetBrains Mono, monospace', color: '#38bdf8' }}>python ml/scripts/train_model.py</code> from the project root!
        </div>
      </div>
    </section>
  );
}
