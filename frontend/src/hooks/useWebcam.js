import { useEffect, useRef, useState, useCallback } from 'react';

export function useWebcam() {
  const videoRef = useRef(null);
  const [error, setError] = useState('');
  const streamRef = useRef(null);

  const stopTracks = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
  }, []);

  const start = useCallback(async () => {
    stopTracks();
    setError('');
    try {
      // First try with standard ideal constraints
      let stream;
      try {
        stream = await navigator.mediaDevices.getUserMedia({ 
          video: { width: { ideal: 640 }, height: { ideal: 480 } }, 
          audio: false 
        });
      } catch (err) {
        // Fallback to minimal video constraint in case of resolution issues
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      }
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (e) {
      console.error('Webcam error:', e);
      if (e.name === 'NotReadableError' || e.name === 'TrackStartError' || (e.message && e.message.toLowerCase().includes('could not start'))) {
        setError('Camera is currently in use by another application (e.g., Zoom, Teams, Windows Camera, or another browser tab) or hardware is locked. Please close other camera apps and click Retry.');
      } else if (e.name === 'NotAllowedError' || e.name === 'PermissionDeniedError') {
        setError('Camera permission was denied. Please allow camera access in your browser and check Windows Privacy & Security settings.');
      } else {
        setError(e.message || e.name || 'Unable to access webcam.');
      }
    }
  }, [stopTracks]);

  useEffect(() => {
    start();
    return () => stopTracks();
  }, [start, stopTracks]);

  return { videoRef, error, retry: start };
}
