import React from 'react';

const GESTURE_ICONS = {
  open_palm: '✋',
  peace: '✌️',
  index_up: '👆',
  metal: '🤘',
  pinky_up: '🤙',
  ok_sign: '👌',
  thumbs_up: '👍',
  thumbs_down: '👎',
  none: '🤖'
};

export default function PredictionCard({ prediction }) {
  const rawLabel = prediction?.label || 'none';
  const displayLabel = rawLabel !== 'none' ? rawLabel.replace('_', ' ') : 'none';
  const confidence = prediction?.confidence ?? 0;
  const confPercent = Math.round(confidence * 100);
  const action = prediction?.action && prediction.action !== 'none' ? prediction.action : 'No action';
  const icon = GESTURE_ICONS[rawLabel] || '✨';

  return (
    <section className="card">
      <h2>Prediction</h2>
      <div className="prediction-content">
        <div className="prediction-header">
          <span className="prediction-icon">{icon}</span>
          <span className="big">{displayLabel}</span>
        </div>
        
        <div className="confidence-section">
          <div className="confidence-label">
            <span>Confidence</span>
            <span className="confidence-value">{confPercent}%</span>
          </div>
          <div className="confidence-bar">
            <div className="confidence-fill" style={{ width: `${confPercent}%` }} />
          </div>
        </div>

        <div className="action-row">
          <span className="action-title">Action:</span>
          <span className={`action-pill ${action !== 'No action' ? 'active' : ''}`}>
            {action !== 'No action' ? `⚡ ${action}` : action}
          </span>
        </div>
      </div>
    </section>
  );
}
