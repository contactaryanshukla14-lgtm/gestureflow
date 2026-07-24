import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
});

export const healthCheck = () => api.get('/api/health');
export const inferGesture = (payload) => api.post('/api/infer', payload);
export const fetchLogs = () => api.get('/api/logs/recent');
export const fetchDatasetSummary = () => api.get('/api/dataset/summary');
export default api;
