import React, { useEffect, useRef } from 'react';
import { useWebcam } from '../hooks/useWebcam';

export default function WebcamPanel({ onFrame }) {
  const { videoRef, error } = useWebcam();
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!onFrame) return;
    
    let interval = setInterval(() => {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      if (video && video.readyState >= 2 && canvas) {
        // Draw video frame to canvas
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Get base64 jpeg
        const dataUrl = canvas.toDataURL('image/jpeg', 0.8);
        onFrame(dataUrl);
      }
    }, 100); // 10 FPS

    return () => clearInterval(interval);
  }, [onFrame, videoRef]);

  return (
    <section className="card">
      <h2>Live Camera</h2>
      {error && <p className="error">{error}</p>}
      <video ref={videoRef} autoPlay playsInline muted className="video" />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </section>
  );
}
