/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        display: ['Clash Display', 'sans-serif'],
        body: ['Satoshi', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        'bg-primary': '#0A0A0F',
        'bg-secondary': '#111118',
        'bg-card': '#16161F',
        'border-subtle': '#1E1E2E',
        'accent-primary': '#6C63FF',
        'accent-secondary': '#00D4AA',
        'accent-danger': '#FF4D6D',
        'accent-warm': '#FFB347',
        'text-primary': '#F0EEF8',
        'text-secondary': '#8B8AA0',
        'text-muted': '#4A4A6A',
      },
      animation: {
        'fade-slide-up': 'fadeSlideUp 0.5s ease forwards',
        'slide-in-left': 'slideInLeft 0.3s ease forwards',
        'slide-in-right': 'slideInRight 0.3s ease forwards',
        'bounce-dot': 'bounceDot 1.4s ease-in-out infinite',
        'pulse-dot': 'pulseDot 2s ease-in-out infinite',
      },
      keyframes: {
        fadeSlideUp: {
          'from': { opacity: '0', transform: 'translateY(24px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInLeft: {
          'from': { opacity: '0', transform: 'translateX(-16px)' },
          'to': { opacity: '1', transform: 'translateX(0)' },
        },
        slideInRight: {
          'from': { opacity: '0', transform: 'translateX(16px)' },
          'to': { opacity: '1', transform: 'translateX(0)' },
        },
        bounceDot: {
          '0%, 80%, 100%': { transform: 'scale(0)' },
          '40%': { transform: 'scale(1)' },
        },
        pulseDot: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3' },
        },
      },
    },
  },
  plugins: [],
}
