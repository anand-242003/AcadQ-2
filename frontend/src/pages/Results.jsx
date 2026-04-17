import { useEffect, useRef, useState } from 'react'
import { useLocation, useNavigate, Navigate } from 'react-router-dom'
import { ArrowRight, Trophy, Target, Flame, Leaf, TrendingDown, MessageSquare, Download, Award } from 'lucide-react'
import confetti from 'canvas-confetti'
import { jsPDF } from 'jspdf'
import Navbar from '../components/Navbar'
import RadarChart from '../components/RadarChart'
import Toast from '../components/Toast'
import { predictAPI } from '../api/client'

// ─── Score Ring ───────────────────────────────────────────────────────────────
function ScoreRing({ score }) {
  const [displayScore, setDisplayScore] = useState(0)
  const radius = 80
  const circumference = 2 * Math.PI * radius
  const strokeDashoffset = circumference - (displayScore / 100) * circumference
  const color = score >= 80 ? '#00D4AA' : score >= 60 ? '#6C63FF' : score >= 40 ? '#FFB347' : '#FF4D6D'
  const grade = score >= 75 ? 'A' : score >= 60 ? 'B' : score >= 45 ? 'C' : score >= 30 ? 'D' : 'F'

  useEffect(() => {
    const start = performance.now()
    const duration = 1500
    const animate = (now) => {
      const elapsed = now - start
      const progress = Math.min(elapsed / duration, 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setDisplayScore(Math.round(eased * score))
      if (progress < 1) requestAnimationFrame(animate)
    }
    requestAnimationFrame(animate)
  }, [score])

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative">
        <svg width="200" height="200" className="-rotate-90">
          <circle cx="100" cy="100" r={radius} fill="none" stroke="#1E1E2E" strokeWidth="12" />
          <circle cx="100" cy="100" r={radius} fill="none" stroke={color} strokeWidth="12"
            strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={strokeDashoffset}
            style={{ transition: 'stroke-dashoffset 0.05s linear', filter: `drop-shadow(0 0 12px ${color}60)` }} />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-5xl font-bold" style={{ fontFamily: 'Clash Display, sans-serif', color }}>{displayScore}</span>
          <span className="text-2xl font-bold text-[var(--text-secondary)]" style={{ fontFamily: 'Clash Display, sans-serif' }}>{grade}</span>
        </div>
      </div>
      <p className="text-sm text-[var(--text-secondary)]">Predicted Exam Score</p>
    </div>
  )
}

const ARCHETYPE_CONFIG = {
  'High Achiever': { icon: <Trophy size={28} />, gradient: 'from-[#00D4AA]/10 to-[#00B894]/5', border: 'border-[#00D4AA]/30', color: '#00D4AA', tags: ['Consistent', 'High Pass Rate', 'Strong Habits'], desc: 'You demonstrate consistently strong academic performance with excellent study habits and high pass probability.' },
  'Developing Learner': { icon: <Target size={28} />, gradient: 'from-[#6C63FF]/10 to-[#5B52EE]/5', border: 'border-[#6C63FF]/30', color: '#6C63FF', tags: ['On Track', 'Growing', 'Consistent Effort'], desc: 'You are on the right trajectory. Consistent effort and targeted improvements will push you to the top tier.' },
  'Struggling Learner': { icon: <Flame size={28} />, gradient: 'from-[#FF4D6D]/10 to-[#FF6B35]/5', border: 'border-[#FF4D6D]/30', color: '#FF4D6D', tags: ['Needs Support', 'High Burnout', 'At Risk'], desc: 'You are facing challenges but with targeted support and focused effort, significant improvement is achievable.' },
  'Average Learner': { icon: <Leaf size={28} />, gradient: 'from-[#FFB347]/10 to-[#FF9500]/5', border: 'border-[#FFB347]/30', color: '#FFB347', tags: ['Solid Foundation', 'Room to Grow', 'Consistent'], desc: 'You have a solid foundation with specific areas to strengthen. Small targeted changes yield big results.' },
  'At Risk Learner': { icon: <Flame size={28} />, gradient: 'from-[#FF4D6D]/10 to-[#FF6B35]/5', border: 'border-[#FF4D6D]/30', color: '#FF4D6D', tags: ['Critical', 'Needs Immediate Help', 'Low Pass Rate'], desc: 'Immediate academic support is recommended. With the right help and plan, recovery is absolutely possible.' },
}

