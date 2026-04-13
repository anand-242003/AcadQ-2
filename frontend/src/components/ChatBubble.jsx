import { Sparkles } from 'lucide-react'

function formatTime(timestamp) {
  if (!timestamp) return ''
  const d = new Date(timestamp)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

export default function ChatBubble({ role, message, timestamp }) {
  const isUser = role === 'user'

  if (isUser) {
    return (
      <div className="flex justify-end animate-slide-in-right">
        <div className="max-w-[75%]">
          <div className="bg-[#6C63FF] rounded-2xl rounded-tr-sm px-4 py-3">
            <p className="text-white text-sm leading-relaxed whitespace-pre-wrap">{message}</p>
          </div>
          {timestamp && (
            <p className="text-[var(--text-muted)] text-xs mt-1 text-right">{formatTime(timestamp)}</p>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="flex items-start gap-3 animate-slide-in-left">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gradient-to-br from-[#6C63FF] to-[#00D4AA] flex items-center justify-center mt-1">
        <Sparkles size={14} className="text-white" />
      </div>
      <div className="max-w-[75%]">
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-2xl rounded-tl-sm px-4 py-3">
          <p className="text-[var(--text-primary)] text-sm leading-relaxed whitespace-pre-wrap">{message}</p>
        </div>
        {timestamp && (
          <p className="text-[var(--text-muted)] text-xs mt-1">{formatTime(timestamp)}</p>
        )}
      </div>
    </div>
  )
}
