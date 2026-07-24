import React from 'react';

export default function HistoryPanel({ logs }) {
  return (
    <section className="card">
      <h2>Recent Events</h2>
      <ul>
        {logs.map((item) => (
          <li key={item.id}>{item.predicted_label} · {item.action_triggered} · {item.confidence}</li>
        ))}
      </ul>
    </section>
  );
}
