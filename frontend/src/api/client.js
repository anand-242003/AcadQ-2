import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({ baseURL: API_BASE })

// Attach JWT to every request automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('acadiq_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login:    (data) => api.post('/auth/login', data),
  me:       ()     => api.get('/auth/me'),
}

export const predictAPI = {
  predict: (data) => api.post('/predict', data),
}

export const coachAPI = {
  chat:     (data)  => api.post('/coach/chat', data),
  plan:     (data)  => api.post('/coach/plan', data),
  diagnose: (data)  => api.post('/coach/diagnose', data),
  reset:    ()      => api.delete('/coach/reset'),
}

export default api
