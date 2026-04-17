import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Navbar from '../components/Navbar'
import { predictAPI } from '../api/client'

export default function History() {
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await predictAPI.getHistory()
        setReports(res.data.reports)
      } catch (err) {
        setError('Failed to load history')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchHistory()
  }, [])

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

  if (error) {
    return (
      <div className="min-h-screen bg-[#0A0A0F] text-white flex flex-col">
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-red-400">{error}</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#0A0A0F] text-white flex flex-col font-sans">
      <Navbar />
      
      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Analysis History</h1>
          <p className="text-gray-400">View all your past performance reports</p>
        </div>

        {reports.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📊</div>
            <h3 className="text-xl font-medium text-white mb-2">No reports yet</h3>
            <p className="text-gray-400">Complete your first analysis to see it here.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {reports.map((report, index) => (
              <motion.div
                key={report.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-[#1A1A24] rounded-2xl p-6 border border-[#2D2D3D]"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-[#00F0FF]">
                      Report #{reports.length - index}
                    </h3>
                    <p className="text-sm text-gray-400">
                      {new Date(report.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-white">
                      {report.prediction.predicted_score.toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-400">Predicted Score</div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <div className="bg-[#0F0F16] rounded-lg p-4">
                    <div className="text-sm text-gray-400 mb-1">Classification</div>
                    <div className="font-semibold text-white">{report.prediction.classification}</div>
                  </div>
                  <div className="bg-[#0F0F16] rounded-lg p-4">
                    <div className="text-sm text-gray-400 mb-1">Learner Type</div>
                    <div className="font-semibold text-white">{report.prediction.learner_type}</div>
                  </div>
                  <div className="bg-[#0F0F16] rounded-lg p-4">
                    <div className="text-sm text-gray-400 mb-1">Pass Probability</div>
                    <div className="font-semibold text-green-400">{(report.prediction.pass_probability * 100).toFixed(1)}%</div>
                  </div>
                </div>

                {report.prediction.top_weaknesses.length > 0 && (
                  <div>
                    <h4 className="font-semibold mb-2">Top Weaknesses</h4>
                    <div className="flex flex-wrap gap-2">
                      {report.prediction.top_weaknesses.slice(0, 3).map((w, i) => (
                        <span key={i} className="bg-red-500/20 text-red-400 px-3 py-1 rounded-full text-sm">
                          {w.feature}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
      
      <main className="flex-1 max-w-6xl w-full mx-auto px-6 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Analysis History</h1>
          <p className="text-gray-400">View all your past performance reports</p>
        </div>

        {reports.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📊</div>
            <h3 className="text-xl font-medium text-white mb-2">No reports yet</h3>
            <p className="text-gray-400">Complete your first analysis to see it here.</p>
          </div>
        ) : (
          <div className="space-y-6">
            {reports.map((report, index) => (
              <motion.div
                key={report.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-[#1A1A24] rounded-2xl p-6 border border-[#2D2D3D]"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-[#00F0FF]">
                      Report #{reports.length - index}
                    </h3>
                    <p className="text-sm text-gray-400">
                      {new Date(report.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold text-white">
                      {report.prediction.predicted_score.toFixed(1)}%
                    </div>
                    <div className="text-sm text-gray-400">Predicted Score</div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                  <div className="bg-[#0F0F16] rounded-lg p-4">
                    <div className="text-sm text-gray-400 mb-1">Classification</div>
                    <div className="font-semibold text-white">{report.prediction.classification}</div>
                  </div>
                  <div className="bg-[#0F0F16] rounded-lg p-4">
                    <div className="text-sm text-gray-400 mb-1">Learner Type</div>
                    <div className="font-semibold text-white">{report.prediction.learner_type}</div>
                  </div>
                  <div className="bg-[#0F0F16] rounded-lg p-4">
                    <div className="text-sm text-gray-400 mb-1">Pass Probability</div>
                    <div className="font-semibold text-green-400">{(report.prediction.pass_probability * 100).toFixed(1)}%</div>
                  </div>
                </div>

                {report.prediction.top_weaknesses.length > 0 && (
                  <div>
                    <h4 className="font-semibold mb-2">Top Weaknesses</h4>
                    <div className="flex flex-wrap gap-2">
                      {report.prediction.top_weaknesses.slice(0, 3).map((w, i) => (
                        <span key={i} className="bg-red-500/20 text-red-400 px-3 py-1 rounded-full text-sm">
                          {w.feature}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
