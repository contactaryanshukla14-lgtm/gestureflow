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

export default function HistoryPanel({ logs }) {
  if (!logs || logs.length === 0) {
    return (
      <section className="card">
        <h2>⏱️ Real-Time Event Audit Log</h2>
        <div style={{ textAlign: 'center', padding: '40px 20px', color: 'var(--text-muted)' }}>
          <p style={{ fontSize: '24px', marginBottom: '8px' }}>📭</p>
          <p>No gesture recognition events logged yet.</p>
          <p style={{ fontSize: '13px' }}>Perform gestures in front of the camera or use demo buttons to trigger logs.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2 style={{ margin: 0, border: 'none', padding: 0 }}>⏱️ Real-Time Event Audit Log</h2>
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)', background: 'rgba(255,255,255,0.05)', padding: '4px 12px', borderRadius: '999px' }}>
          Latest {logs.length} Events
        </span>
      </div>
      
      <ul className="history-list">
        {logs.map((item) => {
          const rawLabel = item.predicted_label || 'none';
          const icon = GESTURE_ICONS[rawLabel] || '✨';
          const conf = Math.round((item.confidence || 0) * 100);
          const timeStr = item.created_at ? new Date(item.created_at).toLocaleTimeString() : 'Just now';

          return (
            <li key={item.id} className="history-item">
              <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                <span style={{ fontSize: '24px', background: 'rgba(255,255,255,0.05)', width: '42px', height: '42px', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  {icon}
                </span>
                <div>
                  <div className="history-label">{rawLabel.replace('_', ' ')}</div>
                  <div className="history-meta">Confidence: <span style={{ color: '#34d399', fontFamily: 'JetBrains Mono, monospace' }}>{conf}%</span> · {timeStr}</div>
                </div>
              </div>
              <div className="history-action">⚡ {item.action_triggered || 'none'}</div>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
