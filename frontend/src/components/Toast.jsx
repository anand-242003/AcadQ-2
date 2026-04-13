import { useEffect, useState } from 'react'
import { CheckCircle2, XCircle, X } from 'lucide-react'

export default function Toast({ message, type = 'success', onClose }) {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    if (message) {
      setVisible(true)
      const t = setTimeout(() => { setVisible(false); setTimeout(onClose, 300) }, 3000)
      return () => clearTimeout(t)
    }
  }, [message])

  if (!message) return null

  const isSuccess = type === 'success'

  return (
    <div className={`fixed top-6 right-6 z-[100] flex items-center gap-3 px-5 py-3 rounded-xl shadow-2xl text-sm font-medium max-w-sm border-l-4 transition-all duration-300 ${
      visible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-8'
    } bg-[var(--bg-card)] border border-[var(--border)] ${
      isSuccess ? 'border-l-[#00D4AA]' : 'border-l-[#FF4D6D]'
    }`}>
      {isSuccess
        ? <CheckCircle2 size={16} className="text-[#00D4AA] flex-shrink-0" />
        : <XCircle size={16} className="text-[#FF4D6D] flex-shrink-0" />
      }
      <span className="flex-1 text-[var(--text-primary)]">{message}</span>
      <button onClick={() => { setVisible(false); setTimeout(onClose, 300) }}
        className="text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors">
        <X size={14} />
      </button>
    </div>
  )
}
