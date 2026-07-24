import { useEffect, useRef, useState } from 'react';

export function useWebcam() {
  const videoRef = useRef(null);
  const [error, setError] = useState('');

  useEffect(() => {
    let stream;
    async function start() {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        if (videoRef.current) videoRef.current.srcObject = stream;
      } catch (e) {
        setError(e.message || 'Unable to access webcam');
      }
    }
    start();
    return () => stream?.getTracks?.().forEach((t) => t.stop());
  }, []);

  return { videoRef, error };
}
