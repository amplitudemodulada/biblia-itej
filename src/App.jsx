import { useState, useEffect, useMemo, useCallback } from 'react'
import { Workbox } from 'workbox-window'
import {
  Menu, X, Sun, Moon, BookOpen, CheckCircle, BarChart3,
  ChevronLeft, ChevronRight, ChevronDown, Book, Sparkles,
  Trophy, Target, Flame, RotateCcw, Download,
  Play, Pause, SkipBack, SkipForward, Volume2, Gauge
} from 'lucide-react'
import { BIBLE_DATA } from './data/bibleData'

const LS_KEY_PROGRESS = 'pv-progress'
const LS_KEY_THEME = 'pv-theme'

function saveProgress(data) {
  localStorage.setItem(LS_KEY_PROGRESS, JSON.stringify(data))
}

function loadProgress() {
  try {
    const d = localStorage.getItem(LS_KEY_PROGRESS)
    return d ? JSON.parse(d) : { completed: {}, quiz: {}, answered: {} }
  } catch { return { completed: {}, quiz: {}, answered: {} } }
}

function loadTheme() {
  try {
    const t = localStorage.getItem(LS_KEY_THEME)
    return t === 'dark' || t === 'light' ? t : 'dark'
  } catch { return 'dark' }
}

function saveTheme(t) {
  localStorage.setItem(LS_KEY_THEME, t)
}

const totalBibleChapters = BIBLE_DATA.reduce((acc, b) => acc + b.totalChapters, 0)

