import { useState } from 'react'
import { useNavigate, Navigate } from 'react-router-dom'
import { Eye, EyeOff, Mail, Lock, User, Sparkles, CheckCircle2 } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { authAPI } from '../api/client'
import Toast from '../components/Toast'

function PasswordStrength({ password }) {
  if (!password) return null

  const getStrength = (p) => {
    if (p.length < 6) return { score: 1, label: 'Weak', color: '#FF4D6D' }
    if (p.length < 8 || !(/[A-Za-z]/.test(p) && /[0-9]/.test(p))) return { score: 2, label: 'Fair', color: '#FF8C42' }
    if (p.length >= 10 && /[A-Z]/.test(p) && /[0-9]/.test(p) && /[^A-Za-z0-9]/.test(p)) return { score: 4, label: 'Strong', color: '#00D4AA' }
    return { score: 3, label: 'Good', color: '#FFB347' }
  }

  const { score, label, color } = getStrength(password)

  return (
    <div className="space-y-1.5">
      <div className="flex gap-1">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="flex-1 h-1 rounded-full transition-all duration-300"
            style={{ backgroundColor: i <= score ? color : 'var(--border)' }} />
        ))}
      </div>
      <div className="flex justify-end">
        <p className="text-xs font-medium" style={{ color }}>{label} password</p>
      </div>
    </div>
  )
}

function InputField({ icon: Icon, type = 'text', placeholder, value, onChange, error, rightElement }) {
  return (
    <div>
      <div className={`flex items-center gap-3 bg-[var(--bg-card)] border rounded-xl px-4 py-3 transition-colors ${
        error ? 'border-[#FF4D6D]' : 'border-[var(--border)] focus-within:border-[#6C63FF]'
      }`}>
        <Icon size={16} className="text-[var(--text-muted)] flex-shrink-0" />
        <input
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          className="flex-1 bg-transparent text-[var(--text-primary)] placeholder:text-[var(--text-muted)] text-sm outline-none"
        />
        {rightElement}
      </div>
      {error && <p className="text-[#FF4D6D] text-xs mt-1">{error}</p>}
    </div>
  )
}

