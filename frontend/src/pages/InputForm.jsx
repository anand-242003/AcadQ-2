import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ChevronLeft, ChevronRight, Plus, Minus, ArrowRight } from 'lucide-react'
import Navbar from '../components/Navbar'
import { predictAPI } from '../api/client'

// ─── Custom Slider ────────────────────────────────────────────────────────────
function Slider({ label, value, min, max, step = 1, unit = '', onChange }) {
  const pct = ((value - min) / (max - min)) * 100
  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center">
        <label className="text-sm font-medium text-[var(--text-secondary)]">{label}</label>
        <span className="text-xs font-mono bg-[#6C63FF]/20 text-[#6C63FF] px-2.5 py-1 rounded-full font-semibold">
          {value}{unit}
        </span>
      </div>
      <div className="relative pt-4 pb-5">
        {/* Track */}
        <div className="relative h-1.5 bg-[#1E1E2E] rounded-full">
          <div
            className="absolute h-full bg-[#6C63FF] rounded-full transition-all duration-150"
            style={{ width: `${pct}%` }}
          />
          {/* Thumb */}
          <div
            className="absolute top-1/2 -translate-y-1/2 w-5 h-5 bg-white border-2 border-[#6C63FF] rounded-full shadow-[0_0_10px_rgba(108,99,255,0.5)] pointer-events-none transition-all duration-150"
            style={{ left: `calc(${pct}% - 10px)` }}
          />
          <input
            type="range" min={min} max={max} step={step} value={value}
            onChange={e => onChange(parseFloat(e.target.value))}
            className="absolute inset-0 w-full opacity-0 cursor-pointer h-full"
            style={{ zIndex: 10 }}
          />
        </div>
        <div className="flex justify-between mt-1">
          <span className="text-xs text-[var(--text-muted)]">{min}{unit}</span>
          <span className="text-xs text-[var(--text-muted)]">{max}{unit}</span>
        </div>
      </div>
    </div>
  )
}

// ─── Number Stepper ───────────────────────────────────────────────────────────
function NumberStepper({ label, value, min, max, onChange }) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-[var(--text-secondary)]">{label}</label>
      <div className="flex items-center gap-3">
        <button type="button"
          onClick={() => onChange(Math.max(min, value - 1))}
          className="w-10 h-10 rounded-xl bg-[var(--bg-primary)] border border-[var(--border)] hover:border-[#6C63FF]/50 flex items-center justify-center text-[var(--text-secondary)] hover:text-[#6C63FF] transition-colors">
          <Minus size={14} />
        </button>
        <input type="number" min={min} max={max} value={value}
          onChange={e => onChange(Math.min(max, Math.max(min, parseInt(e.target.value) || min)))}
          className="flex-1 text-center bg-[var(--bg-primary)] border border-[var(--border)] rounded-xl px-4 py-2.5 text-[var(--text-primary)] text-lg font-bold outline-none focus:border-[#6C63FF] transition-colors" />
        <button type="button"
          onClick={() => onChange(Math.min(max, value + 1))}
          className="w-10 h-10 rounded-xl bg-[var(--bg-primary)] border border-[var(--border)] hover:border-[#6C63FF]/50 flex items-center justify-center text-[var(--text-secondary)] hover:text-[#6C63FF] transition-colors">
          <Plus size={14} />
        </button>
      </div>
    </div>
  )
}

// ─── Pill Selector ────────────────────────────────────────────────────────────
function PillSelector({ label, options, value, onChange, error }) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-[var(--text-secondary)]">{label}</label>
      <div className="flex flex-wrap gap-2">
        {options.map(opt => (
          <button key={opt} type="button" onClick={() => onChange(opt)}
            className={`px-4 py-2 rounded-xl text-sm font-medium border transition-all duration-200 ${
              value === opt
                ? 'bg-[#6C63FF] border-[#6C63FF] text-white shadow-[0_0_12px_rgba(108,99,255,0.4)]'
                : 'bg-[var(--bg-primary)] border-[var(--border)] text-[var(--text-secondary)] hover:border-[#6C63FF]/50 hover:text-[var(--text-primary)]'
            }`}>
            {opt}
          </button>
        ))}
      </div>
      {error && <p className="text-[#FF4D6D] text-xs">{error}</p>}
    </div>
  )
}