const CATEGORY_COLORS = {
  'Critical alert': '#FF4D6D', 'At risk': '#FF4D6D', 'Room to improve': '#FFB347',
  'Study strategy': '#6C63FF', 'Performing well': '#00D4AA', 'Next level': '#00D4AA',
  'Study time': '#6C63FF', 'Sleep': '#00D4AA', 'Distractions': '#FFB347',
  'Mental health': '#6C63FF', 'Burnout': '#FF4D6D', 'Exercise': '#00D4AA',
  'Connectivity': '#FFB347', 'Learner profile': '#6C63FF', 'Study approach': '#6C63FF', 'Planning': '#FFB347',
}

export default function Results() {
  const location = useLocation()
  const navigate = useNavigate()
  const { result: stateResult, input: stateInput } = location.state || {}
  const [result, setResult] = useState(stateResult)
  const [input, setInput] = useState(stateInput)
  const [loading, setLoading] = useState(!stateResult)
  const [toast, setToast] = useState({ message: '', type: '' })

  // Fetch latest report from database if no state
  useEffect(() => {
    if (!stateResult) {
      const fetchLatestReport = async () => {
        try {
          const res = await predictAPI.getHistory()
          const reports = res.data.reports
          if (reports.length > 0) {
            const latest = reports[0] // Most recent first
            setResult(latest.prediction)
            setInput(latest.input_data)
          } else {
            navigate('/input', { replace: true })
          }
        } catch (err) {
          console.error('Failed to fetch report:', err)
          navigate('/input', { replace: true })
        } finally {
          setLoading(false)
        }
      }
      fetchLatestReport()
    } else {
      setLoading(false)
    }
  }, [stateResult, navigate])

  // Confetti on pass — fires once
  useEffect(() => {
    if (result?.classification === 'Pass') {
      const t = setTimeout(() => {
        confetti({
          particleCount: 120,
          spread: 80,
          origin: { y: 0.6 },
          colors: ['#6C63FF', '#00D4AA', '#FFB347'],
        })
      }, 600)
      return () => clearTimeout(t)
    }
  }, [result])

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0A0A0F] text-white flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="w-12 h-12 rounded-full border-4 border-[#6C63FF]/30 border-t-[#6C63FF] animate-spin" />
        </div>
      </div>
    )
  }

  if (!result || !input) return <Navigate to="/input" replace />

  const archetype = ARCHETYPE_CONFIG[result.learner_type] || ARCHETYPE_CONFIG['Average Learner']
  const isPass = result.classification === 'Pass'
  const grade = result.predicted_score >= 75 ? 'A' : result.predicted_score >= 60 ? 'B' : result.predicted_score >= 45 ? 'C' : result.predicted_score >= 30 ? 'D' : 'F'
  const scoreColor = result.predicted_score >= 80 ? '#00D4AA' : result.predicted_score >= 60 ? '#6C63FF' : result.predicted_score >= 40 ? '#FFB347' : '#FF4D6D'

  // ── Download Badge ──────────────────────────────────────────────────────────
  const handleDownloadBadge = () => {
    const canvas = document.createElement('canvas')
    canvas.width = 680
    canvas.height = 400
    const ctx = canvas.getContext('2d')

    // Background
    ctx.fillStyle = '#0A0A0F'
    ctx.fillRect(0, 0, 680, 400)

    // Radial glow
    const grd = ctx.createRadialGradient(340, 200, 20, 340, 200, 220)
    grd.addColorStop(0, 'rgba(108,99,255,0.35)')
    grd.addColorStop(1, 'rgba(108,99,255,0)')
    ctx.fillStyle = grd
    ctx.fillRect(0, 0, 680, 400)

    // Border
    ctx.strokeStyle = '#1E1E2E'
    ctx.lineWidth = 2
    ctx.strokeRect(1, 1, 678, 398)

    // AcadIQ title
    ctx.fillStyle = '#6C63FF'
    ctx.font = 'bold 28px sans-serif'
    ctx.textAlign = 'center'
    ctx.fillText('AcadIQ', 340, 55)

    // Score
    ctx.fillStyle = scoreColor
    ctx.font = 'bold 96px sans-serif'
    ctx.fillText(String(Math.round(result.predicted_score)), 300, 185)
    ctx.fillStyle = '#8B8AA0'
    ctx.font = 'bold 32px sans-serif'
    ctx.fillText('/100', 430, 175)

    // Grade circle
    ctx.beginPath()
    ctx.arc(340, 240, 28, 0, Math.PI * 2)
    ctx.fillStyle = scoreColor + '33'
    ctx.fill()
    ctx.strokeStyle = scoreColor
    ctx.lineWidth = 2
    ctx.stroke()
    ctx.fillStyle = scoreColor
    ctx.font = 'bold 24px sans-serif'
    ctx.textAlign = 'center'
    ctx.fillText(grade, 340, 249)

    // Learner type
    ctx.fillStyle = '#F0EEF8'
    ctx.font = 'bold 22px sans-serif'
    ctx.fillText(result.learner_type, 340, 300)

    // Pass/Fail pill
    const pillColor = isPass ? '#00D4AA' : '#FF4D6D'
    const pillText = isPass ? '✓ PASS' : '✗ FAIL'
    ctx.beginPath()
    ctx.roundRect(280, 318, 120, 34, 17)
    ctx.fillStyle = pillColor + '33'
    ctx.fill()
    ctx.strokeStyle = pillColor
    ctx.lineWidth = 1.5
    ctx.stroke()
    ctx.fillStyle = pillColor
    ctx.font = 'bold 14px sans-serif'
    ctx.fillText(pillText, 340, 340)

    // Watermark
    ctx.fillStyle = '#4A4A6A'
    ctx.font = '13px sans-serif'
    ctx.fillText('acadiq.app', 340, 385)

    // Download
    const link = document.createElement('a')
    link.download = 'acadiq-badge.png'
    link.href = canvas.toDataURL('image/png')
    link.click()
    setToast({ message: 'Badge downloaded!', type: 'success' })
  }

  // ── Download PDF Report ─────────────────────────────────────────────────────
  const handleDownloadPDF = () => {
    const doc = new jsPDF()
    const pageW = doc.internal.pageSize.getWidth()
    let y = 20

    const addLine = (text, size = 11, bold = false, color = [240, 238, 248]) => {
      doc.setFontSize(size)
      doc.setFont('helvetica', bold ? 'bold' : 'normal')
      doc.setTextColor(...color)
      doc.text(text, 20, y)
      y += size * 0.6 + 4
    }

    const addSection = (title) => {
      y += 4
      doc.setFillColor(108, 99, 255, 0.15)
      doc.rect(15, y - 6, pageW - 30, 10, 'F')
      addLine(title, 13, true, [108, 99, 255])
      y += 2
    }

    const checkPage = () => {
      if (y > 270) { doc.addPage(); y = 20; addFooter() }
    }

    const addFooter = () => {
      doc.setFontSize(9)
      doc.setTextColor(74, 74, 106)
      doc.text('Generated by AcadIQ — Intelligent Learning Analytics', pageW / 2, 290, { align: 'center' })
    }

    // Header
    doc.setFillColor(10, 10, 15)
    doc.rect(0, 0, pageW, 30, 'F')
    doc.setFontSize(20)
    doc.setFont('helvetica', 'bold')
    doc.setTextColor(108, 99, 255)
    doc.text('AcadIQ', 20, 20)
    doc.setFontSize(10)
    doc.setTextColor(139, 138, 160)
    doc.text('Performance Analysis Report', 60, 20)
    doc.text(`Generated: ${new Date().toLocaleDateString()}`, pageW - 20, 20, { align: 'right' })
    y = 45

    // Section 1: Results
    addSection('Prediction Results')
    addLine(`Predicted Score: ${result.predicted_score}/100  (Grade: ${grade})`, 12, true)
    addLine(`Classification: ${result.classification}`)
    addLine(`Pass Probability: ${result.pass_probability}%`)
    addLine(`Fail Probability: ${result.fail_probability}%`)
    addLine(`Learner Archetype: ${result.learner_type}`)

    // Section 2: Weaknesses
    checkPage()
    addSection('Key Areas for Improvement')
    result.top_weaknesses.forEach(w => {
      addLine(`• ${w.feature.replace(/_/g, ' ')}: Your value ${w.student_value.toFixed(1)} vs Average ${w.dataset_average.toFixed(1)} (${Math.abs(w.delta / w.dataset_average * 100).toFixed(0)}% below avg)`)
      checkPage()
    })

    // Section 3: Recommendations
    checkPage()
    addSection('Personalized Recommendations')
    result.recommendations.forEach(r => {
      addLine(`[${r.category.toUpperCase()}]`, 10, true, [108, 99, 255])
      y -= 2
      const lines = doc.splitTextToSize(r.message, pageW - 40)
      lines.forEach(line => { addLine(line, 10); checkPage() })
      y += 2
    })

    // Section 4: Study Plan placeholder
    checkPage()
    addSection('7-Day Study Plan')
    addLine('Visit the Study Coach to generate your personalized study plan.', 10, false, [139, 138, 160])

    addFooter()
    const userName = 'student'
    const dateStr = new Date().toISOString().split('T')[0]
    doc.save(`acadiq-report-${userName}-${dateStr}.pdf`)
    setToast({ message: 'Report downloaded!', type: 'success' })
  }

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]" style={{ fontFamily: 'Satoshi, sans-serif' }}>
      <Toast message={toast.message} type={toast.type} onClose={() => setToast({ message: '', type: '' })} />
      <Navbar />
      <div className="max-w-7xl mx-auto px-6 pt-28 pb-16">
        <div className="mb-8 flex items-start justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-3xl font-bold text-[var(--text-primary)]" style={{ fontFamily: 'Clash Display, sans-serif' }}>Your Results</h1>
            <p className="text-[var(--text-secondary)] mt-1">Here's your personalized academic performance analysis.</p>
          </div>
          <div className="flex gap-2 flex-wrap">
            <button onClick={handleDownloadBadge}
              className="flex items-center gap-2 px-4 py-2 bg-transparent border border-[#6C63FF]/50 hover:border-[#6C63FF] text-[#6C63FF] rounded-xl text-sm font-medium transition-colors">
              <Award size={14} /> Download Badge
            </button>
            <button onClick={handleDownloadPDF}
              className="flex items-center gap-2 px-4 py-2 bg-[#6C63FF] hover:bg-[#5B52EE] text-white rounded-xl text-sm font-medium transition-colors">
              <Download size={14} /> Download Report
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[1fr_420px] gap-8">
          {/* Left Column */}
          <div className="space-y-6">
            <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-8">
              <div className="flex flex-col md:flex-row items-center gap-8">
                <ScoreRing score={result.predicted_score} />
                <div className="flex-1 space-y-4">
                  <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold border ${isPass ? 'bg-[#00D4AA]/20 text-[#00D4AA] border-[#00D4AA]/40' : 'bg-[#FF4D6D]/20 text-[#FF4D6D] border-[#FF4D6D]/40'}`}>
                    {isPass ? '🎉 Pass' : '✗ Fail'}
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-2">
                      <span className="text-[var(--text-secondary)]">Pass Probability</span>
                      <span className="text-[#00D4AA] font-semibold">{result.pass_probability}%</span>
                    </div>
                    <div className="h-2 bg-[#1E1E2E] rounded-full overflow-hidden">
                      <div className="h-full bg-gradient-to-r from-[#6C63FF] to-[#00D4AA] rounded-full transition-all duration-1000" style={{ width: `${result.pass_probability}%` }} />
                    </div>
                    <div className="flex justify-between text-xs mt-1 text-[var(--text-muted)]">
                      <span>Fail: {result.fail_probability}%</span>
                      <span>Pass: {result.pass_probability}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className={`bg-gradient-to-br ${archetype.gradient} border ${archetype.border} rounded-2xl p-6`}>
              <div className="flex items-start gap-4">
                <div className="w-14 h-14 rounded-xl flex items-center justify-center flex-shrink-0" style={{ backgroundColor: `${archetype.color}20`, color: archetype.color }}>
                  {archetype.icon}
                </div>
                <div className="flex-1">
                  <h3 className="text-2xl font-bold text-[var(--text-primary)] mb-1" style={{ fontFamily: 'Clash Display, sans-serif' }}>{result.learner_type}</h3>
                  <p className="text-sm text-[var(--text-secondary)] mb-3">{archetype.desc}</p>
                  <div className="flex flex-wrap gap-2">
                    {archetype.tags.map(tag => (
                      <span key={tag} className="px-3 py-1 rounded-full text-xs font-medium border" style={{ color: archetype.color, borderColor: `${archetype.color}40`, backgroundColor: `${archetype.color}10` }}>{tag}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-6">
              <h3 className="font-bold text-[var(--text-primary)] mb-4" style={{ fontFamily: 'Clash Display, sans-serif' }}>Personalized Recommendations</h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {result.recommendations.slice(0, 6).map((rec, i) => {
                  const color = CATEGORY_COLORS[rec.category] || '#6C63FF'
                  return (
                    <div key={i} className="bg-[var(--bg-primary)] border border-[var(--border)] rounded-xl p-4">
                      <span className="inline-block px-2 py-0.5 rounded-full text-xs font-semibold mb-2" style={{ color, backgroundColor: `${color}15` }}>{rec.category.toUpperCase()}</span>
                      <p className="text-sm text-[var(--text-secondary)] leading-relaxed">{rec.message}</p>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-6">
              <h3 className="font-bold text-[var(--text-primary)] mb-4" style={{ fontFamily: 'Clash Display, sans-serif' }}>Profile vs Average</h3>
              <RadarChart studentInput={input} animationDuration={1200} />
            </div>

            {result.top_weaknesses.length > 0 && (
              <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-6">
                <h3 className="font-bold text-[var(--text-primary)] mb-4 flex items-center gap-2" style={{ fontFamily: 'Clash Display, sans-serif' }}>
                  <TrendingDown size={18} className="text-[#FF4D6D]" />
                  Key Areas for Improvement
                </h3>
                <div className="space-y-4">
                  {result.top_weaknesses.map((w, i) => {
                    const pctBelow = Math.abs(w.delta / w.dataset_average * 100).toFixed(0)
                    const studentPct = Math.min(100, (w.student_value / (w.dataset_average * 1.5)) * 100)
                    const avgPct = Math.min(100, (w.dataset_average / (w.dataset_average * 1.5)) * 100)
                    return (
                      <div key={i} className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-sm font-medium text-[var(--text-primary)] capitalize">{w.feature.replace(/_/g, ' ')}</span>
                          <span className="text-xs text-[#FF4D6D]">{pctBelow}% below avg</span>
                        </div>
                        <div className="relative h-2 bg-[#1E1E2E] rounded-full overflow-hidden">
                          <div className="absolute h-full bg-[#FF4D6D]/40 rounded-full" style={{ width: `${avgPct}%` }} />
                          <div className="absolute h-full bg-[#FF4D6D] rounded-full" style={{ width: `${studentPct}%` }} />
                        </div>
                        <div className="flex justify-between text-xs text-[var(--text-muted)]">
                          <span>You: {w.student_value.toFixed(1)}</span>
                          <span>Avg: {w.dataset_average.toFixed(1)}</span>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            <div className="bg-gradient-to-br from-[#6C63FF]/10 to-[#00D4AA]/5 border border-[#6C63FF]/30 rounded-2xl p-6 text-center">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#6C63FF] to-[#00D4AA] flex items-center justify-center mx-auto mb-4">
                <MessageSquare size={22} className="text-white" />
              </div>
              <h3 className="font-bold text-[var(--text-primary)] mb-2" style={{ fontFamily: 'Clash Display, sans-serif' }}>Ready to improve?</h3>
              <p className="text-sm text-[var(--text-secondary)] mb-4">Talk to your AI coach and get a personalized 7-day study plan.</p>
              <button onClick={() => navigate('/coach', { state: { result, input } })}
                className="w-full py-3 bg-[#6C63FF] hover:bg-[#5B52EE] text-white font-semibold rounded-xl transition-colors text-sm flex items-center justify-center gap-2">
                Open Study Coach <ArrowRight size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
