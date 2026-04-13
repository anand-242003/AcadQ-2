import { useState, useEffect, useRef } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { Send, Sparkles, RotateCcw, BookOpen, ExternalLink, Loader2, ChevronRight } from 'lucide-react'
import Navbar from '../components/Navbar'
import ChatBubble from '../components/ChatBubble'
import Toast from '../components/Toast'
import { coachAPI } from '../api/client'
import { useAuth } from '../context/AuthContext'

// ─── Typing Indicator ─────────────────────────────────────────────────────────
function TypingIndicator() {
  return (
    <div className="flex items-start gap-3">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-[#6C63FF] to-[#00D4AA] flex items-center justify-center">
        <Sparkles size={14} className="text-white" />
      </div>
      <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl rounded-tl-sm px-4 py-3">
        <div className="flex gap-1 items-center h-5">
          {[0, 1, 2].map(i => (
            <div key={i} className="w-2 h-2 bg-[#6C63FF] rounded-full"
              style={{ animation: 'bounceDot 1.4s ease-in-out infinite', animationDelay: `${i * 0.16}s` }} />
          ))}
        </div>
      </div>
    </div>
  )
}

// ─── Shimmer Skeleton ─────────────────────────────────────────────────────────
function SkeletonCard() {
  return (
    <div className="rounded-xl p-3 space-y-2 overflow-hidden" style={{
      background: 'linear-gradient(90deg, #1E1E2E 25%, #2A2A3E 50%, #1E1E2E 75%)',
      backgroundSize: '1000px 100%',
      animation: 'shimmer 1.5s infinite',
    }}>
      <div className="h-3 rounded w-1/3 bg-[#2A2A3E]" />
      <div className="h-4 rounded w-full bg-[#2A2A3E]" />
      <div className="h-3 rounded w-2/3 bg-[#2A2A3E]" />
    </div>
  )
}

// ─── Study Plan Display ───────────────────────────────────────────────────────
function StudyPlanDisplay({ plan, weeklyGoal }) {
  if (!plan) return null
  const days = plan.split('\n').filter(l => l.trim().startsWith('Day'))

  return (
    <div className="space-y-3">
      {weeklyGoal && (
        <div className="bg-[#FFB347]/10 border border-[#FFB347]/30 rounded-xl p-3">
          <p className="text-xs font-semibold text-[#FFB347] mb-1">WEEKLY GOAL</p>
          <p className="text-sm text-[var(--text-primary)]">{weeklyGoal}</p>
        </div>
      )}
      {days.map((day, i) => {
        const parts = day.split('—').map(s => s.trim())
        const dayLabel = parts[0] || day
        const task = parts[1] || ''
        const time = parts[2] || ''
        const isToday = i === 0
        return (
          <div key={i} className={`border rounded-xl p-3 relative ${
            isToday ? 'border-l-4 border-l-[#6C63FF] border-[#6C63FF]/30 bg-[#6C63FF]/5' : 'border-[var(--border)] bg-[var(--bg-primary)]'
          }`}>
            <div className="flex items-center justify-between mb-1">
              <p className="text-xs font-semibold text-[#6C63FF]">{dayLabel}</p>
              {isToday && (
                <span className="text-xs bg-[#6C63FF]/20 text-[#6C63FF] px-2 py-0.5 rounded-full font-medium">TODAY</span>
              )}
            </div>
            {task && <p className="text-sm text-[var(--text-primary)]">{task}</p>}
            {time && <p className="text-xs text-[var(--text-secondary)] mt-1">{time}</p>}
          </div>
        )
      })}
    </div>
  )
}

// ─── Quick Prompt Chips ───────────────────────────────────────────────────────
const QUICK_PROMPTS = [
  'What are my biggest weaknesses?',
  'Give me a 7-day study plan',
  'How can I improve my focus?',
  'What resources do you recommend?',
]

// ─── Main Component ───────────────────────────────────────────────────────────
export default function StudyCoach() {
  const location = useLocation()
  const navigate = useNavigate()
  const { user } = useAuth()
  const { result, input } = location.state || {}

  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [activeTab, setActiveTab] = useState('plan')
  const [studyPlan, setStudyPlan] = useState(null)
  const [resources, setResources] = useState([])
  const [planLoading, setPlanLoading] = useState(false)
  const [greetingSent, setGreetingSent] = useState(false)
  const [showChips, setShowChips] = useState(true)
  const [toast, setToast] = useState({ message: '', type: '' })

  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  useEffect(() => { scrollToBottom() }, [messages, isTyping])

  // Auto-greeting on mount
  useEffect(() => {
    if (!result || greetingSent) return
    setGreetingSent(true)
    const topWeakness = result.top_weaknesses?.[0]?.feature?.replace(/_/g, ' ') || 'study habits'
    const greeting = `Hi ${user?.name?.split(' ')[0] || 'there'}! 👋 I've reviewed your learning profile — your predicted score is ${result.predicted_score}/100 and you're classified as a ${result.learner_type}. I've identified ${topWeakness} as your biggest area for improvement. What would you like to work on today?`
    setMessages([{ id: Date.now(), role: 'assistant', content: greeting, timestamp: new Date() }])
  }, [result, user, greetingSent])

  const sendMessage = async (text) => {
    if (!text.trim() || isTyping) return
    setShowChips(false)
    const userMsg = { id: Date.now(), role: 'user', content: text, timestamp: new Date() }
    setMessages(prev => [...prev, userMsg])
    setInputText('')
    setIsTyping(true)

    try {
      const profile = result ? {
        predicted_score: result.predicted_score,
        classification: result.classification,
        pass_probability: result.pass_probability,
        learner_type: result.learner_type,
        top_weaknesses: result.top_weaknesses || [],
      } : { predicted_score: 0, classification: 'Unknown', pass_probability: 0, learner_type: 'Average Learner', top_weaknesses: [] }

      const { data } = await coachAPI.chat({ message: text, student_profile: profile })
      setMessages(prev => [...prev, { id: Date.now() + 1, role: 'assistant', content: data.reply, timestamp: new Date() }])
    } catch (err) {
      const detail = err.response?.data?.detail || 'Connection error. Please try again.'
      if (err.response?.status === 429) {
        setToast({ message: 'Message limit reached. Try again in an hour.', type: 'error' })
      } else {
        setToast({ message: 'Connection error. Please try again.', type: 'error' })
      }
      setMessages(prev => [...prev, { id: Date.now() + 1, role: 'assistant', content: detail, timestamp: new Date() }])
    } finally {
      setIsTyping(false)
    }
  }

  const handleReset = async () => {
    try { await coachAPI.reset() } catch {}
    setMessages([])
    setStudyPlan(null)
    setResources([])
    setGreetingSent(false)
    setShowChips(true)
    setToast({ message: 'Session cleared. Starting fresh!', type: 'success' })
  }

  const generatePlan = async () => {
    if (!result) return
    setPlanLoading(true)
    try {
      const profile = {
        predicted_score: result.predicted_score,
        classification: result.classification,
        pass_probability: result.pass_probability,
        learner_type: result.learner_type,
        top_weaknesses: result.top_weaknesses || [],
      }
      const { data } = await coachAPI.plan({ student_profile: profile })
      setStudyPlan({ plan: data.plan, weekly_goal: data.weekly_goal })
      setResources(data.resources || [])
      setToast({ message: 'Your 7-day study plan is ready!', type: 'success' })
    } catch {
      setToast({ message: 'Connection error. Please try again.', type: 'error' })
    } finally {
      setPlanLoading(false)
    }
  }

  if (!result) {
    return (
      <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] flex flex-col" style={{ fontFamily: 'Satoshi, sans-serif' }}>
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center max-w-sm px-6">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#6C63FF] to-[#00D4AA] flex items-center justify-center mx-auto mb-4">
              <Sparkles size={28} className="text-white" />
            </div>
            <h2 className="text-2xl font-bold text-[var(--text-primary)] mb-2" style={{ fontFamily: 'Clash Display, sans-serif' }}>Run a prediction first</h2>
            <p className="text-[var(--text-secondary)] mb-6">Your AI coach needs your prediction results to give personalized advice.</p>
            <button onClick={() => navigate('/input')}
              className="px-6 py-3 bg-[#6C63FF] hover:bg-[#5B52EE] text-white font-semibold rounded-xl transition-colors text-sm">
              Go to Input Form
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] flex flex-col" style={{ fontFamily: 'Satoshi, sans-serif' }}>
      <style>{`
        @keyframes bounceDot { 0%,80%,100% { transform: scale(0) } 40% { transform: scale(1) } }
        @keyframes shimmer { 0% { background-position: -1000px 0 } 100% { background-position: 1000px 0 } }
      `}</style>
      <Toast message={toast.message} type={toast.type} onClose={() => setToast({ message: '', type: '' })} />
      <Navbar />

      <div className="flex-1 flex pt-16 overflow-hidden" style={{ height: 'calc(100vh - 64px)' }}>
        {/* ── Left Sidebar ── */}
        <div className="hidden lg:flex w-72 flex-col bg-[var(--bg-secondary)] border-r border-[var(--border)] p-5 gap-5 overflow-y-auto flex-shrink-0">
          <div className="flex flex-col items-center gap-3 pt-4">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#6C63FF] to-[#00D4AA] flex items-center justify-center">
              <Sparkles size={24} className="text-white" />
            </div>
            <div className="text-center">
              <p className="font-bold text-[var(--text-primary)]" style={{ fontFamily: 'Clash Display, sans-serif' }}>AcadIQ Coach</p>
              <p className="text-xs text-[var(--text-secondary)]">Powered by Groq + LangChain</p>
            </div>
          </div>

          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-4 space-y-2">
            <p className="text-xs text-[var(--text-muted)] font-medium">FROM YOUR LAST ANALYSIS</p>
            <div className="flex items-center justify-between">
              <span className="text-xs text-[var(--text-secondary)]">Score</span>
              <span className="text-sm font-bold text-[#6C63FF]">{result.predicted_score}/100</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-[var(--text-secondary)]">Status</span>
              <span className={`text-xs font-semibold ${result.classification === 'Pass' ? 'text-[#00D4AA]' : 'text-[#FF4D6D]'}`}>{result.classification}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-[var(--text-secondary)]">Archetype</span>
              <span className="text-xs text-[#FFB347] font-medium truncate max-w-[100px]">{result.learner_type}</span>
            </div>
          </div>

          <button onClick={handleReset}
            className="flex items-center gap-2 px-4 py-2.5 border border-[var(--border)] hover:border-[#FF4D6D]/50 text-[var(--text-secondary)] hover:text-[#FF4D6D] rounded-xl transition-colors text-sm">
            <RotateCcw size={14} />
            New Session
          </button>

          <div>
            <p className="text-xs text-[var(--text-muted)] font-medium mb-2">QUICK PROMPTS</p>
            <div className="space-y-2">
              {QUICK_PROMPTS.map(prompt => (
                <button key={prompt} onClick={() => sendMessage(prompt)}
                  className="w-full text-left px-3 py-2.5 bg-[var(--bg-card)] border border-[var(--border)] hover:border-[#6C63FF]/50 rounded-xl text-xs text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-colors flex items-center gap-2">
                  <ChevronRight size={12} className="text-[#6C63FF] flex-shrink-0" />
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* ── Center Chat Panel ── */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4">
            {messages.map(msg => (
              <ChatBubble key={msg.id} role={msg.role} message={msg.content} timestamp={msg.timestamp} />
            ))}
            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick prompt chips — visible on all screens, hidden after first user message */}
          {showChips && (
            <div className="px-4 pb-3 flex flex-wrap gap-2">
              {QUICK_PROMPTS.map(p => (
                <button key={p} onClick={() => sendMessage(p)}
                  className="px-4 py-2 bg-[var(--bg-card)] border border-[var(--border)] hover:border-[#6C63FF] hover:text-[var(--text-primary)] rounded-full text-sm text-[var(--text-secondary)] transition-colors whitespace-nowrap">
                  {p}
                </button>
              ))}
            </div>
          )}

          {/* Input area */}
          <div className="border-t border-[var(--border)] p-4">
            <div className="flex gap-3 items-end">
              <div className="flex-1 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl px-4 py-3 focus-within:border-[#6C63FF] transition-colors">
                <textarea
                  ref={inputRef}
                  value={inputText}
                  onChange={e => setInputText(e.target.value)}
                  onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(inputText) } }}
                  placeholder="Ask your coach anything..."
                  rows={1}
                  className="w-full bg-transparent text-[var(--text-primary)] placeholder:text-[var(--text-muted)] text-sm outline-none resize-none"
                  style={{ maxHeight: '120px' }}
                />
              </div>
              <button onClick={() => sendMessage(inputText)} disabled={!inputText.trim() || isTyping}
                className="w-11 h-11 bg-[#6C63FF] hover:bg-[#5B52EE] disabled:opacity-40 disabled:cursor-not-allowed rounded-xl flex items-center justify-center transition-colors flex-shrink-0">
                <Send size={16} className="text-white" />
              </button>
            </div>
            <p className="text-xs text-[var(--text-muted)] mt-2 text-center hidden md:block">Press Enter to send · Shift+Enter for new line</p>
          </div>
        </div>

        {/* ── Right Panel ── */}
        <div className="hidden xl:flex w-80 flex-col bg-[var(--bg-secondary)] border-l border-[var(--border)] overflow-hidden flex-shrink-0">
          <div className="flex border-b border-[var(--border)]">
            {[{ id: 'plan', label: '📋 Study Plan' }, { id: 'resources', label: '📚 Resources' }].map(tab => (
              <button key={tab.id} onClick={() => setActiveTab(tab.id)}
                className={`flex-1 py-3.5 text-xs font-medium transition-colors ${activeTab === tab.id ? 'text-[#6C63FF] border-b-2 border-[#6C63FF]' : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)]'}`}>
                {tab.label}
              </button>
            ))}
          </div>

          <div className="flex-1 overflow-y-auto p-4">
            {activeTab === 'plan' && (
              <div className="space-y-4">
                <button onClick={generatePlan} disabled={planLoading}
                  className="w-full py-2.5 bg-[#6C63FF] hover:bg-[#5B52EE] disabled:opacity-50 text-white text-sm font-semibold rounded-xl transition-colors flex items-center justify-center gap-2">
                  {planLoading ? <><Loader2 size={14} className="animate-spin" /> Generating...</> : 'Generate My Plan'}
                </button>
                {planLoading && <>{[1,2,3,4,5,6,7].map(i => <SkeletonCard key={i} />)}</>}
                {studyPlan && !planLoading && <StudyPlanDisplay plan={studyPlan.plan} weeklyGoal={studyPlan.weekly_goal} />}
                {!studyPlan && !planLoading && (
                  <p className="text-xs text-[var(--text-muted)] text-center py-8">Click "Generate My Plan" to get a personalized 7-day study plan based on your profile.</p>
                )}
              </div>
            )}

            {activeTab === 'resources' && (
              <div className="space-y-3">
                {resources.length === 0 ? (
                  <div className="text-center py-8">
                    <BookOpen size={32} className="text-[var(--text-muted)] mx-auto mb-3" />
                    <p className="text-xs text-[var(--text-muted)]">Generate a study plan to see curated resources for your weaknesses.</p>
                  </div>
                ) : (
                  resources.map((r, i) => (
                    <div key={i} className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl p-4">
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <p className="text-sm font-medium text-[var(--text-primary)] leading-tight">{r.title}</p>
                        <a href={r.url} target="_blank" rel="noopener noreferrer"
                          className="flex-shrink-0 text-[#6C63FF] hover:text-[#00D4AA] transition-colors">
                          <ExternalLink size={14} />
                        </a>
                      </div>
                      <p className="text-xs text-[var(--text-secondary)] leading-relaxed mb-2">{r.description}</p>
                      <span className="inline-block px-2 py-0.5 rounded-full text-xs bg-[#6C63FF]/10 text-[#6C63FF] border border-[#6C63FF]/20">
                        {r.topic?.replace(/_/g, ' ')}
                      </span>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