// ─── Toggle ───────────────────────────────────────────────────────────────────
function Toggle({ label, value, onChange }) {
  const isYes = value === 'Yes'
  return (
    <div className="flex items-center justify-between py-1">
      <span className="text-sm font-medium text-[var(--text-secondary)]">{label}</span>
      <div className="flex items-center gap-3">
        <span className={`text-sm ${!isYes ? 'text-[var(--text-primary)]' : 'text-[var(--text-muted)]'}`}>No</span>
        <button type="button" onClick={() => onChange(isYes ? 'No' : 'Yes')}
          className={`relative w-12 h-6 rounded-full transition-colors duration-200 ${isYes ? 'bg-[#6C63FF]' : 'bg-[#1E1E2E]'}`}>
          <div className={`absolute top-1 w-4 h-4 bg-white rounded-full shadow transition-transform duration-200 ${isYes ? 'translate-x-7' : 'translate-x-1'}`} />
        </button>
        <span className={`text-sm ${isYes ? 'text-[var(--text-primary)]' : 'text-[var(--text-muted)]'}`}>Yes</span>
      </div>
    </div>
  )
}

// ─── Score Ring Input ─────────────────────────────────────────────────────────
function ScoreRingInput({ label, value, onChange, error }) {
  const pct = value / 100
  const radius = 28
  const circumference = 2 * Math.PI * radius
  const offset = circumference - pct * circumference
  const color = value >= 70 ? '#00D4AA' : value >= 40 ? '#FFB347' : '#FF4D6D'

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-[var(--text-secondary)]">{label}</label>
      <div className="flex items-center gap-4">
        <div className="relative flex-shrink-0">
          <svg width="72" height="72" className="-rotate-90">
            <circle cx="36" cy="36" r={radius} fill="none" stroke="#1E1E2E" strokeWidth="5" />
            <circle cx="36" cy="36" r={radius} fill="none" stroke={color} strokeWidth="5"
              strokeLinecap="round" strokeDasharray={circumference} strokeDashoffset={offset}
              style={{ transition: 'stroke-dashoffset 0.3s ease, stroke 0.3s ease' }} />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-sm font-bold" style={{ color }}>{value}</span>
          </div>
        </div>
        <div className="flex-1 flex items-center gap-2">
          <button type="button" onClick={() => onChange(Math.max(0, value - 1))}
            className="w-9 h-9 rounded-lg bg-[var(--bg-primary)] border border-[var(--border)] hover:border-[#6C63FF]/50 flex items-center justify-center text-[var(--text-secondary)] hover:text-[#6C63FF] transition-colors">
            <Minus size={12} />
          </button>
          <input type="number" min={0} max={100} value={value}
            onChange={e => onChange(Math.min(100, Math.max(0, parseInt(e.target.value) || 0)))}
            className={`flex-1 text-center bg-[var(--bg-primary)] border rounded-xl px-3 py-2 text-[var(--text-primary)] font-bold outline-none focus:border-[#6C63FF] transition-colors ${error ? 'border-[#FF4D6D]' : 'border-[var(--border)]'}`} />
          <button type="button" onClick={() => onChange(Math.min(100, value + 1))}
            className="w-9 h-9 rounded-lg bg-[var(--bg-primary)] border border-[var(--border)] hover:border-[#6C63FF]/50 flex items-center justify-center text-[var(--text-secondary)] hover:text-[#6C63FF] transition-colors">
            <Plus size={12} />
          </button>
        </div>
      </div>
      {error && <p className="text-[#FF4D6D] text-xs">{error}</p>}
    </div>
  )
}

// ─── Mental Health Picker ─────────────────────────────────────────────────────
function MentalHealthPicker({ value, onChange, error }) {
  return (
    <div className="space-y-3">
      <label className="text-sm font-medium text-[var(--text-secondary)]">Mental Health Score</label>
      <div className="flex gap-2">
        {Array.from({ length: 10 }, (_, i) => i + 1).map(n => (
          <button key={n} type="button" onClick={() => onChange(n)}
            className={`flex-1 aspect-square rounded-full text-xs font-bold border transition-all duration-200 ${
              value === n
                ? 'bg-[#6C63FF] border-[#6C63FF] text-white shadow-[0_0_10px_rgba(108,99,255,0.4)]'
                : 'bg-[var(--bg-primary)] border-[var(--border)] text-[var(--text-secondary)] hover:border-[#6C63FF]/50'
            }`}>
            {n}
          </button>
        ))}
      </div>
      <div className="flex justify-between text-xs text-[var(--text-muted)]">
        <span>Poor</span>
        <span>Excellent</span>
      </div>
      {error && <p className="text-[#FF4D6D] text-xs">{error}</p>}
    </div>
  )
}