function Sidebar({ books, currentBookId, currentChapterIdx, progress, onSelectChapter, onClose, isOpen }) {
  const [expandedBook, setExpandedBook] = useState(currentBookId)
  const [search, setSearch] = useState('')

  const toggleBook = (id) => setExpandedBook(expandedBook === id ? null : id)

  useEffect(() => {
    if (currentBookId) setExpandedBook(currentBookId)
  }, [currentBookId])

  const filteredBooks = useMemo(() => {
    if (!search.trim()) return books
    const q = search.toLowerCase()
    return books.filter(b => {
      const matchBook = b.name.toLowerCase().includes(q)
      const matchChapter = b.chapters.some(c =>
        c.title.toLowerCase().includes(q) || c.number.toString() === q
      )
      return matchBook || matchChapter
    })
  }, [books, search])

  return (
    <>
      <div className={`fixed inset-0 bg-black/50 z-30 md:hidden transition-opacity ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`} onClick={onClose} />
      <aside className={`fixed md:static inset-y-0 left-0 z-40 w-72 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-700 flex flex-col transition-transform duration-300 ${isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}>
        <div className="flex items-center justify-between p-4 border-b border-slate-200 dark:border-slate-700">
          <div className="flex items-center gap-2">
            <Book className="w-5 h-5 text-amber-500" />
            <span className="font-semibold text-slate-800 dark:text-slate-100">Livros</span>
          </div>
          <button onClick={onClose} className="md:hidden p-1 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500">
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="p-3">
          <input
            type="text"
            placeholder="Buscar livro ou capítulo..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500/50"
          />
        </div>
        <div className="flex-1 overflow-y-auto scrollbar-thin px-2 pb-4">
          {filteredBooks.map(book => {
            const isExpanded = expandedBook === book.id
            const completedInBook = book.chapters.filter(c => progress.completed[`${book.id}-${c.number}`]).length
            return (
              <div key={book.id} className="mb-1">
                <button
                  onClick={() => toggleBook(book.id)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-left transition-colors ${isExpanded ? 'bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-400' : 'hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300'}`}
                >
                  <div className="flex items-center gap-2 min-w-0">
                    <BookOpen className="w-4 h-4 shrink-0" />
                    <span className="text-sm font-medium truncate">{book.name}</span>
                  </div>
                  <div className="flex items-center gap-1.5 shrink-0">
                    <span className="text-xs text-slate-400">{completedInBook}/{book.totalChapters}</span>
                    <ChevronDown className={`w-4 h-4 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
                  </div>
                </button>
                {isExpanded && (
                  <div className="ml-2 mt-1 space-y-0.5">
                    {book.chapters.map(ch => {
                      const key = `${book.id}-${ch.number}`
                      const isCompleted = progress.completed[key]
                      const isCurrent = book.id === currentBookId && ch.number === currentChapterIdx + 1
                      return (
                        <button
                          key={ch.number}
                          onClick={() => { onSelectChapter(book.id, ch.number - 1); onClose() }}
                          className={`w-full flex items-center gap-2 px-3 py-1.5 rounded-lg text-left text-sm transition-colors ${isCurrent ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-300 font-medium' : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'}`}
                        >
                          {isCompleted ? (
                            <CheckCircle className="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                          ) : (
                            <span className="w-3.5 h-3.5 shrink-0 flex items-center justify-center">
                              <span className="w-1.5 h-1.5 rounded-full bg-slate-300 dark:bg-slate-600" />
                            </span>
                          )}
                          <span className="truncate">{ch.number}. {ch.title}</span>
                        </button>
                      )
                    })}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </aside>
    </>
  )
}

function Home({ progress, onStartReading, onShowDashboard }) {
  const dailyReflection = useMemo(() => {
    const today = new Date().toISOString().split('T')[0]
    let hash = 0
    for (let i = 0; i < today.length; i++) { hash = ((hash << 5) - hash) + today.charCodeAt(i); hash |= 0 }
    const idx = Math.abs(hash) % 1189
    let counter = 0
    for (const book of BIBLE_DATA) {
      for (const ch of book.chapters) {
        if (counter === idx) {
          return { book: book.name, chapter: ch.number, title: ch.title, text: ch.reflection }
        }
        counter++
      }
    }
    return { book: '', chapter: 1, title: '', text: 'Que a paz de Deus esteja com você hoje. Leia a Bíblia e medite na sua palavra.' }
  }, [])

  const stats = useMemo(() => {
    let completed = 0
    let total = 0
    BIBLE_DATA.forEach(book => {
      book.chapters.forEach(ch => {
        total++
        if (progress.completed[`${book.id}-${ch.number}`]) completed++
      })
    })
    return { completed, total, pct: total > 0 ? Math.round((completed / total) * 100) : 0 }
  }, [progress])

  const streak = useMemo(() => {
    const dates = Object.values(progress.completed || {}).filter(v => typeof v === 'string').map(v => v.split('T')[0])
    if (dates.length === 0) return 0
    const unique = [...new Set(dates)].sort().reverse()
    const today = new Date().toISOString().split('T')[0]
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0]
    if (unique[0] !== today && unique[0] !== yesterday) return 0
    let count = 1
    let expected = new Date(unique[0])
    for (let i = 1; i < unique.length; i++) {
      expected.setDate(expected.getDate() - 1)
      if (unique[i] === expected.toISOString().split('T')[0]) count++
      else break
    }
    return count
  }, [progress])

  const lastRead = useMemo(() => {
    const entries = Object.entries(progress.completed || {})
    if (entries.length === 0) return null
    const sorted = entries.sort((a, b) => new Date(b[1]) - new Date(a[1]))
    const [key] = sorted[0]
    const parts = key.split('-')
    const bookId = parts.slice(0, -1).join('-')
    const chNum = parseInt(parts[parts.length - 1])
    const book = BIBLE_DATA.find(b => b.id === bookId)
    return book ? { book: book.name, chapter: chNum } : null
  }, [progress])

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
        <div className="text-center mb-10">
          <div className="p-4 rounded-full bg-amber-100 dark:bg-amber-900/30 mx-auto mb-5 w-fit">
            <Book className="w-10 h-10 text-amber-600 dark:text-amber-400" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold text-slate-800 dark:text-slate-100 mb-2">Palavra Viva</h1>
          <p className="text-slate-500 dark:text-slate-400 text-lg">Sua leitura bíblica passo a passo</p>
        </div>

        <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 mb-6">
          <div className="flex items-start gap-4">
            <div className="p-2 rounded-xl bg-gradient-to-br from-amber-400 to-amber-600 shrink-0 mt-1">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-1">Reflexão do Dia</h2>
              <p className="text-xs text-amber-600 dark:text-amber-400 font-medium mb-3">{dailyReflection.book} — Capítulo {dailyReflection.chapter}</p>
              <p className="text-slate-600 dark:text-slate-400 leading-relaxed">{dailyReflection.text}</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-3 mb-6">
          <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-4 text-center">
            <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{stats.pct}%</div>
            <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">Concluído</div>
          </div>
          <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-4 text-center">
            <div className="text-2xl font-bold text-amber-600 dark:text-amber-400">{stats.completed}</div>
            <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">Capítulos</div>
          </div>
          <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-4 text-center">
            <div className="flex items-center justify-center gap-1">
              <Flame className="w-5 h-5 text-orange-500" />
              <span className="text-2xl font-bold text-orange-600 dark:text-orange-400">{streak}</span>
            </div>
            <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">Dias seguidos</div>
          </div>
        </div>

        {lastRead && (
          <div className="text-center mb-6">
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Última leitura: <span className="font-medium text-slate-700 dark:text-slate-300">{lastRead.book} {lastRead.chapter}</span>
            </p>
          </div>
        )}

        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <button
            onClick={onStartReading}
            className="inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-semibold shadow-lg shadow-amber-500/25 hover:shadow-amber-500/40 transition-all active:scale-[0.98]"
          >
            <BookOpen className="w-5 h-5" />
            Começar Leitura
          </button>
          <button
            onClick={onShowDashboard}
            className="inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl border border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 font-medium transition-all"
          >
            <BarChart3 className="w-5 h-5" />
            Ver Progresso
          </button>
        </div>
      </div>
    </div>
  )
}

function Dashboard({ progress }) {
  const stats = useMemo(() => {
    let completed = 0
    let total = 0
    BIBLE_DATA.forEach(book => {
      book.chapters.forEach(ch => {
        total++
        if (progress.completed[`${book.id}-${ch.number}`]) completed++
      })
    })
    const pct = total > 0 ? Math.round((completed / total) * 100) : 0
    return { completed, total, pct }
  }, [progress])

  const streak = useMemo(() => {
    const dates = Object.values(progress.completed || {})
      .filter(v => typeof v === 'string')
      .map(v => v.split('T')[0])

    if (dates.length === 0) return 0

    const unique = [...new Set(dates)].sort().reverse()
    const today = new Date().toISOString().split('T')[0]
    const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0]

    if (unique[0] !== today && unique[0] !== yesterday) return 0

    let count = 1
    let expected = new Date(unique[0])
    for (let i = 1; i < unique.length; i++) {
      expected.setDate(expected.getDate() - 1)
      const expectedStr = expected.toISOString().split('T')[0]
      if (unique[i] === expectedStr) {
        count++
      } else if (unique[i] < expectedStr) {
        break
      }
    }
    return count
  }, [progress])

  return (
    <div className="max-w-2xl mx-auto animate-fade-in">
      <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-6">Seu Progresso</h2>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-emerald-100 dark:bg-emerald-900/30">
              <Trophy className="w-5 h-5 text-emerald-600 dark:text-emerald-400" />
            </div>
          </div>
          <div className="text-2xl font-bold text-slate-800 dark:text-slate-100">{stats.pct}%</div>
          <div className="text-sm text-slate-500 dark:text-slate-400 mt-1">Bíblia concluída</div>
          <div className="mt-2 w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
            <div className="bg-emerald-500 h-2 rounded-full transition-all duration-500" style={{ width: `${stats.pct}%` }} />
          </div>
        </div>
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/30">
              <Target className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
          <div className="text-2xl font-bold text-slate-800 dark:text-slate-100">{stats.completed}</div>
          <div className="text-sm text-slate-500 dark:text-slate-400 mt-1">Capítulos lidos</div>
          <div className="text-xs text-slate-400 mt-1">de {stats.total} no total</div>
        </div>
        <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="p-2 rounded-lg bg-amber-100 dark:bg-amber-900/30">
              <Flame className="w-5 h-5 text-amber-600 dark:text-amber-400" />
            </div>
          </div>
          <div className="text-2xl font-bold text-slate-800 dark:text-slate-100">{streak}</div>
          <div className="text-sm text-slate-500 dark:text-slate-400 mt-1">Dias consecutivos</div>
          <div className="text-xs text-slate-400 mt-1">Continue firme!</div>
        </div>
      </div>
      <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5">
        <h3 className="font-semibold text-slate-800 dark:text-slate-100 mb-4">Progresso por Livro</h3>
        <div className="space-y-3">
          {BIBLE_DATA.map(book => {
            const completed = book.chapters.filter(c => progress.completed[`${book.id}-${c.number}`]).length
            const pct = book.totalChapters > 0 ? Math.round((completed / book.totalChapters) * 100) : 0
            return (
              <div key={book.id}>
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{book.name}</span>
                  <span className="text-xs text-slate-500">{completed}/{book.totalChapters}</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5">
                  <div className="bg-amber-500 h-1.5 rounded-full transition-all duration-500" style={{ width: `${pct}%` }} />
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}

function QuizSection({ quiz, chapterKey, progress, onAnswer }) {
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

function ReadingView({ chapter, bookId, bookName, progress, onComplete, onQuizAnswer }) {
  const [showIrAlem, setShowIrAlem] = useState(false)
  const [irAlemTab, setIrAlemTab] = useState('reflection')
  const [audioPlaying, setAudioPlaying] = useState(false)
  const [audioPaused, setAudioPaused] = useState(false)
  const [audioVerseIdx, setAudioVerseIdx] = useState(null)
  const [audioRate, setAudioRate] = useState(1)

  const verses = chapter.verses || [chapter.text]

  const speakVerse = useCallback((idx) => {
    if (!window.speechSynthesis) return
    window.speechSynthesis.cancel()
    const u = new SpeechSynthesisUtterance(verses[idx])
    u.lang = 'pt-BR'
    u.rate = audioRate
    u.onend = () => {
      if (idx < verses.length - 1) {
        setAudioVerseIdx(idx + 1)
      } else {
        setAudioPlaying(false)
        setAudioPaused(false)
        setAudioVerseIdx(null)
      }
    }
    u.onerror = () => { setAudioPlaying(false); setAudioPaused(false); setAudioVerseIdx(null) }
    window.speechSynthesis.speak(u)
  }, [verses, audioRate])

  useEffect(() => {
    if (audioVerseIdx !== null && audioPlaying) {
      speakVerse(audioVerseIdx)
    }
  }, [audioVerseIdx, audioPlaying, speakVerse])

  useEffect(() => {
    return () => { window.speechSynthesis?.cancel() }
  }, [chapter.number])

  const togglePlay = () => {
    if (!audioPlaying) {
      if (audioPaused) {
        window.speechSynthesis.resume()
        setAudioPaused(false)
      } else {
        const startIdx = audioVerseIdx !== null ? audioVerseIdx : 0
        setAudioVerseIdx(startIdx)
        setAudioPlaying(true)
      }
    } else {
      if (window.speechSynthesis.speaking) {
        window.speechSynthesis.pause()
        setAudioPaused(true)
      } else {
        setAudioPlaying(false)
      }
    }
  }

  const stopAudio = () => {
    window.speechSynthesis?.cancel()
    setAudioPlaying(false)
    setAudioPaused(false)
    setAudioVerseIdx(null)
  }

  const skipTo = (idx) => {
    window.speechSynthesis?.cancel()
    setAudioVerseIdx(idx)
    if (!audioPlaying) setAudioPlaying(true)
    setAudioPaused(false)
  }

  const key = `${bookId}-${chapter.number}`
  const isCompleted = progress.completed[key]

  useEffect(() => {
    setShowIrAlem(false)
    stopAudio()
  }, [chapter.number])

  const handleScroll = useCallback((e) => {
    const el = e.currentTarget
    const scrolled = el.scrollTop
    const threshold = el.scrollHeight - el.clientHeight - 300
    if (scrolled > threshold) setShowIrAlem(true)
  }, [])

  const handleComplete = () => {
    onComplete(chapter.number - 1)
  }

  const sectionKey = `${chapter.number}-${irAlemTab}`
  
  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <div className="flex-1 overflow-y-auto" onScroll={handleScroll}>
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-2 flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
            <BookOpen className="w-4 h-4" />
            <span>{bookName}</span>
            <span className="text-slate-300 dark:text-slate-600">•</span>
            <span>Capítulo {chapter.number}</span>
            <span className="px-1.5 py-0.5 rounded bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300 text-[10px] font-semibold uppercase tracking-wide">NTLH</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-800 dark:text-slate-100 mb-6">{chapter.title}</h1>

          <div className="flex items-center gap-2 mb-6 p-3 rounded-xl bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700">
            <button
              onClick={togglePlay}
              className={`p-2.5 rounded-lg transition-all ${audioPlaying ? 'bg-amber-500 hover:bg-amber-600 text-white shadow-lg shadow-amber-500/20' : 'bg-white dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-600 dark:text-slate-300'}`}
              title={audioPlaying && !audioPaused ? 'Pausar' : 'Ouvir capítulo'}
            >
              {audioPlaying && !audioPaused ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            </button>
            {audioPlaying && (
              <>
                <button
                  onClick={() => skipTo(Math.max(0, (audioVerseIdx || 0) - 1))}
                  disabled={audioVerseIdx === 0 || audioVerseIdx === null}
                  className="p-2 rounded-lg hover:bg-white dark:hover:bg-slate-700 text-slate-500 disabled:opacity-30 transition-all"
                >
                  <SkipBack className="w-4 h-4" />
                </button>
                <button
                  onClick={() => skipTo(Math.min(verses.length - 1, (audioVerseIdx || 0) + 1))}
                  disabled={audioVerseIdx === verses.length - 1 || audioVerseIdx === null}
                  className="p-2 rounded-lg hover:bg-white dark:hover:bg-slate-700 text-slate-500 disabled:opacity-30 transition-all"
                >
                  <SkipForward className="w-4 h-4" />
                </button>
                <button
                  onClick={stopAudio}
                  className="p-2 rounded-lg hover:bg-white dark:hover:bg-slate-700 text-red-500 transition-all"
                  title="Parar"
                >
                  <X className="w-4 h-4" />
                </button>
              </>
            )}
            <div className="flex items-center gap-1.5 ml-auto">
              <Volume2 className="w-3.5 h-3.5 text-slate-400" />
              <div className="flex gap-0.5">
                {[0.75, 1, 1.25, 1.5].map(rate => (
                  <button
                    key={rate}
                    onClick={() => { stopAudio(); setAudioRate(rate) }}
                    className={`px-1.5 py-0.5 rounded text-[11px] font-medium transition-all ${audioRate === rate ? 'bg-amber-500 text-white' : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-300'}`}
                  >
                    {rate}x
                  </button>
                ))}
              </div>
            </div>
            {audioPlaying && audioVerseIdx !== null && (
              <span className="text-[11px] text-slate-400 font-medium shrink-0">
                {audioVerseIdx + 1}/{verses.length}
              </span>
            )}
          </div>

          <div className="mb-12">
            {chapter.verses && chapter.verses.length > 0 ? (
              <div className="space-y-3">
                {chapter.verses.map((v, i) => (
                  <p
                    key={i}
                    onClick={() => { if (!audioPlaying) { skipTo(i) } else { stopAudio(); skipTo(i) } }}
                    className={`text-base sm:text-lg leading-relaxed font-serif cursor-pointer rounded-lg transition-all ${audioVerseIdx === i && audioPlaying ? 'bg-amber-50 dark:bg-amber-900/20 px-4 -mx-4 py-3 text-amber-800 dark:text-amber-200 shadow-sm' : audioVerseIdx === i && audioPaused ? 'bg-amber-50/50 dark:bg-amber-900/10 px-4 -mx-4 py-3 text-slate-700 dark:text-slate-300' : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800/50 px-2 -mx-2'}`}
                  >
                    <sup className="text-amber-500 dark:text-amber-400 font-semibold text-xs sm:text-sm mr-1.5 select-none">{i + 1}</sup>
                    {v}
                  </p>
                ))}
              </div>
            ) : (
              chapter.text.split('\n\n').map((paragraph, i) => (
                <p key={i} className="text-base sm:text-lg leading-relaxed text-slate-700 dark:text-slate-300 mb-4 font-serif">
                  {paragraph}
                </p>
              ))
            )}
          </div>

          {showIrAlem && (
            <div className="animate-fade-in mb-12" key={sectionKey}>
              <div className="flex items-center gap-2 mb-6">
                <div className="h-px flex-1 bg-slate-200 dark:bg-slate-700" />
                <span className="text-sm font-medium text-slate-400 dark:text-slate-500 px-3">Ir Além</span>
                <div className="h-px flex-1 bg-slate-200 dark:bg-slate-700" />
              </div>

              <div className="flex gap-1 mb-6 bg-slate-100 dark:bg-slate-800 rounded-lg p-1 w-fit">
                <button
                  onClick={() => setIrAlemTab('reflection')}
                  className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${irAlemTab === 'reflection' ? 'bg-white dark:bg-slate-700 text-amber-700 dark:text-amber-400 shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}`}
                >
                  <Sparkles className="w-4 h-4" />
                  Reflexão
                </button>
                {chapter.apologeticPoints && chapter.apologeticPoints.length > 0 && (
                  <button
                    onClick={() => setIrAlemTab('apologetics')}
                    className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-colors ${irAlemTab === 'apologetics' ? 'bg-white dark:bg-slate-700 text-amber-700 dark:text-amber-400 shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}`}
                  >
                    <Target className="w-4 h-4" />
                    Apologética
                  </button>
                )}
              </div>

              {irAlemTab === 'reflection' && (
                <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-6">
                  <div className="flex items-start gap-4">
                    <div className="p-2 rounded-lg bg-amber-100 dark:bg-amber-900/30 shrink-0 mt-1">
                      <Sparkles className="w-5 h-5 text-amber-600 dark:text-amber-400" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-3">Reflexão Devocional</h3>
                      <p className="text-slate-600 dark:text-slate-400 leading-relaxed whitespace-pre-line">
                        {chapter.reflection}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {irAlemTab === 'apologetics' && chapter.apologeticPoints && (
                <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-6">
                  <div className="flex items-start gap-4">
                    <div className="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/30 shrink-0 mt-1">
                      <Target className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-3">Pontos Apologéticos</h3>
                      <ul className="space-y-3">
                        {chapter.apologeticPoints.map((point, i) => (
                          <li key={i} className="flex items-start gap-2 text-slate-600 dark:text-slate-400">
                            <span className="w-1.5 h-1.5 rounded-full bg-blue-500 shrink-0 mt-2" />
                            <span className="leading-relaxed">{point}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {chapter.quiz && chapter.quiz.length > 0 && (
            <div className="mb-12 animate-fade-in">
              <div className="flex items-center gap-2 mb-6">
                <div className="h-px flex-1 bg-slate-200 dark:bg-slate-700" />
                <span className="text-sm font-medium text-slate-400 dark:text-slate-500 px-3">Quiz</span>
                <div className="h-px flex-1 bg-slate-200 dark:bg-slate-700" />
              </div>
              <QuizSection
                quiz={chapter.quiz}
                chapterKey={key}
                progress={progress}
                onAnswer={onQuizAnswer}
              />
            </div>
          )}
        </div>
      </div>

      <div className="border-t border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-4 sm:px-6 lg:px-8 py-4">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
            {isCompleted ? (
              <>
                <CheckCircle className="w-4 h-4 text-emerald-500" />
                <span>Capítulo concluído</span>
              </>
            ) : (
              <>
                <span className="w-4 h-4 rounded-full border-2 border-slate-300 dark:border-slate-600" />
                <span>Não concluído</span>
              </>
            )}
          </div>
          <button
            onClick={handleComplete}
            disabled={isCompleted}
            className={`inline-flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${isCompleted ? 'bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-500 cursor-not-allowed' : 'bg-amber-500 hover:bg-amber-600 text-white shadow-lg shadow-amber-500/25 hover:shadow-amber-500/40 active:scale-[0.98]'}`}
          >
            <CheckCircle className="w-4 h-4" />
            {isCompleted ? 'Concluído' : 'Concluir Capítulo'}
          </button>
        </div>
      </div>
    </div>
  )
}
function App() {
  const [theme, setTheme] = useState(loadTheme)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [activeSection, setActiveSection] = useState('home')
  const [progress, setProgress] = useState(loadProgress)
  const [currentBookId, setCurrentBookId] = useState('genesis')
  const [currentChapterIdx, setCurrentChapterIdx] = useState(0)
  const [showCompletionModal, setShowCompletionModal] = useState(false)
  const [needRefresh, setNeedRefresh] = useState(false)
  const [installPrompt, setInstallPrompt] = useState(null)
  const [wb, setWb] = useState(null)

  useEffect(() => {
    const handler = (e) => { e.preventDefault(); setInstallPrompt(e) }
    window.addEventListener('beforeinstallprompt', handler)
    return () => window.removeEventListener('beforeinstallprompt', handler)
  }, [])

  useEffect(() => {
    if ('serviceWorker' in navigator) {
      const wb = new Workbox('/sw.js')
      wb.addEventListener('waiting', () => setNeedRefresh(true))
      wb.register()
      setWb(wb)
    }
  }, [])

  const currentBook = useMemo(() => BIBLE_DATA.find(b => b.id === currentBookId), [currentBookId])
  const currentChapter = useMemo(() => currentBook?.chapters[currentChapterIdx], [currentBook, currentChapterIdx])
  const hasNextChapter = currentBook && currentChapterIdx < currentBook.chapters.length - 1

  useEffect(() => {
    const root = document.documentElement
    if (theme === 'dark') {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }
    saveTheme(theme)
  }, [theme])

  const toggleTheme = useCallback(() => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark')
  }, [])

  const handleSelectChapter = useCallback((bookId, idx) => {
    setCurrentBookId(bookId)
    setCurrentChapterIdx(idx)
    setActiveSection('reading')
    setSidebarOpen(false)
  }, [])

  const handleCompleteChapter = useCallback(() => {
    const ch = currentChapter
    if (!ch) return
    const key = `${currentBookId}-${ch.number}`
    setProgress(prev => {
      const next = {
        ...prev,
        completed: { ...prev.completed, [key]: new Date().toISOString().split('T')[0] }
      }
      saveProgress(next)
      return next
    })
    setShowCompletionModal(true)
  }, [currentBookId, currentChapter])

  const handleModalNext = useCallback(() => {
    if (hasNextChapter) {
      setCurrentChapterIdx(prev => prev + 1)
    }
    setShowCompletionModal(false)
  }, [hasNextChapter])

  const handleModalChoose = useCallback(() => {
    setShowCompletionModal(false)
    setSidebarOpen(true)
  }, [])

  const handleQuizAnswer = useCallback((chapterKey, questionIdx, correct) => {
    setProgress(prev => {
      const prevQuiz = prev.quiz?.[chapterKey] || []
      const newQuiz = [...prevQuiz]
      newQuiz[questionIdx] = correct
      const next = { ...prev, quiz: { ...prev.quiz, [chapterKey]: newQuiz } }
      saveProgress(next)
      return next
    })
  }, [])

  const completedCount = useMemo(() => {
    return Object.keys(progress.completed || {}).length
  }, [progress])

  return (
    <div className="h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      <header className="h-14 shrink-0 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between px-4 z-20">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setSidebarOpen(true)}
            className="md:hidden p-2 -ml-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500"
          >
            <Menu className="w-5 h-5" />
          </button>
          <button
            onClick={() => setSidebarOpen(prev => !prev)}
            className="hidden md:flex p-2 -ml-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500"
          >
            <Menu className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-2">
            <Book className="w-5 h-5 text-amber-500" />
            <span className="font-bold text-lg text-slate-800 dark:text-slate-100 hidden sm:inline">Palavra Viva</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="hidden sm:flex items-center gap-1 bg-slate-100 dark:bg-slate-800 rounded-lg p-0.5">
            <button
              onClick={() => setActiveSection('home')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${activeSection === 'home' ? 'bg-white dark:bg-slate-700 text-amber-700 dark:text-amber-400 shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}`}
            >
              <Book className="w-3.5 h-3.5" />
              Início
            </button>
            <button
              onClick={() => setActiveSection('reading')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${activeSection === 'reading' ? 'bg-white dark:bg-slate-700 text-amber-700 dark:text-amber-400 shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}`}
            >
              <BookOpen className="w-3.5 h-3.5" />
              Leitura
            </button>
            <button
              onClick={() => setActiveSection('dashboard')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${activeSection === 'dashboard' ? 'bg-white dark:bg-slate-700 text-amber-700 dark:text-amber-400 shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}`}
            >
              <BarChart3 className="w-3.5 h-3.5" />
              Progresso
            </button>
          </div>

          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-lg bg-slate-100 dark:bg-slate-800">
            <div className="w-20 h-1.5 rounded-full bg-slate-200 dark:bg-slate-700 overflow-hidden">
              <div
                className="h-full bg-amber-500 rounded-full transition-all duration-500"
                style={{ width: `${totalBibleChapters > 0 ? Math.min(100, (completedCount / totalBibleChapters) * 100) : 0}%` }}
              />
            </div>
            <span className="text-xs font-medium text-slate-500 dark:text-slate-400">
              {completedCount}/{totalBibleChapters}
            </span>
          </div>

          {installPrompt && (
            <button
              onClick={async () => { installPrompt.prompt(); const r = await installPrompt.userChoice; if (r.outcome === 'accepted') setInstallPrompt(null) }}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-500 hover:bg-amber-600 text-white text-xs font-medium transition-colors"
              title="Instalar aplicativo"
            >
              <Download className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Instalar</span>
            </button>
          )}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 transition-colors"
            title={theme === 'dark' ? 'Modo claro' : 'Modo escuro'}
          >
            {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          books={BIBLE_DATA}
          currentBookId={currentBookId}
          currentChapterIdx={currentChapterIdx}
          progress={progress}
          onSelectChapter={handleSelectChapter}
          onClose={() => setSidebarOpen(false)}
          isOpen={sidebarOpen}
        />

        <main className="flex-1 flex flex-col overflow-hidden">
          {activeSection === 'home' ? (
            <Home
              progress={progress}
              onStartReading={() => { if (!currentChapter) handleSelectChapter(currentBookId, 0); setActiveSection('reading') }}
              onShowDashboard={() => setActiveSection('dashboard')}
            />
          ) : activeSection === 'dashboard' ? (
            <div className="flex-1 overflow-y-auto">
              <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Dashboard progress={progress} />
              </div>
            </div>
          ) : currentChapter ? (
            <ReadingView
              key={`${currentBookId}-${currentChapter.number}`}
              chapter={currentChapter}
              bookId={currentBookId}
              bookName={currentBook?.name}
              progress={progress}
              onComplete={handleCompleteChapter}
              onQuizAnswer={handleQuizAnswer}
            />
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <p className="text-slate-400">Selecione um capítulo para começar</p>
            </div>
          )}
        </main>
      </div>

      {needRefresh && (
        <div className="fixed bottom-0 left-0 right-0 z-50 bg-amber-500 text-white px-4 py-3 flex items-center justify-between shadow-2xl animate-fade-in">
          <p className="text-sm font-medium">Nova versão disponível</p>
          <div className="flex items-center gap-2">
            <button
              onClick={() => { wb?.messageSkipWaiting(); window.location.reload() }}
              className="px-4 py-1.5 rounded-lg bg-white text-amber-700 text-sm font-semibold hover:bg-amber-50 transition-colors"
            >
              Atualizar
            </button>
            <button
              onClick={() => setNeedRefresh(false)}
              className="px-2 py-1.5 text-white/80 hover:text-white text-sm transition-colors"
            >
              Dispensar
            </button>
          </div>
        </div>
      )}

      {showCompletionModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl p-6 mx-4 max-w-sm w-full animate-fade-in">
            <div className="text-center mb-6">
              <div className="p-3 rounded-full bg-emerald-100 dark:bg-emerald-900/30 mx-auto mb-3 w-fit">
                <CheckCircle className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
              </div>
              <h3 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Capítulo concluído!</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">O que deseja fazer agora?</p>
            </div>
            <div className="space-y-2">
              <button
                onClick={handleModalNext}
                disabled={!hasNextChapter}
                className={`w-full flex items-center justify-center gap-2 px-5 py-3 rounded-xl text-sm font-medium transition-all ${hasNextChapter ? 'bg-amber-500 hover:bg-amber-600 text-white shadow-lg shadow-amber-500/25' : 'bg-slate-100 dark:bg-slate-700 text-slate-400 cursor-not-allowed'}`}
              >
                <ChevronRight className="w-4 h-4" />
                Próximo Capítulo
              </button>
              <button
                onClick={handleModalChoose}
                className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-xl text-sm font-medium border border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all"
              >
                <BookOpen className="w-4 h-4" />
                Escolher Capítulo
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
