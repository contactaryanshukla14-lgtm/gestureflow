import React from 'react';

const GESTURE_LIST = [
  { icon: '✋', name: 'Open Palm', desc: 'All 4 fingers up', action: 'Chrome' },
  { icon: '✌️', name: 'Peace Sign', desc: 'Index + Middle up', action: 'WhatsApp' },
  { icon: '👆', name: 'Index Up', desc: 'Only Index up', action: 'Camera' },
  { icon: '🤘', name: 'Metal Sign', desc: 'Index + Pinky up', action: 'Calculator' },
  { icon: '🤙', name: 'Pinky Up', desc: 'Only Pinky up', action: 'Notepad' },
  { icon: '👌', name: 'OK Sign', desc: 'Thumb & Index circle', action: 'Paint' },
  { icon: '👍', name: 'Thumbs Up', desc: 'Thumb pointing up', action: 'File Explorer' },
  { icon: '👎', name: 'Thumbs Down', desc: 'Thumb pointing down', action: 'VS Code' },
];

export default function InstructionsCard() {
  return (
    <section className="card instructions-card">
      <h2>Gesture Command Directory</h2>
      <ul className="instructions-list">
        {GESTURE_LIST.map((item) => (
          <li key={item.name} className="instruction-row">
            <div className="instruction-info">
              <span className="instruction-icon">{item.icon}</span>
              <div className="instruction-text-block">
                <strong className="instruction-name">{item.name}</strong>
                <span className="instruction-desc">{item.desc}</span>
              </div>
            </div>
            <span className="instruction-action">⚡ {item.action}</span>
          </li>
        ))}
      </ul>
      <p className="cooldown-note">
        💡 <strong>Note:</strong> Automated OS commands have a 3-second cooldown between activations to prevent accidental double-triggering.
      </p>
    </section>
  );
}