// ─── Field Error ──────────────────────────────────────────────────────────────
function FieldError({ msg }) {
  if (!msg) return null
  return <p className="text-[#FF4D6D] text-xs mt-1">{msg}</p>
}

// ─── Default Form Values ──────────────────────────────────────────────────────
const DEFAULT_FORM = {
  age: 20, gender: 'Male', academic_level: 'Undergraduate',
  part_time_job: 'No', upcoming_deadline: 'No', internet_quality: 'Good',
  study_hours: 4, self_study_hours: 2, online_classes_hours: 1.5, topics_completed: 15,
  social_media_hours: 2, gaming_hours: 1, screen_time_hours: 5,
  sleep_hours: 7, exercise_minutes: 30, caffeine_intake_mg: 100, mental_health_score: 7,
  quiz_avg: 65, assignment_avg: 65, midterm_score: 60,
  focus_index: 60, productivity_score: 60, burnout_level: 30,
}

const STEPS = [
  { title: 'Tell us about yourself', subtitle: 'Basic information to personalize your analysis' },
  { title: 'How do you study?', subtitle: 'Tell us about your daily study routine' },
  { title: 'Screen time and distractions', subtitle: 'Honest answers give better predictions' },
  { title: 'Your lifestyle habits', subtitle: 'Wellness directly impacts academic performance' },
  { title: 'Your academic performance', subtitle: 'Enter your recent scores for accurate prediction' },
]

// ─── Loading Overlay ──────────────────────────────────────────────────────────
function LoadingOverlay({ phase }) {
  const messages = [
    'Analyzing your profile...',
    'Running ML models...',
    'Generating your results...',
  ]
  return (
    <div className="fixed inset-0 bg-[var(--bg-primary)]/90 backdrop-blur-sm z-50 flex flex-col items-center justify-center gap-6">
      <div className="w-16 h-16 rounded-full border-4 border-[#6C63FF]/30 border-t-[#6C63FF] animate-spin" />
      <div className="text-center space-y-2">
        <p className="text-[var(--text-primary)] font-semibold text-lg">{messages[phase] || messages[0]}</p>
        <div className="flex gap-1 justify-center">
          {messages.map((_, i) => (
            <div key={i} className={`w-2 h-2 rounded-full transition-colors duration-300 ${i <= phase ? 'bg-[#6C63FF]' : 'bg-[#1E1E2E]'}`} />
          ))}
        </div>
      </div>
    </div>
  )
}

