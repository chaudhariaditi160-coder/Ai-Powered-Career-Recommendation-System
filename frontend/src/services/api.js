import axios from 'axios';

// Connect to local Flask server by default, or read deployment server url
const API_URL = import.meta.env.VITE_API_URL || 'https://ai-powered-career-recommendation-system-3.onrender.com';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to automatically append JWT bearer token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('career_ai_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle session expires or 401s
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Automatic logout on token expire/tamper
      localStorage.removeItem('career_ai_token');
      localStorage.removeItem('career_ai_user');
      if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/register') && window.location.pathname !== '/') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (name, email, password) => api.post('/api/auth/register', { name, email, password }),
  login: (email, password) => api.post('/api/auth/login', { email, password }),
  getProfile: () => api.get('/api/auth/profile'),
  updateGoal: (career_goal) => api.put('/api/auth/profile/update', { career_goal }),
};

export const assessmentAPI = {
  getQuestions: () => api.get('/assessment/questions'),
  submit: (payload) => api.post('/assessment/submit', payload),
};

export const predictAPI = {
  recommend: () => api.get('/predict/recommend'),
  saveCareer: (career_title, match_percentage) => api.post('/predict/save', { career_title, match_percentage }),
  getSaved: () => api.get('/predict/saved'),
  downloadReport: () => api.post('/predict/report/generate', {}, { responseType: 'blob' }),
  emailReport: (email) => api.post('/predict/report/email', { email }),
};

export const resumeAPI = {
  upload: (formData) => api.post('/resume/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  getLatest: () => api.get('/resume/analysis'),
};

export const roadmapAPI = {
  getRoadmap: (career) =>
  api.get(`/roadmap/generate?career=${encodeURIComponent(career)}`),
  updateProgress: (course_name, progress, status) => api.post('/roadmap/progress/update', { course_name, progress, status }),
  getAllProgress: () => api.get('/roadmap/progress'),
};

export const chatbotAPI = {
  sendMessage: (message) => api.post('/chatbot/message', { message }),
};

export const interviewAPI = {
  getQuestions: () => api.get('/interview/questions'),
  evaluate: (question_id, answer) => api.post('/interview/evaluate', { question_id, answer }),
};

export const portfolioAPI = {
  analyze: (username) => api.post('/portfolio/analyze', { username }),
};

export const notificationsAPI = {
  getNotifications: () => api.get('/notifications'),
  markRead: () => api.post('/notifications/read'),
};

export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
};

export default api;
