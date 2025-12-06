import axios from 'axios';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach CSRF token on mutating requests when provided by the backend.
api.interceptors.request.use((config) => {
  const method = (config.method || 'get').toUpperCase();
  if (method === 'GET' || method === 'HEAD') {
    return config;
  }

  // Expect the backend to set a cookie like `XSRF-TOKEN=<token>`.
  if (typeof document !== 'undefined') {
    const match = document.cookie.match(/(?:^|; )XSRF-TOKEN=([^;]+)/);
    if (match) {
      const token = decodeURIComponent(match[1]);
      config.headers = config.headers || {};
      // Use the header name your backend expects.
      (config.headers as any)['X-CSRF-Token'] = token;
    }
  }

  return config;
});
