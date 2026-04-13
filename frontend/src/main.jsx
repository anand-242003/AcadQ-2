import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

// Apply saved theme immediately — no flash
const savedTheme = localStorage.getItem('acadiq_theme') || 'dark'
document.documentElement.classList.add(savedTheme)

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