export default function Auth() {
  const { login, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const [tab, setTab] = useState('login')
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState({ message: '', type: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  const [loginData, setLoginData] = useState({ email: '', password: '' })
  const [loginErrors, setLoginErrors] = useState({})

  const [registerData, setRegisterData] = useState({ name: '', email: '', password: '', confirm: '' })
  const [registerErrors, setRegisterErrors] = useState({})

  if (isAuthenticated) return <Navigate to="/input" replace />

  const showToast = (message, type = 'success') => setToast({ message, type })

  const handleLogin = async (e) => {
    e.preventDefault()
    const errors = {}
    if (!loginData.email) errors.email = 'Email is required'
    if (!loginData.password) errors.password = 'Password is required'
    if (Object.keys(errors).length) { setLoginErrors(errors); return }

    setLoading(true)
    setLoginErrors({})
    try {
      const { data } = await authAPI.login({ email: loginData.email, password: loginData.password })
      login(data.token, { name: data.name, email: data.email })
      showToast('Welcome back! Redirecting...', 'success')
      setTimeout(() => navigate('/input'), 800)
    } catch (err) {
      const msg = err.response?.data?.detail || 'Login failed. Please try again.'
      setLoginErrors({ general: msg })
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    const errors = {}
    if (!registerData.name || registerData.name.length < 2) errors.name = 'Name must be at least 2 characters'
    if (!registerData.email) errors.email = 'Email is required'
    if (!registerData.password || registerData.password.length < 8) errors.password = 'Password must be at least 8 characters'
    if (registerData.password !== registerData.confirm) errors.confirm = 'Passwords do not match'
    if (Object.keys(errors).length) { setRegisterErrors(errors); return }

    setLoading(true)
    setRegisterErrors({})
    try {
      const { data } = await authAPI.register({
        name: registerData.name,
        email: registerData.email,
        password: registerData.password,
      })
      login(data.token, { name: data.name, email: data.email })
      showToast('Account created! Redirecting...', 'success')
      setTimeout(() => navigate('/input'), 800)
    } catch (err) {
      const msg = err.response?.data?.detail || 'Registration failed. Please try again.'
      if (msg.toLowerCase().includes('email')) {
        setRegisterErrors({ email: msg })
      } else {
        setRegisterErrors({ general: msg })
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] flex" style={{ fontFamily: 'Satoshi, sans-serif' }}>
      <Toast message={toast.message} type={toast.type} onClose={() => setToast({ message: '', type: '' })} />

      {/* Left decorative panel */}
      <div className="hidden lg:flex lg:w-1/2 bg-[var(--bg-secondary)] relative overflow-hidden flex-col items-center justify-center p-12">
        <div className="absolute inset-0 pointer-events-none"
          style={{ background: 'radial-gradient(ellipse 60% 60% at 50% 50%, rgba(108,99,255,0.2) 0%, transparent 70%)' }} />
        <div className="relative z-10 text-center max-w-sm">
          <div className="flex items-center justify-center gap-2 mb-12">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#6C63FF] to-[#00D4AA] flex items-center justify-center">
              <Sparkles size={20} className="text-white" />
            </div>
            <span className="text-2xl font-bold text-[var(--text-primary)]" style={{ fontFamily: 'Clash Display, sans-serif' }}>AcadIQ</span>
          </div>
          <blockquote className="text-4xl font-bold text-[var(--text-primary)] mb-8 leading-tight" style={{ fontFamily: 'Clash Display, sans-serif' }}>
            "Know before you go."
          </blockquote>
          <ul className="space-y-4 text-left">
            {['Predict your exam score before it happens', 'Get a personalized AI study coach', 'Understand your learner archetype'].map(item => (
              <li key={item} className="flex items-center gap-3 text-sm text-[var(--text-secondary)]">
                <div className="w-5 h-5 rounded-full bg-[#6C63FF]/20 flex items-center justify-center flex-shrink-0">
                  <CheckCircle2 size={12} className="text-[#6C63FF]" />
                </div>
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Right form panel */}
      <div className="flex-1 flex items-center justify-center px-6 py-12 bg-[var(--bg-primary)]">
        <div className="w-full max-w-md">
          <div className="flex items-center gap-2 mb-8 lg:hidden">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#6C63FF] to-[#00D4AA] flex items-center justify-center">
              <Sparkles size={16} className="text-white" />
            </div>
            <span className="text-xl font-bold text-[var(--text-primary)]" style={{ fontFamily: 'Clash Display, sans-serif' }}>AcadIQ</span>
          </div>

          <div className="flex border-b border-[var(--border)] mb-8">
            {['login', 'register'].map(t => (
              <button key={t} onClick={() => setTab(t)}
                className={`pb-3 px-1 mr-6 text-sm font-medium capitalize transition-colors border-b-2 -mb-px ${
                  tab === t ? 'border-[#6C63FF] text-[#6C63FF]' : 'border-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
                }`}>
                {t === 'login' ? 'Login' : 'Register'}
              </button>
            ))}
          </div>

          {tab === 'login' && (
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-1" style={{ fontFamily: 'Clash Display, sans-serif' }}>Welcome back</h2>
                <p className="text-sm text-[var(--text-secondary)]">Sign in to your AcadIQ account</p>
              </div>
              {loginErrors.general && (
                <div className="px-4 py-3 bg-[#FF4D6D]/10 border border-[#FF4D6D]/30 rounded-xl text-sm text-[#FF4D6D]">{loginErrors.general}</div>
              )}
              <InputField icon={Mail} type="email" placeholder="Email address" value={loginData.email}
                onChange={e => setLoginData(p => ({ ...p, email: e.target.value }))} error={loginErrors.email} />
              <InputField icon={Lock} type={showPassword ? 'text' : 'password'} placeholder="Password"
                value={loginData.password} onChange={e => setLoginData(p => ({ ...p, password: e.target.value }))}
                error={loginErrors.password}
                rightElement={
                  <button type="button" onClick={() => setShowPassword(!showPassword)} className="text-[var(--text-muted)] hover:text-[var(--text-secondary)]">
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                } />
              <div className="flex justify-end">
                <button type="button" className="text-xs text-[var(--text-secondary)] hover:text-[#6C63FF] transition-colors">Forgot password?</button>
              </div>
              <button type="submit" disabled={loading}
                className="w-full py-3.5 bg-[#6C63FF] hover:bg-[#5B52EE] disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-colors text-sm">
                {loading ? 'Signing in...' : 'Sign In →'}
              </button>
              <p className="text-center text-sm text-[var(--text-secondary)]">
                Don't have an account?{' '}
                <button type="button" onClick={() => setTab('register')} className="text-[#6C63FF] hover:underline">Register</button>
              </p>
            </form>
          )}

          {tab === 'register' && (
            <form onSubmit={handleRegister} className="space-y-4">
              <div>
                <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-1" style={{ fontFamily: 'Clash Display, sans-serif' }}>Create account</h2>
                <p className="text-sm text-[var(--text-secondary)]">Start your AI-powered learning journey</p>
              </div>
              {registerErrors.general && (
                <div className="px-4 py-3 bg-[#FF4D6D]/10 border border-[#FF4D6D]/30 rounded-xl text-sm text-[#FF4D6D]">{registerErrors.general}</div>
              )}
              <InputField icon={User} placeholder="Full name" value={registerData.name}
                onChange={e => setRegisterData(p => ({ ...p, name: e.target.value }))} error={registerErrors.name} />
              <InputField icon={Mail} type="email" placeholder="Email address" value={registerData.email}
                onChange={e => setRegisterData(p => ({ ...p, email: e.target.value }))} error={registerErrors.email} />
              <InputField icon={Lock} type={showPassword ? 'text' : 'password'} placeholder="Password (min 8 characters)"
                value={registerData.password} onChange={e => setRegisterData(p => ({ ...p, password: e.target.value }))}
                error={registerErrors.password}
                rightElement={
                  <button type="button" onClick={() => setShowPassword(!showPassword)} className="text-[var(--text-muted)] hover:text-[var(--text-secondary)]">
                    {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                } />
              <PasswordStrength password={registerData.password} />
              <InputField icon={Lock} type={showConfirm ? 'text' : 'password'} placeholder="Confirm password"
                value={registerData.confirm} onChange={e => setRegisterData(p => ({ ...p, confirm: e.target.value }))}
                error={registerErrors.confirm}
                rightElement={
                  <button type="button" onClick={() => setShowConfirm(!showConfirm)} className="text-[var(--text-muted)] hover:text-[var(--text-secondary)]">
                    {showConfirm ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                } />
              <button type="submit" disabled={loading}
                className="w-full py-3.5 bg-[#6C63FF] hover:bg-[#5B52EE] disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold rounded-xl transition-colors text-sm">
                {loading ? 'Creating account...' : 'Create Account →'}
              </button>
              <p className="text-center text-sm text-[var(--text-secondary)]">
                Already have an account?{' '}
                <button type="button" onClick={() => setTab('login')} className="text-[#6C63FF] hover:underline">Login</button>
              </p>
            </form>
          )}
        </div>
      </div>
    </div>
  )
}
