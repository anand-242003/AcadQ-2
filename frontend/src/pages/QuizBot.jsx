import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Navbar from '../components/Navbar'
import { quizAPI } from '../api/client'

export default function QuizBot() {
  const [topic, setTopic] = useState('')
  const [count, setCount] = useState(5)
  const [level, setLevel] = useState('Beginner')
  const [difficulty, setDifficulty] = useState('Easy')
  const [language, setLanguage] = useState('English')
  
  const [loading, setLoading] = useState(false)
  const [quizData, setQuizData] = useState(null)
  
  const [currentQIndex, setCurrentQIndex] = useState(0)
  const [answers, setAnswers] = useState({}) // { questionNumber: selectedLabel }
  const [showResults, setShowResults] = useState(false)

  const handleGenerate = async (e) => {
    e.preventDefault()
    if (!topic) return
    
    setLoading(true)
    setQuizData(null)
    setAnswers({})
    setCurrentQIndex(0)
    setShowResults(false)
    
    try {
      const res = await quizAPI.generate({
        topic,
        count: Number(count),
        level,
        difficulty,
        distractor_count: 3,
        language
      })
      setQuizData(res.data)
    } catch (err) {
      console.error(err)
      alert("Failed to generate quiz. Check server.")
    } finally {
      setLoading(false)
    }
  }

  const handleOptionSelect = (label) => {
    if (showResults) return
    setAnswers(prev => ({ ...prev, [currentQIndex]: label }))
  }

  const handleNext = () => {
    if (currentQIndex < quizData.questions.length - 1) {
      setCurrentQIndex(currentQIndex + 1)
    } else {
      setShowResults(true)
    }
  }

  const currentQ = quizData?.questions[currentQIndex]
  const score = showResults ? Object.keys(answers).reduce((acc, index) => {
    return acc + (answers[index] === quizData.questions[index].correct_option_label ? 1 : 0)
  }, 0) : 0

  return (
    <div className="min-h-screen bg-[#0A0A0F] text-white flex flex-col font-sans">
      <Navbar />
      {/* Add padding top to prevent overlap with fixed navbar */}
      <main className="flex-1 max-w-5xl w-full mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-[350px_1fr] gap-8 pt-24">
        
        {/* Settings Panel */}
        <div className="bg-[#1A1A24] rounded-2xl p-6 border border-[#2D2D3D] flex flex-col">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <span className="text-[#6C63FF]">✨</span> Quiz Generator
          </h2>
          
          <form onSubmit={handleGenerate} className="flex flex-col gap-4 flex-1">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Topic</label>
              <input 
                type="text" 
                value={topic}
                onChange={e => setTopic(e.target.value)}
                placeholder="e.g. Photosynthesis, React Hooks..."
                className="w-full bg-[#0F0F16] border border-[#2D2D3D] rounded-lg px-4 py-2.5 focus:border-[#6C63FF] focus:outline-none transition-colors"
                required
              />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Questions</label>
                <input 
                  type="number" 
                  min="1" max="20"
                  value={count}
                  onChange={e => setCount(e.target.value)}
                  className="w-full bg-[#0F0F16] border border-[#2D2D3D] rounded-lg px-4 py-2.5 focus:border-[#6C63FF] focus:outline-none transition-colors"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Language</label>
                <select 
                  value={language}
                  onChange={e => setLanguage(e.target.value)}
                  className="w-full bg-[#0F0F16] border border-[#2D2D3D] rounded-lg px-4 py-2.5 focus:border-[#6C63FF] focus:outline-none transition-colors"
                >
                  <option>English</option>
                  <option>Spanish</option>
                  <option>French</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-1">Level</label>
              <select 
                value={level}
                onChange={e => setLevel(e.target.value)}
                className="w-full bg-[#0F0F16] border border-[#2D2D3D] rounded-lg px-4 py-2.5 focus:border-[#6C63FF] focus:outline-none transition-colors"
              >
                <option>Beginner</option>
                <option>Intermediate</option>
                <option>Advanced</option>
              </select>
            </div>

            <div>
              <label className="block text-sm text-gray-400 mb-1">Difficulty</label>
              <select 
                value={difficulty}
                onChange={e => setDifficulty(e.target.value)}
                className="w-full bg-[#0F0F16] border border-[#2D2D3D] rounded-lg px-4 py-2.5 focus:border-[#6C63FF] focus:outline-none transition-colors"
              >
                <option>Easy</option>
                <option>Medium</option>
                <option>Hard</option>
              </select>
            </div>

            <button 
              type="submit"
              disabled={loading || !topic}
              className="mt-auto bg-gradient-to-r from-[#6C63FF] to-[#00F0FF] text-white font-semibold py-3 rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Generating...' : 'Generate Quiz'}
            </button>
          </form>
        </div>

        {/* Quiz Display Area */}
        <div className="bg-[#1A1A24] rounded-2xl border border-[#2D2D3D] overflow-hidden flex flex-col">
          {loading ? (
             <div className="flex-1 flex flex-col items-center justify-center p-12 text-center text-gray-400">
               <div className="w-12 h-12 rounded-full border-4 border-[#6C63FF]/30 border-t-[#6C63FF] animate-spin mb-4" />
               <p>AI is crafting your quiz...</p>
             </div>
          ) : !quizData ? (
             <div className="flex-1 flex flex-col items-center justify-center p-12 text-center text-gray-400">
               <div className="text-4xl mb-4">🤖</div>
               <h3 className="text-xl font-medium text-white mb-2">Ready to test your knowledge?</h3>
               <p className="max-w-xs">Fill out the settings on the left to generate a personalized AI quiz.</p>
             </div>
          ) : (
            <div className="flex flex-col h-full">
              {/* Quiz Header */}
              <div className="p-6 border-b border-[#2D2D3D] flex justify-between items-center bg-[#15151D]">
                <h3 className="font-bold text-lg text-[#00F0FF]">{quizData.title}</h3>
                <span className="text-sm font-medium bg-[#2D2D3D] px-3 py-1 rounded-full text-white">
                  Question {currentQIndex + 1} / {quizData.questions.length}
                </span>
              </div>

              {/* Question Body */}
              <div className="p-8 flex-1 overflow-y-auto">
                <AnimatePresence mode="wait">
                  <motion.div 
                    key={currentQIndex}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    className="max-w-2xl mx-auto"
                  >
                    <h2 className="text-2xl font-serif text-white mb-8 leading-snug">
                      {currentQ?.question}
                    </h2>
                    
                    <div className="space-y-4">
                      {currentQ?.options.map((opt) => {
                        const isSelected = answers[currentQIndex] === opt.label
                        const isCorrect = opt.label === currentQ.correct_option_label
                        
                        let bgColor = "bg-[#2D2D3D] hover:bg-[#3D3D4D]"
                        let borderColor = "border-transparent"
                        
                        if (showResults) {
                          if (isCorrect) {
                            bgColor = "bg-green-500/20"
                            borderColor = "border-green-500"
                          } else if (isSelected && !isCorrect) {
                            bgColor = "bg-red-500/20"
                            borderColor = "border-red-500"
                          } else {
                            bgColor = "bg-[#2D2D3D]/50"
                          }
                        } else if (isSelected) {
                          bgColor = "bg-[#6C63FF]/20"
                          borderColor = "border-[#6C63FF]"
                        }

                        return (
                          <button
                            key={opt.label}
                            onClick={() => handleOptionSelect(opt.label)}
                            className={`w-full text-left p-4 rounded-xl border-2 transition-all duration-200 flex items-center gap-4 ${bgColor} ${borderColor}`}
                          >
                            <span className={`flex items-center justify-center w-8 h-8 rounded-lg text-sm font-bold ${showResults && isCorrect ? 'bg-green-500 text-white' : showResults && isSelected ? 'bg-red-500 text-white' : isSelected ? 'bg-[#6C63FF] text-white' : 'bg-[#15151D] text-gray-400'}`}>
                              {opt.label}
                            </span>
                            <span className={`flex-1 ${showResults ? (isCorrect ? 'text-green-400' : isSelected ? 'text-red-400' : 'text-gray-500') : 'text-gray-200'}`}>
                              {opt.text}
                            </span>
                          </button>
                        )
                      })}
                    </div>

                    {showResults && (
                      <motion.div 
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-8 p-5 rounded-xl bg-[#00F0FF]/10 text-white border border-[#00F0FF]/30"
                      >
                        <h4 className="font-bold text-[#00F0FF] mb-2 flex items-center gap-2">
                          <span>💡</span> Explanation
                        </h4>
                        <p className="text-gray-300 text-sm leading-relaxed">
                          {currentQ.explanation}
                        </p>
                      </motion.div>
                    )}
                  </motion.div>
                </AnimatePresence>
              </div>
              
              {/* Footer Controls */}
              <div className="p-6 border-t border-[#2D2D3D] flex justify-between items-center bg-[#15151D]">
                {showResults ? (
                  <div className="flex items-center gap-4 text-green-400 font-bold text-xl">
                    <span>🏆</span> Score: {score} / {quizData.questions.length}
                  </div>
                ) : (
                  <div className="text-gray-500 text-sm">
                    {answers[currentQIndex] ? '✔ Answer selected' : 'Pick an answer'}
                  </div>
                )}
                
                <button
                  onClick={handleNext}
                  disabled={!answers[currentQIndex] && !showResults}
                  className="bg-white text-black px-8 py-2.5 rounded-lg font-bold hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {showResults 
                    ? (currentQIndex < quizData.questions.length - 1 ? 'Next Explanation ➔' : 'Finish Quiz')
                    : (currentQIndex < quizData.questions.length - 1 ? 'Next Question ➔' : 'Submit Quiz')
                  }
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
