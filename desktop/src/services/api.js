import axios from 'axios';

// Backend API URL - can be configured via environment variable
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8002';

// Create axios instance with defaults
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

// API Service Methods
export const apiService = {
  // Health Check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Jobs
  getJobs: async () => {
    const response = await api.get('/api/jobs');
    return response.data;
  },

  getJob: async (jobId) => {
    const response = await api.get(`/api/jobs/${jobId}`);
    return response.data;
  },

  createJob: async (jobData) => {
    const response = await api.post('/api/jobs', jobData);
    return response.data;
  },

  updateJob: async (jobId, jobData) => {
    const response = await api.put(`/api/jobs/${jobId}`, jobData);
    return response.data;
  },

  deleteJob: async (jobId) => {
    const response = await api.delete(`/api/jobs/${jobId}`);
    return response.data;
  },

  // Rooms
  getRooms: async (jobId) => {
    const response = await api.get(`/api/jobs/${jobId}/rooms`);
    return response.data;
  },

  getRoom: async (roomId) => {
    const response = await api.get(`/api/rooms/${roomId}`);
    return response.data;
  },

  classifyRoom: async (formData) => {
    const response = await api.post('/api/rooms/classify', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  updateRoomClassification: async (roomId, classificationData) => {
    const response = await api.put(`/api/rooms/${roomId}/classification`, classificationData);
    return response.data;
  },

  // Customers
  getCustomers: async () => {
    const response = await api.get('/api/customers');
    return response.data;
  },

  createCustomer: async (customerData) => {
    const response = await api.post('/api/customers', customerData);
    return response.data;
  },

  // Invoices
  getInvoices: async (jobId) => {
    const response = await api.get(`/api/jobs/${jobId}/invoices`);
    return response.data;
  },

  generateInvoice: async (jobId) => {
    const response = await api.post(`/api/jobs/${jobId}/invoice`);
    return response.data;
  },
};

export default api;