// ─── Main Component ───────────────────────────────────────────────────────────
export default function InputForm() {
  const navigate = useNavigate()
  const [form, setForm] = useState(DEFAULT_FORM)
  const [step, setStep] = useState(0)
  const [direction, setDirection] = useState('next') // 'next' | 'back'
  const [animating, setAnimating] = useState(false)
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [loadingPhase, setLoadingPhase] = useState(0)
  const [apiError, setApiError] = useState('')

  const set = key => val => setForm(prev => ({ ...prev, [key]: val }))

  // ─── Validation ─────────────────────────────────────────────────────────────
  const validate = (stepIndex) => {
    const errs = {}
    if (stepIndex === 0) {
      if (!form.gender) errs.gender = 'Please select a gender'
      if (!form.academic_level) errs.academic_level = 'Please select academic level'
      if (!form.internet_quality) errs.internet_quality = 'Please select internet quality'
    }
    if (stepIndex === 4) {
      if (form.quiz_avg < 0 || form.quiz_avg > 100) errs.quiz_avg = 'Must be 0–100'
      if (form.assignment_avg < 0 || form.assignment_avg > 100) errs.assignment_avg = 'Must be 0–100'
      if (form.midterm_score < 0 || form.midterm_score > 100) errs.midterm_score = 'Must be 0–100'
    }
    return errs
  }

  // ─── Navigation ─────────────────────────────────────────────────────────────
  const goNext = () => {
    const errs = validate(step)
    if (Object.keys(errs).length) { setErrors(errs); return }
    setErrors({})
    if (step < 4) {
      setDirection('next')
      setAnimating(true)
      setTimeout(() => { setStep(s => s + 1); setAnimating(false) }, 250)
    }
  }

  const goBack = () => {
    if (step > 0) {
      setErrors({})
      setDirection('back')
      setAnimating(true)
      setTimeout(() => { setStep(s => s - 1); setAnimating(false) }, 250)
    }
  }

  // ─── Submit ──────────────────────────────────────────────────────────────────
  const handleSubmit = async () => {
    const errs = validate(4)
    if (Object.keys(errs).length) { setErrors(errs); return }
    setLoading(true)
    setLoadingPhase(0)
    setApiError('')

    const t1 = setTimeout(() => setLoadingPhase(1), 1000)
    const t2 = setTimeout(() => setLoadingPhase(2), 2000)

    try {
      const { data } = await predictAPI.predict(form)
      clearTimeout(t1); clearTimeout(t2)
      navigate('/results', { state: { result: data, input: form } })
    } catch (err) {
      clearTimeout(t1); clearTimeout(t2)
      setLoading(false)
      setApiError(
        typeof err.response?.data?.detail === 'string'
          ? err.response.data.detail
          : Array.isArray(err.response?.data?.detail)
          ? err.response.data.detail.map(e => e.msg).join(', ')
          : 'Prediction failed. Please try again.'
      )
    }
  }

  const progress = ((step + 1) / 5) * 100

  // ─── Step Content ────────────────────────────────────────────────────────────
  const stepContent = [
    // Step 1
    <div key={0} className="space-y-6">
      <NumberStepper label="Age" value={form.age} min={16} max={40} onChange={set('age')} />
      <PillSelector label="Gender" options={['Male', 'Female', 'Other']} value={form.gender} onChange={set('gender')} error={errors.gender} />
      <PillSelector label="Academic Level" options={['High School', 'Undergraduate', 'Postgraduate']} value={form.academic_level} onChange={set('academic_level')} error={errors.academic_level} />
      <Toggle label="Part-time Job" value={form.part_time_job} onChange={set('part_time_job')} />
      <Toggle label="Upcoming Deadline" value={form.upcoming_deadline} onChange={set('upcoming_deadline')} />
      <PillSelector label="Internet Quality" options={['Poor', 'Average', 'Good', 'Excellent']} value={form.internet_quality} onChange={set('internet_quality')} error={errors.internet_quality} />
    </div>,

    // Step 2
    <div key={1} className="space-y-6">
      <Slider label="Study Hours per Day" value={form.study_hours} min={0} max={16} step={0.5} unit="h" onChange={set('study_hours')} />
      {form.study_hours < 2 && (
        <p className="text-xs text-[#FFB347] bg-[#FFB347]/10 border border-[#FFB347]/20 rounded-xl px-4 py-2">
          ⚠ Consider increasing study time — less than 2 hours may not be enough for good results
        </p>
      )}
      <Slider label="Self-Study Hours per Day" value={form.self_study_hours} min={0} max={10} step={0.5} unit="h" onChange={set('self_study_hours')} />
      <Slider label="Online Class Hours per Day" value={form.online_classes_hours} min={0} max={10} step={0.5} unit="h" onChange={set('online_classes_hours')} />
      <NumberStepper label="Topics Completed" value={form.topics_completed} min={0} max={50} onChange={set('topics_completed')} />
    </div>,

    // Step 3
    <div key={2} className="space-y-6">
      <Slider label="Social Media Hours per Day" value={form.social_media_hours} min={0} max={12} step={0.5} unit="h" onChange={set('social_media_hours')} />
      <Slider label="Gaming Hours per Day" value={form.gaming_hours} min={0} max={10} step={0.5} unit="h" onChange={set('gaming_hours')} />
      <Slider label="Total Screen Time per Day" value={form.screen_time_hours} min={0} max={16} step={0.5} unit="h" onChange={set('screen_time_hours')} />
      {form.screen_time_hours < form.social_media_hours + form.gaming_hours && (
        <p className="text-xs text-[#FFB347] bg-[#FFB347]/10 border border-[#FFB347]/20 rounded-xl px-4 py-2">
          ⚠ Screen time should be ≥ social media + gaming hours
        </p>
      )}
      {form.social_media_hours > 6 && (
        <p className="text-xs text-[#FF4D6D] bg-[#FF4D6D]/10 border border-[#FF4D6D]/20 rounded-xl px-4 py-2">
          ⚠ High screen time may hurt your score — consider reducing social media to under 3 hours
        </p>
      )}
    </div>,
    <div key={3} className="space-y-6">
      <Slider label="Sleep Hours per Night" value={form.sleep_hours} min={4} max={12} step={0.5} unit="h" onChange={set('sleep_hours')} />
      {form.sleep_hours < 6 && (
        <p className="text-xs text-[#FF4D6D] bg-[#FF4D6D]/10 border border-[#FF4D6D]/20 rounded-xl px-4 py-2">
          ⚠ Low sleep affects focus and memory — aim for 7–9 hours per night
        </p>
      )}
      <Slider label="Exercise Minutes per Day" value={form.exercise_minutes} min={0} max={120} step={5} unit="min" onChange={set('exercise_minutes')} />
      <Slider label="Caffeine Intake per Day" value={form.caffeine_intake_mg} min={0} max={600} step={25} unit="mg" onChange={set('caffeine_intake_mg')} />
      <MentalHealthPicker value={form.mental_health_score} onChange={set('mental_health_score')} error={errors.mental_health_score} />
    </div>,

    // Step 5
    <div key={4} className="space-y-6">
      <ScoreRingInput label="Quiz Average Score" value={form.quiz_avg} onChange={set('quiz_avg')} error={errors.quiz_avg} />
      <ScoreRingInput label="Assignment Average Score" value={form.assignment_avg} onChange={set('assignment_avg')} error={errors.assignment_avg} />
      <ScoreRingInput label="Midterm Score" value={form.midterm_score} onChange={set('midterm_score')} error={errors.midterm_score} />
      <Slider label="Focus Index" value={form.focus_index} min={0} max={100} unit="%" onChange={set('focus_index')} />
      <Slider label="Productivity Score" value={form.productivity_score} min={0} max={100} unit="%" onChange={set('productivity_score')} />
      <Slider label="Burnout Level" value={form.burnout_level} min={0} max={100} unit="%" onChange={set('burnout_level')} />
      {apiError && (
        <div className="px-4 py-3 bg-[#FF4D6D]/10 border border-[#FF4D6D]/30 rounded-xl text-sm text-[#FF4D6D]">
          {apiError}
        </div>
      )}
    </div>,
  ]

  return (
    <div className="min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)]" style={{ fontFamily: 'Satoshi, sans-serif' }}>
      <Navbar />
      {loading && <LoadingOverlay phase={loadingPhase} />}

      <div className="flex items-center justify-center min-h-screen px-4 pt-20 pb-12">
        <div className="w-full max-w-[680px]">

          {/* Card */}
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl p-8 md:p-10">

            {/* Progress bar */}
            <div className="mb-6">
              <div className="h-1.5 bg-[#1E1E2E] rounded-full overflow-hidden">
                <div
                  className="h-full bg-[#6C63FF] rounded-full transition-all duration-500 ease-out"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <div className="flex justify-between items-center mt-2">
                <span className="text-xs text-[var(--text-muted)]">{Math.round(progress)}% complete</span>
                <span className="text-xs text-[var(--text-muted)]">Step {step + 1} of 5</span>
              </div>
            </div>

            {/* Step header */}
            <div className="mb-8">
              <h2
                className="text-3xl font-bold text-[var(--text-primary)] mb-1"
                style={{ fontFamily: 'Clash Display, sans-serif' }}
              >
                {STEPS[step].title}
              </h2>
              <p className="text-sm text-[var(--text-secondary)]">{STEPS[step].subtitle}</p>
            </div>

            {/* Step content with slide animation */}
            <div
              className="transition-all duration-250"
              style={{
                opacity: animating ? 0 : 1,
                transform: animating
                  ? `translateX(${direction === 'next' ? '-24px' : '24px'})`
                  : 'translateX(0)',
                transition: 'opacity 0.25s ease, transform 0.25s ease',
              }}
            >
              {stepContent[step]}
            </div>

            {/* Navigation */}
            <div className="flex items-center justify-between mt-10 pt-6 border-t border-[var(--border)]">
              <button
                type="button"
                onClick={goBack}
                disabled={step === 0}
                className={`flex items-center gap-2 px-5 py-2.5 rounded-xl border text-sm font-medium transition-all ${
                  step === 0
                    ? 'border-[var(--border)] text-[var(--text-muted)] cursor-not-allowed opacity-40'
                    : 'border-[var(--border)] text-[var(--text-secondary)] hover:border-[#6C63FF]/50 hover:text-[var(--text-primary)]'
                }`}
              >
                <ChevronLeft size={16} />
                Back
              </button>

              {step < 4 ? (
                <button
                  type="button"
                  onClick={goNext}
                  className="flex items-center gap-2 px-6 py-2.5 bg-[#6C63FF] hover:bg-[#5B52EE] text-white text-sm font-semibold rounded-xl transition-colors"
                >
                  Next
                  <ChevronRight size={16} />
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={loading}
                  className="flex items-center gap-2 px-6 py-2.5 bg-[#6C63FF] hover:bg-[#5B52EE] disabled:opacity-50 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-xl transition-colors"
                >
                  Analyze My Performance
                  <ArrowRight size={16} />
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
