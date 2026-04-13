import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  Sparkles, ArrowRight, Brain, MessageSquare, ClipboardList,
  Trophy, Target, Flame, Leaf, CheckCircle2, ChevronRight,
  TrendingUp, Zap, ChevronUp
} from 'lucide-react'
import Navbar from '../components/Navbar'

// ─── Back to Top ──────────────────────────────────────────────────────────────
function BackToTop() {
  const [show, setShow] = useState(false)
  useEffect(() => {
    const handler = () => setShow(window.scrollY > 400)
    window.addEventListener('scroll', handler)
    return () => window.removeEventListener('scroll', handler)
  }, [])

  return (
    <button
      onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
      className={`fixed bottom-8 right-8 z-50 w-12 h-12 bg-[#6C63FF] hover:bg-[#5B52EE] text-white rounded-full flex items-center justify-center shadow-lg hover:shadow-[0_0_20px_rgba(108,99,255,0.5)] hover:-translate-y-1 transition-all duration-300 ${
        show ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
      }`}
    >
      <ChevronUp size={20} />
    </button>
  )
}

// ─── Floating Particles ───────────────────────────────────────────────────────
function Particles() {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {Array.from({ length: 20 }).map((_, i) => (
        <div
          key={i}
          className="absolute rounded-full bg-[#6C63FF]"
          style={{
            width: `${Math.random() * 4 + 2}px`,
            height: `${Math.random() * 4 + 2}px`,
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            opacity: 0.05 + Math.random() * 0.08,
            animation: `float ${8 + Math.random() * 12}s ease-in-out infinite`,
            animationDelay: `${Math.random() * 8}s`,
          }}
        />
      ))}
    </div>
  )
}

// ─── Animated Counter ─────────────────────────────────────────────────────────
function AnimatedCounter({ target, suffix = '', duration = 2000 }) {
  const [count, setCount] = useState(0)
  const ref = useRef(null)
  const started = useRef(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !started.current) {
          started.current = true
          const start = performance.now()
          const animate = (now) => {
            const elapsed = now - start
            const progress = Math.min(elapsed / duration, 1)
            const eased = 1 - Math.pow(1 - progress, 3)
            setCount(Math.floor(eased * target))
            if (progress < 1) requestAnimationFrame(animate)
            else setCount(target)
          }
          requestAnimationFrame(animate)
        }
      },
      { threshold: 0.5 }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [target, duration])

  return <span ref={ref}>{count.toLocaleString()}{suffix}</span>
}

