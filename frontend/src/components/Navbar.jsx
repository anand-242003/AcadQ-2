import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { Sparkles, LogOut, ChevronDown, BarChart2, MessageSquare, BookOpen } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [scrolled, setScrolled] = useState(false)
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const dropdownRef = useRef(null)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50)
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target)) {
        setDropdownOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleLogout = () => {
    logout()
    setDropdownOpen(false)
    navigate('/')
  }

  const initials = user?.name
    ? user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    : 'U'

  const isActive = (path) => location.pathname === path

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      scrolled
        ? 'bg-[var(--bg-primary)]/90 backdrop-blur-md border-b border-[var(--border)]/50'
        : 'bg-transparent'
    }`}>
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#6C63FF] to-[#00D4AA] flex items-center justify-center">
            <Sparkles size={16} className="text-white" />
          </div>
          <span className="text-xl font-bold text-[var(--text-primary)]" style={{ fontFamily: 'Clash Display, sans-serif' }}>
            AcadIQ
          </span>
        </Link>

        {/* Right side */}
        <div className="flex items-center gap-3">

          {isAuthenticated ? (
            <>
              {/* Nav links */}
              <div className="hidden md:flex items-center gap-1">
                <Link to="/input" className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${
                  isActive('/input') ? 'bg-[#6C63FF]/20 text-[#6C63FF]' : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'
                }`}>
                  <BarChart2 size={15} /> Analyze
                </Link>
                <Link to="/results" className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive('/results') ? 'bg-[#6C63FF]/20 text-[#6C63FF]' : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'
                }`}>
                  Results
                </Link>
                <Link to="/coach" className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${
                  isActive('/coach') ? 'bg-[#6C63FF]/20 text-[#6C63FF]' : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'
                }`}>
                  <MessageSquare size={15} /> Coach
                </Link>
                <Link to="/quiz" className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${
                  isActive('/quiz') ? 'bg-[#6C63FF]/20 text-[#6C63FF]' : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'
                }`}>
                  <BookOpen size={15} /> Quiz Bot
                </Link>
                <Link to="/history" className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${
                  isActive('/history') ? 'bg-[#6C63FF]/20 text-[#6C63FF]' : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-white/5'
                }`}>
                  <BarChart2 size={15} /> History
                </Link>
              </div>

              {/* User avatar dropdown */}
              <div className="relative" ref={dropdownRef}>
                <button
                  onClick={() => setDropdownOpen(!dropdownOpen)}
                  className="flex items-center gap-2 px-3 py-2 rounded-xl bg-[var(--bg-card)] border border-[var(--border)] hover:border-[#6C63FF]/50 transition-colors"
                >
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-[#6C63FF] to-[#00D4AA] flex items-center justify-center text-white text-xs font-bold">
                    {initials}
                  </div>
                  <span className="text-sm text-[var(--text-primary)] hidden sm:block max-w-[100px] truncate">
                    {user?.name}
                  </span>
                  <ChevronDown size={14} className={`text-[var(--text-secondary)] transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} />
                </button>

                {dropdownOpen && (
                  <div className="absolute right-0 top-full mt-2 w-48 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl shadow-xl overflow-hidden">
                    <div className="px-4 py-3 border-b border-[var(--border)]">
                      <p className="text-sm font-medium text-[var(--text-primary)] truncate">{user?.name}</p>
                      <p className="text-xs text-[var(--text-secondary)] truncate">{user?.email}</p>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-4 py-3 text-sm text-[#FF4D6D] hover:bg-[#FF4D6D]/10 transition-colors"
                    >
                      <LogOut size={14} />
                      Logout
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <>
              <Link to="/auth" className="text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors px-4 py-2">
                Login
              </Link>
              <Link to="/auth" className="px-5 py-2.5 bg-[#6C63FF] hover:bg-[#5B52EE] text-white text-sm font-medium rounded-xl transition-colors">
                Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
