import React from 'react';

export default function InstructionsCard() {
  return (
    <section className="card">
      <h2>Gesture Commands</h2>
      <ul style={{ listStyle: 'none', padding: 0, margin: 0, lineHeight: '1.8' }}>
        <li>✋ <strong>Open Palm</strong> (All 4 fingers up) — <em>Chrome</em></li>
        <li>✌️ <strong>Peace Sign</strong> (Index + Middle up) — <em>WhatsApp</em></li>
        <li>👆 <strong>Index Up</strong> (Only Index up) — <em>Camera</em></li>
        <li>🤘 <strong>Metal</strong> (Index + Pinky up) — <em>Calculator</em></li>
        <li>🤙 <strong>Pinky Up</strong> (Only Pinky up) — <em>Notepad</em></li>
        <li>👌 <strong>OK Sign</strong> (Index down, others up) — <em>Paint</em></li>
        <li>👍 <strong>Thumbs Up</strong> (Thumb up, 4 fingers down) — <em>File Explorer</em></li>
        <li>👎 <strong>Thumbs Down</strong> (Thumb down, 4 fingers down) — <em>VS Code</em></li>
      </ul>
      <p style={{ fontSize: '0.8em', marginTop: '15px', color: '#666' }}>
        * Gestures have a 3-second cooldown to prevent spam.
      </p>
    </section>
  );
}
