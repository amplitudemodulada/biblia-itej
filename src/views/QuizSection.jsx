import { useState } from 'react'
import { CheckCircle, ChevronRight, RotateCcw } from 'lucide-react'

export default function QuizSection({ quiz, chapterKey, progress, onAnswer }) {
  if (!quiz || quiz.length === 0) return null

  const [currentIdx, setCurrentIdx] = useState(0)
  const [selected, setSelected] = useState(null)
  const [showResult, setShowResult] = useState(false)

  const saved = progress.quiz?.[chapterKey] || []
  const total = quiz.length
  const allDone = saved.length >= total

  const current = quiz[currentIdx]
  if (!current) return null

  const handleConfirm = () => {
    if (selected === null) return
    onAnswer(chapterKey, currentIdx, selected === current.correct)
    setShowResult(true)
  }

  const handleNext = () => {
    if (currentIdx < total - 1) {
      setCurrentIdx(prev => prev + 1)
      setSelected(null)
      setShowResult(false)
    }
  }

  const handleRestart = () => {
    setCurrentIdx(0)
    setSelected(null)
    setShowResult(false)
  }

  if (allDone) {
    const correct = saved.filter(Boolean).length
    const pct = Math.round((correct / total) * 100)
    return (
      <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-6 text-center">
        <div className="p-3 rounded-full bg-emerald-100 dark:bg-emerald-900/30 mx-auto mb-4 w-fit">
          <CheckCircle className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
        </div>
        <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-1">Quiz Concluído!</h3>
        <p className="text-3xl font-bold text-amber-500 mb-1">{correct}/{total}</p>
        <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">{pct}% de acerto</p>
        <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 mb-4 max-w-xs mx-auto">
          <div className="bg-amber-500 h-2 rounded-full transition-all" style={{ width: `${pct}%` }} />
        </div>
        <button
          onClick={handleRestart}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-slate-200 dark:border-slate-600 text-sm text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
        >
          <RotateCcw className="w-4 h-4" />
          Refazer Quiz
        </button>
      </div>
    )
  }

  const wasAnswered = saved.length > currentIdx
  const isCorrect = wasAnswered ? saved[currentIdx] : null

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <span className="text-sm text-slate-500">Questão {currentIdx + 1} de {total}</span>
        {saved.some(Boolean) && (
          <span className="text-xs text-emerald-600 dark:text-emerald-400 font-medium">
            {saved.filter(Boolean).length} acerto{saved.filter(Boolean).length !== 1 ? 's' : ''}
          </span>
        )}
      </div>

      <p className="text-lg font-medium text-slate-800 dark:text-slate-100 mb-6">{current.question}</p>

      <div className="space-y-2 mb-6">
        {current.options.map((opt, i) => {
          const label = String.fromCharCode(65 + i)
          let itemClass = 'border-slate-200 dark:border-slate-600 text-slate-700 dark:text-slate-300 hover:border-slate-300 dark:hover:border-slate-500'
          if (wasAnswered) {
            if (i === current.correct) {
              itemClass = 'border-emerald-500 bg-emerald-50 dark:bg-emerald-900/20 text-emerald-700 dark:text-emerald-300'
            } else if (i === selected) {
              itemClass = 'border-red-500 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300'
            }
          } else if (selected === i) {
            itemClass = 'border-amber-500 bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300'
          }
          return (
            <button
              key={i}
              onClick={() => !wasAnswered && setSelected(i)}
              className={`w-full text-left px-4 py-3 rounded-lg border transition-all text-sm ${itemClass}`}
            >
              <span className="font-medium mr-2">{label}.</span>
              {opt}
            </button>
          )
        })}
      </div>

      {wasAnswered && (
        <div className={`p-4 rounded-lg mb-4 border ${isCorrect ? 'bg-emerald-50 dark:bg-emerald-900/20 border-emerald-200 dark:border-emerald-800' : 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800'}`}>
          <p className={`font-medium mb-1 text-sm ${isCorrect ? 'text-emerald-700 dark:text-emerald-300' : 'text-red-700 dark:text-red-300'}`}>
            {isCorrect ? 'Correto!' : 'Incorreto'}
          </p>
          <p className="text-sm text-slate-600 dark:text-slate-400">{current.explanation}</p>
        </div>
      )}

      <div className="flex justify-end">
        {!wasAnswered ? (
          <button
            onClick={handleConfirm}
            disabled={selected === null}
            className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-all ${selected === null ? 'bg-slate-100 dark:bg-slate-800 text-slate-400 cursor-not-allowed' : 'bg-amber-500 hover:bg-amber-600 text-white'}`}
          >
            <CheckCircle className="w-4 h-4" />
            Confirmar
          </button>
        ) : (
          <button
            onClick={handleNext}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-amber-500 hover:bg-amber-600 text-white text-sm font-medium transition-all"
          >
            {currentIdx < total - 1 ? 'Próxima' : 'Ver Resultado'}
            <ChevronRight className="w-4 h-4" />
          </button>
        )}
      </div>
    </div>
  )
}
