import { useState, useEffect } from 'react'

export function useTheme() {
  const [theme, setTheme] = useState(
    localStorage.getItem('acadiq_theme') || 'dark'
  )

  useEffect(() => {
    const root = document.documentElement
    if (theme === 'dark') {
      root.classList.add('dark')
      root.classList.remove('light')
    } else {
      root.classList.add('light')
      root.classList.remove('dark')
    }
    localStorage.setItem('acadiq_theme', theme)
  }, [theme])

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark')
  }

  return { theme, toggleTheme }
}
