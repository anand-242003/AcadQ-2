import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'

const Landing    = lazy(() => import('./pages/Landing'))
const Auth       = lazy(() => import('./pages/Auth'))
const InputForm  = lazy(() => import('./pages/InputForm'))
const Results    = lazy(() => import('./pages/Results'))
const StudyCoach = lazy(() => import('./pages/StudyCoach'))
const QuizBot    = lazy(() => import('./pages/QuizBot'))
const History    = lazy(() => import('./pages/History'))

function PageLoader() {
  return (
    <div className="min-h-screen bg-[#0A0A0F] flex items-center justify-center">
      <div className="w-10 h-10 rounded-full border-4 border-[#6C63FF]/30 border-t-[#6C63FF] animate-spin" />
    </div>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <Suspense fallback={<PageLoader />}>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/auth" element={<Auth />} />
            <Route path="/input" element={<ProtectedRoute><InputForm /></ProtectedRoute>} />
            <Route path="/results" element={<ProtectedRoute><Results /></ProtectedRoute>} />
            <Route path="/coach" element={<ProtectedRoute><StudyCoach /></ProtectedRoute>} />
            <Route path="/quiz" element={<ProtectedRoute><QuizBot /></ProtectedRoute>} />
            <Route path="/history" element={<ProtectedRoute><History /></ProtectedRoute>} />
          </Routes>
        </Suspense>
      </BrowserRouter>
    </AuthProvider>
  )
}
