import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1/itam/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// API service functions
export const assetService = {
  getAll: () => api.get('/assets/'),
  getById: (id: number) => api.get(`/assets/${id}/`),
  create: (data: any) => api.post('/assets/', data),
  update: (id: number, data: any) => api.put(`/assets/${id}/`, data),
  delete: (id: number) => api.delete(`/assets/${id}/`),
  assign: (id: number, data: any) => api.post(`/assets/${id}/assign/`, data),
  unassign: (id: number, data: any) => api.post(`/assets/${id}/unassign/`, data),
  getHistory: (id: number) => api.get(`/assets/${id}/history/`),
}

export const categoryService = {
  getAll: () => api.get('/categories/'),
  create: (data: any) => api.post('/categories/', data),
  update: (id: number, data: any) => api.put(`/categories/${id}/`, data),
  delete: (id: number) => api.delete(`/categories/${id}/`),
}

export const locationService = {
  getAll: () => api.get('/locations/'),
  create: (data: any) => api.post('/locations/', data),
  update: (id: number, data: any) => api.put(`/locations/${id}/`, data),
  delete: (id: number) => api.delete(`/locations/${id}/`),
}

export const vendorService = {
  getAll: () => api.get('/vendors/'),
  create: (data: any) => api.post('/vendors/', data),
  update: (id: number, data: any) => api.put(`/vendors/${id}/`, data),
  delete: (id: number) => api.delete(`/vendors/${id}/`),
}

export const userService = {
  getAll: () => api.get('/users/'),
}

export const assignmentService = {
  getAll: () => api.get('/assignments/'),
  create: (data: any) => api.post('/assignments/', data),
}

export const maintenanceService = {
  getAll: () => api.get('/maintenance/'),
  create: (data: any) => api.post('/maintenance/', data),
  update: (id: number, data: any) => api.put(`/maintenance/${id}/`, data),
  delete: (id: number) => api.delete(`/maintenance/${id}/`),
}

export const dashboardService = {
  getStats: () => api.get('/dashboard/stats/'),
  getAlerts: () => api.get('/dashboard/alerts/'),
}