// ─── Score Ring Mockup ────────────────────────────────────────────────────────
function ScoreRingMockup() {
  const score = 74
  const radius = 54
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (score / 100) * circumference

  return (
    <div className="relative bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-6 shadow-[0_0_60px_rgba(108,99,255,0.25)] max-w-xs mx-auto">
      {/* Glow */}
      <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-[#6C63FF]/5 to-[#00D4AA]/5" />

      <div className="relative flex flex-col items-center gap-4">
        {/* Score ring */}
        <div className="relative">
          <svg width="140" height="140" className="-rotate-90">
            <circle cx="70" cy="70" r={radius} fill="none" stroke="#1E1E2E" strokeWidth="8" />
            <circle
              cx="70" cy="70" r={radius} fill="none"
              stroke="#6C63FF" strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              style={{ transition: 'stroke-dashoffset 1.5s ease' }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-3xl font-bold text-[var(--text-primary)]" style={{ fontFamily: 'Clash Display, sans-serif' }}>74</span>
            <span className="text-sm text-[var(--text-secondary)]">/ 100</span>
          </div>
        </div>

        {/* Badges */}
        <div className="flex flex-col items-center gap-2 w-full">
          <span className="px-3 py-1 rounded-full bg-[#00D4AA]/20 text-[#00D4AA] text-xs font-medium border border-[#00D4AA]/30">
            ✓ Pass — 84% probability
          </span>
          <span className="px-3 py-1 rounded-full bg-[#6C63FF]/20 text-[#6C63FF] text-xs font-medium border border-[#6C63FF]/30">
            🏆 High Achiever
          </span>
        </div>

        {/* Mini bar */}
        <div className="w-full">
          <div className="flex justify-between text-xs text-[var(--text-secondary)] mb-1">
            <span>Pass Probability</span>
            <span>84%</span>
          </div>
          <div className="h-1.5 bg-[#1E1E2E] rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-[#6C63FF] to-[#00D4AA] rounded-full" style={{ width: '84%' }} />
          </div>
        </div>
      </div>
    </div>
  )
}

// ─── Main Landing Component ───────────────────────────────────────────────────
export default function Landing() {
  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]" style={{ fontFamily: 'Satoshi, sans-serif' }}>
      <BackToTop />
      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) }
          50% { transform: translateY(-20px) }
        }
        @keyframes fadeSlideUp {
          from { opacity: 0; transform: translateY(24px) }
          to { opacity: 1; transform: translateY(0) }
        }
        .animate-in { animation: fadeSlideUp 0.6s ease forwards; }
        .stagger-1 { animation-delay: 0.1s; opacity: 0; }
        .stagger-2 { animation-delay: 0.2s; opacity: 0; }
        .stagger-3 { animation-delay: 0.3s; opacity: 0; }
        .stagger-4 { animation-delay: 0.4s; opacity: 0; }
      `}</style>

      <Navbar />

      {/* ── Section 1: Hero ── */}
      <section className="relative min-h-screen flex flex-col items-center justify-center px-6 pt-20 overflow-hidden">
        {/* Background glow */}
        <div
          className="absolute inset-0 pointer-events-none"
          style={{
            background: 'radial-gradient(ellipse 80% 50% at 50% -10%, rgba(108,99,255,0.3) 0%, transparent 70%)',
          }}
        />
        <Particles />

        <div className="relative z-10 max-w-5xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-[#6C63FF]/40 bg-[#6C63FF]/10 text-sm text-[#6C63FF] mb-8 animate-in stagger-1">
            <Sparkles size={14} />
            AI-Powered Learning Analytics
          </div>

          {/* Headline */}
          <h1
            className="text-6xl md:text-7xl lg:text-8xl font-bold leading-tight mb-6 animate-in stagger-2"
            style={{ fontFamily: 'Clash Display, sans-serif' }}
          >
            Know Your{' '}
            <span
              style={{
                background: 'linear-gradient(135deg, #6C63FF 0%, #00D4AA 100%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}
            >
              Score.
            </span>
            <br />
            Before You Sit.
          </h1>

          {/* Subheadline */}
          <p className="text-lg md:text-xl text-[var(--text-secondary)] max-w-2xl mx-auto mb-10 leading-relaxed animate-in stagger-3">
            AcadIQ predicts your exam performance using behavioral science and then coaches you with AI to actually improve it.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-6 animate-in stagger-4">
            <Link
              to="/auth"
              className="flex items-center gap-2 px-8 py-4 bg-[#6C63FF] hover:bg-[#5B52EE] text-white font-semibold rounded-xl transition-all duration-200 hover:shadow-[0_0_30px_rgba(108,99,255,0.4)] text-base"
            >
              Analyze My Performance
              <ArrowRight size={18} />
            </Link>
            <a
              href="#how-it-works"
              className="flex items-center gap-2 px-8 py-4 border border-[var(--border)] hover:border-[#6C63FF]/50 text-[var(--text-secondary)] hover:text-[var(--text-primary)] rounded-xl transition-all duration-200 text-base"
            >
              See How It Works
              <ChevronRight size={18} />
            </a>
          </div>
          <p className="text-xs text-[var(--text-muted)]">No credit card. No signup to preview.</p>

          {/* Hero visual */}
          <div className="mt-16 animate-in stagger-4">
            <ScoreRingMockup />
          </div>
        </div>
      </section>

      {/* ── Section 2: Stats Bar ── */}
      <section className="bg-[#0D0D14] py-12 border-y border-[var(--border)]">
        <div className="max-w-5xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { value: 5000, suffix: '+', label: 'Students Analyzed' },
              { value: 97, suffix: '.1%', label: 'Prediction Accuracy' },
              { value: 4, suffix: '', label: 'Learner Archetypes' },
              { value: 1, suffix: '', label: 'AI-Powered Coach' },
            ].map(({ value, suffix, label }, i) => (
              <div key={i} className="text-center">
                <div
                  className="text-4xl md:text-5xl font-bold mb-1"
                  style={{
                    fontFamily: 'Clash Display, sans-serif',
                    background: 'linear-gradient(135deg, #6C63FF 0%, #00D4AA 100%)',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    backgroundClip: 'text',
                  }}
                >
                  <AnimatedCounter target={value} suffix={suffix} />
                </div>
                <p className="text-sm text-[var(--text-secondary)]">{label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Section 3: How It Works ── */}
      <section id="how-it-works" className="py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2
              className="text-4xl md:text-5xl font-bold mb-4"
              style={{ fontFamily: 'Clash Display, sans-serif' }}
            >
              How AcadIQ Works
            </h2>
            <p className="text-[var(--text-secondary)] text-lg">Three steps from data to direction</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                num: '01',
                icon: <ClipboardList size={24} className="text-[#6C63FF]" />,
                title: 'Enter Your Data',
                desc: 'Input your study habits, wellness metrics, and academic scores. 20+ data points build your complete learner profile.',
              },
              {
                num: '02',
                icon: <Brain size={24} className="text-[#6C63FF]" />,
                title: 'Get Predictions',
                desc: 'Our ML models predict your exam score, classify pass/fail probability, and assign your learner archetype.',
              },
              {
                num: '03',
                icon: <MessageSquare size={24} className="text-[#6C63FF]" />,
                title: 'Talk to Your Coach',
                desc: 'Your AI Study Coach diagnoses gaps, builds a weekly plan, and answers your questions — with memory across sessions.',
              },
            ].map(({ num, icon, title, desc }) => (
              <div
                key={num}
                className="relative bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-8 hover:border-[#6C63FF]/50 hover:-translate-y-1 transition-all duration-300 overflow-hidden group"
              >
                {/* Decorative number */}
                <span
                  className="absolute top-4 right-4 text-7xl font-bold text-white/5 select-none"
                  style={{ fontFamily: 'Clash Display, sans-serif' }}
                >
                  {num}
                </span>
                <div className="relative z-10">
                  <div className="w-12 h-12 rounded-xl bg-[#6C63FF]/10 flex items-center justify-center mb-4">
                    {icon}
                  </div>
                  <h3 className="text-xl font-bold text-[var(--text-primary)] mb-3" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                    {title}
                  </h3>
                  <p className="text-[var(--text-secondary)] text-sm leading-relaxed">{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Section 4: Features Deep-Dive ── */}
      <section className="py-24 px-6 bg-[#0D0D14]">
        <div className="max-w-5xl mx-auto space-y-24">
          {/* Feature A */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div>
              <div className="w-12 h-12 rounded-xl bg-[#6C63FF]/10 flex items-center justify-center mb-6">
                <TrendingUp size={24} className="text-[#6C63FF]" />
              </div>
              <h3 className="text-3xl font-bold text-[var(--text-primary)] mb-4" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                Precision ML Predictions
              </h3>
              <p className="text-[var(--text-secondary)] mb-6 leading-relaxed">
                Three simultaneous models analyze your behavioral data to give you a complete academic risk profile before exam day.
              </p>
              <ul className="space-y-3">
                {['Exam score prediction (Linear Regression)', 'Pass/Fail classification (Logistic Regression)', 'Learner archetype assignment (K-Means)'].map(item => (
                  <li key={item} className="flex items-center gap-3 text-sm text-[var(--text-secondary)]">
                    <CheckCircle2 size={16} className="text-[#6C63FF] flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-6 space-y-4">
              {[
                { label: 'Predicted Score', value: '74 / 100', color: '#6C63FF' },
                { label: 'Classification', value: 'Pass ✓', color: '#00D4AA' },
                { label: 'Learner Type', value: 'High Achiever', color: '#FFB347' },
              ].map(({ label, value, color }) => (
                <div key={label} className="flex items-center justify-between p-4 bg-[var(--bg-primary)] rounded-xl border border-[var(--border)]">
                  <span className="text-sm text-[var(--text-secondary)]">{label}</span>
                  <span className="text-sm font-semibold" style={{ color }}>{value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Feature B */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            <div className="order-2 md:order-1 bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-6 space-y-3">
              {[
                { role: 'user', msg: 'I keep procrastinating on assignments.' },
                { role: 'ai', msg: "Given your focus index of 55 and burnout at 60%, let's try the 2-minute rule. If a task takes under 2 minutes, do it now. For bigger tasks, use 25-min Pomodoro blocks." },
                { role: 'user', msg: 'That makes sense. What about sleep?' },
                { role: 'ai', msg: 'Your 6.5 hours is below the 7.3 average. Even one extra hour can improve memory consolidation by 20%. Try a consistent bedtime this week.' },
              ].map(({ role, msg }, i) => (
                <div key={i} className={`flex ${role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] px-3 py-2 rounded-xl text-xs leading-relaxed ${
                    role === 'user'
                      ? 'bg-[#6C63FF] text-white rounded-tr-sm'
                      : 'bg-[var(--bg-primary)] border border-[var(--border)] text-[var(--text-secondary)] rounded-tl-sm'
                  }`}>
                    {msg}
                  </div>
                </div>
              ))}
            </div>
            <div className="order-1 md:order-2">
              <div className="w-12 h-12 rounded-xl bg-[#00D4AA]/10 flex items-center justify-center mb-6">
                <Zap size={24} className="text-[#00D4AA]" />
              </div>
              <h3 className="text-3xl font-bold text-[var(--text-primary)] mb-4" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                Your Personal AI Coach
              </h3>
              <p className="text-[var(--text-secondary)] mb-6 leading-relaxed">
                An AI coach that knows your exact numbers and gives specific, actionable advice — not generic study tips.
              </p>
              <ul className="space-y-3">
                {['Remembers your conversation history', 'Generates personalized 7-day study plans', 'Retrieves curated resources via RAG'].map(item => (
                  <li key={item} className="flex items-center gap-3 text-sm text-[var(--text-secondary)]">
                    <CheckCircle2 size={16} className="text-[#00D4AA] flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* ── Section 5: Learner Archetypes ── */}
      <section className="py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4" style={{ fontFamily: 'Clash Display, sans-serif' }}>
              Which learner are you?
            </h2>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                icon: <Trophy size={28} />,
                name: 'High Achiever',
                desc: 'Consistently strong performance with high pass probability and excellent study habits.',
                gradient: 'from-[#00D4AA] to-[#00B894]',
                border: 'border-[#00D4AA]/30',
                bg: 'bg-[#00D4AA]/5',
              },
              {
                icon: <Target size={28} />,
                name: 'Developing Learner',
                desc: 'On the right track with room to grow. Consistent effort will push you to the top.',
                gradient: 'from-[#6C63FF] to-[#5B52EE]',
                border: 'border-[#6C63FF]/30',
                bg: 'bg-[#6C63FF]/5',
              },
              {
                icon: <Flame size={28} />,
                name: 'Struggling Learner',
                desc: 'Facing challenges but with targeted support and focus, improvement is very achievable.',
                gradient: 'from-[#FF4D6D] to-[#FF6B35]',
                border: 'border-[#FF4D6D]/30',
                bg: 'bg-[#FF4D6D]/5',
              },
              {
                icon: <Leaf size={28} />,
                name: 'Average Learner',
                desc: 'Solid foundation with specific areas to strengthen. Small changes yield big results.',
                gradient: 'from-[#FFB347] to-[#FF9500]',
                border: 'border-[#FFB347]/30',
                bg: 'bg-[#FFB347]/5',
              },
            ].map(({ icon, name, desc, gradient, border, bg }) => (
              <div
                key={name}
                className={`${bg} border ${border} rounded-2xl p-6 hover:-translate-y-1 transition-all duration-300`}
              >
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${gradient} flex items-center justify-center text-white mb-4`}>
                  {icon}
                </div>
                <h4 className="font-bold text-[var(--text-primary)] mb-2" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                  {name}
                </h4>
                <p className="text-xs text-[var(--text-secondary)] leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Section 6: CTA Banner ── */}
      <section className="py-24 px-6 bg-[#6C63FF] relative overflow-hidden">
        <div
          className="absolute inset-0 opacity-10"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.4'/%3E%3C/svg%3E")`,
          }}
        />
        <div className="relative z-10 max-w-3xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6" style={{ fontFamily: 'Clash Display, sans-serif' }}>
            Ready to meet your AI coach?
          </h2>
          <Link
            to="/auth"
            className="inline-flex items-center gap-2 px-8 py-4 bg-white text-[#6C63FF] font-semibold rounded-xl hover:bg-gray-100 transition-colors text-base"
          >
            Start For Free
            <ArrowRight size={18} />
          </Link>
        </div>
      </section>

      {/* ── Section 7: Footer ── */}
      <footer className="bg-[var(--bg-primary)] border-t border-[var(--border)] py-12 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-3">
                <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-[#6C63FF] to-[#00D4AA] flex items-center justify-center">
                  <Sparkles size={14} className="text-white" />
                </div>
                <span className="font-bold text-[var(--text-primary)]" style={{ fontFamily: 'Clash Display, sans-serif' }}>AcadIQ</span>
              </div>
              <p className="text-xs text-[var(--text-muted)]">Intelligent Learning Analytics</p>
            </div>
            <div className="flex flex-col gap-2">
              <a href="#how-it-works" className="text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">How It Works</a>
              <a href="#" className="text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">Features</a>
              <Link to="/auth" className="text-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors">Get Started</Link>
            </div>
            <div>
              <p className="text-sm text-[var(--text-secondary)]">Built for the GenAI Capstone 2026</p>
            </div>
          </div>
          <div className="border-t border-[var(--border)] pt-6 text-center">
            <p className="text-xs text-[var(--text-muted)]">© 2026 AcadIQ. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
