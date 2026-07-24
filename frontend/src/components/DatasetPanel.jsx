import React from 'react';

export default function DatasetPanel({ summary }) {
  return (
    <section className="card">
      <h2>Dataset Summary</h2>
      <ul>
        {Object.entries(summary).map(([label, count]) => (
          <li key={label}>{label}: {count}</li>
        ))}
      </ul>
    </section>
  );
}
