import { useState, useEffect, useMemo, useCallback, useRef, lazy, Suspense } from 'react'
import { Workbox } from 'workbox-window'
import {
  Menu, X, Sun, Moon, BookOpen, CheckCircle, BarChart3,
  ChevronLeft, ChevronRight, ChevronDown, Book, Sparkles,
  Trophy, Target, Flame, RotateCcw, Download,
  Play, Pause, SkipBack, SkipForward, Volume2, Gauge,
  Search as SearchIcon, Share2, Star, Calendar
} from 'lucide-react'
import { BIBLE_DATA } from './data/bibleData'

const Home = lazy(() => import('./views/Home'))
const Dashboard = lazy(() => import('./views/Dashboard'))
const ReadingView = lazy(() => import('./views/ReadingView'))
const SearchView = lazy(() => import('./views/SearchView'))

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

// Reading plan: 1189 chapters / 365 days
function generateReadingPlan() {
  const allChapters = []
  for (const book of BIBLE_DATA) {
    for (const ch of book.chapters) {
      allChapters.push({ bookId: book.id, bookName: book.name, chapterNumber: ch.number, chapterTitle: ch.title })
    }
  }
  
  const plan = []
  const chaptersPerDay = Math.ceil(allChapters.length / 365) // ~3.26 -> 4
  
  for (let i = 0; i < allChapters.length; i += chaptersPerDay) {
    const day = Math.floor(i / chaptersPerDay) + 1
    plan.push({
      day,
      dateOffset: day - 1,
      chapters: allChapters.slice(i, i + chaptersPerDay)
    })
  }
  
  return plan
}

const READING_PLAN = generateReadingPlan()
const TOTAL_PLAN_DAYS = READING_PLAN.length

function loadPlanProgress() {
  try {
    const d = localStorage.getItem('pv-plan')
    return d ? JSON.parse(d) : { daysCompleted: {} }
  } catch { return { daysCompleted: {} } }
}

function savePlanProgress(data) {
  localStorage.setItem('pv-plan', JSON.stringify(data))
}

function getCurrentDayOfPlan(startDate = null) {
  const base = startDate ? new Date(startDate) : new Date('2026-01-01')
  const today = new Date()
  const diff = Math.floor((today - base) / (1000 * 60 * 60 * 24))
  return Math.max(1, Math.min(diff + 1, TOTAL_PLAN_DAYS))
}

function ReadingPlanView({ planProgress, onToggleDay, onSelectChapter, onGoToCurrentDay }) {
  const [currentView, setCurrentView] = useState('current') // 'current', 'list'
  const currentDay = useMemo(() => getCurrentDayOfPlan(), [])
  const currentDayData = READING_PLAN[currentDay - 1]
  const daysCompletedCount = useMemo(() => Object.keys(planProgress.daysCompleted || {}).length, [planProgress])

  const isDayCompleted = (day) => planProgress.daysCompleted?.[day] || false

  const todayCompleted = isDayCompleted(currentDay)

  const handleChapterClick = (chapter) => {
    onSelectChapter(chapter.bookId, chapter.chapterNumber - 1)
  }

  if (currentView === 'current') {
    return (
      <div className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-slate-800 dark:text-slate-100 mb-1">Plano de Leitura</h1>
              <p className="text-sm text-slate-500 dark:text-slate-400">Bíblia em 1 ano</p>
            </div>
            <button
              onClick={() => setCurrentView('list')}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-amber-600 dark:hover:text-amber-400 transition-colors"
            >
              <Calendar className="w-3.5 h-3.5" />
              Ver calendário
            </button>
          </div>

          <div className="grid grid-cols-3 gap-3 mb-8">
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-4 text-center">
              <div className="text-2xl font-bold text-amber-600 dark:text-amber-400">{currentDay}/{TOTAL_PLAN_DAYS}</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">Dia atual</div>
            </div>
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-4 text-center">
              <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{daysCompletedCount}</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">Dias concluídos</div>
            </div>
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-4 text-center">
              <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{TOTAL_PLAN_DAYS - daysCompletedCount}</div>
              <div className="text-xs text-slate-500 dark:text-slate-400 mt-1">Dias restantes</div>
            </div>
          </div>

          <div className={`bg-white dark:bg-slate-800 rounded-2xl border ${todayCompleted ? 'border-emerald-200 dark:border-emerald-800' : 'border-slate-200 dark:border-slate-700'} p-6 mb-6`}>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Calendar className={`w-5 h-5 ${todayCompleted ? 'text-emerald-500' : 'text-amber-500'}`} />
                <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Dia {currentDay}</h2>
                {todayCompleted && (
                  <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400">
                    <CheckCircle className="w-3 h-3" />
                    Concluído
                  </span>
                )}
              </div>
              <button
                onClick={() => onToggleDay(currentDay)}
                className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${todayCompleted ? 'bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400' : 'bg-amber-500 hover:bg-amber-600 text-white'}`}
              >
                {todayCompleted ? 'Desmarcar' : 'Marcar como lido'}
              </button>
            </div>

            <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">Leitura de hoje:</p>
            
            <div className="space-y-2">
              {currentDayData?.chapters.map((ch, i) => (
                <button
                  key={`${ch.bookId}-${ch.chapterNumber}`}
                  onClick={() => handleChapterClick(ch)}
                  className="w-full flex items-center justify-between px-4 py-3 rounded-xl hover:bg-amber-50 dark:hover:bg-amber-900/10 border border-slate-100 dark:border-slate-700 transition-colors text-left group"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <BookOpen className="w-4 h-4 text-amber-500 shrink-0" />
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-slate-700 dark:text-slate-300 truncate">
                        {ch.bookName} {ch.chapterNumber}
                      </p>
                      <p className="text-xs text-slate-400 truncate">{ch.chapterTitle}</p>
                    </div>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-amber-500 shrink-0 transition-colors" />
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  // Calendar/list view
  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-800 dark:text-slate-100 mb-1">Plano de Leitura</h1>
            <p className="text-sm text-slate-500 dark:text-slate-400">{daysCompletedCount} de {TOTAL_PLAN_DAYS} dias concluídos</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={onGoToCurrentDay}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-amber-500 hover:bg-amber-600 text-white transition-colors"
            >
              <Calendar className="w-3.5 h-3.5" />
              Dia atual
            </button>
            <button
              onClick={() => setCurrentView('current')}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-amber-600 dark:hover:text-amber-400 transition-colors"
            >
              Voltar
            </button>
          </div>
        </div>

        <div className="grid grid-cols-5 sm:grid-cols-7 md:grid-cols-10 gap-1.5">
          {READING_PLAN.map((day) => {
            const completed = isDayCompleted(day.day)
            const isToday = day.day === currentDay
            return (
              <button
                key={day.day}
                onClick={() => onSelectChapter(day.chapters[0].bookId, day.chapters[0].chapterNumber - 1)}
                className={`aspect-square rounded-lg text-xs font-medium flex flex-col items-center justify-center gap-0.5 transition-all ${
                  isToday && completed
                    ? 'bg-emerald-500 text-white shadow-lg shadow-emerald-500/30'
                    : isToday
                    ? 'bg-amber-500 text-white shadow-lg shadow-amber-500/30 ring-2 ring-amber-300 dark:ring-amber-700'
                    : completed
                    ? 'bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400'
                    : 'bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:bg-amber-50 dark:hover:bg-amber-900/10'
                }`}
              >
                {completed ? <CheckCircle className="w-3.5 h-3.5" /> : null}
                <span className={completed ? 'text-[10px]' : ''}>{day.day}</span>
              </button>
            )
          })}
        </div>

        <div className="flex items-center justify-center gap-6 mt-8 pt-4 border-t border-slate-200 dark:border-slate-700">
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded bg-amber-500" />
            <span className="text-xs text-slate-500 dark:text-slate-400">Hoje</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded bg-emerald-500" />
            <span className="text-xs text-slate-500 dark:text-slate-400">Concluído</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-3 h-3 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700" />
            <span className="text-xs text-slate-500 dark:text-slate-400">Pendente</span>
          </div>
        </div>
      </div>
    </div>
  )
}

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
  const [bookmarks, setBookmarks] = useState(() => { try { return JSON.parse(localStorage.getItem('pv-bookmarks')) || [] } catch { return [] } })
  const [planProgress, setPlanProgress] = useState(loadPlanProgress)

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

  const handleToggleBookmark = useCallback((key) => {
    setBookmarks(prev => {
      const next = prev.includes(key) ? prev.filter(k => k !== key) : [...prev, key]
      localStorage.setItem('pv-bookmarks', JSON.stringify(next))
      return next
    })
  }, [])

  const handleTogglePlanDay = useCallback((day) => {
    setPlanProgress(prev => {
      const next = {
        ...prev,
        daysCompleted: { ...prev.daysCompleted, [day]: !prev.daysCompleted?.[day] }
      }
      savePlanProgress(next)
      return next
    })
  }, [])

  const completedCount = useMemo(() => {
    return Object.keys(progress.completed || {}).length
  }, [progress])

  // New feature 1: Auto-scroll to top on chapter change
  const mainRef = useRef(null)

  useEffect(() => {
    if (mainRef.current) {
      mainRef.current.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }, [currentChapter])

  // New feature 2: Keyboard arrow key navigation
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (activeSection !== 'reading' || !currentBook) return
      if (e.key === 'ArrowLeft' && currentChapterIdx > 0) {
        e.preventDefault()
        setCurrentChapterIdx(prev => prev - 1)
      } else if (e.key === 'ArrowRight' && currentChapterIdx < currentBook.chapters.length - 1) {
        e.preventDefault()
        setCurrentChapterIdx(prev => prev + 1)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [activeSection, currentBook, currentChapterIdx])

  // New feature 3: Find first uncompleted chapter for "Continue Reading"
  const firstUncompleted = useMemo(() => {
    for (const book of BIBLE_DATA) {
      for (const ch of book.chapters) {
        const key = `${book.id}-${ch.number}`
        if (!progress.completed[key]) {
          return { bookId: book.id, chapterIdx: ch.number - 1 }
        }
      }
    }
    return null
  }, [progress])

  const handleContinueReading = useCallback(() => {
    if (firstUncompleted) {
      handleSelectChapter(firstUncompleted.bookId, firstUncompleted.chapterIdx)
    }
  }, [firstUncompleted, handleSelectChapter])

  const [touchStartX, setTouchStartX] = useState(null)
  const handleTouchStart = useCallback((e) => {
    setTouchStartX(e.touches[0].clientX)
  }, [])
  const handleTouchEnd = useCallback((e) => {
    if (touchStartX === null || activeSection !== 'reading') return
    const dx = e.changedTouches[0].clientX - touchStartX
    if (Math.abs(dx) < 50) return
    if (!currentBook) return
    if (dx < 0 && currentChapterIdx < currentBook.chapters.length - 1) {
      setCurrentChapterIdx(prev => prev + 1)
    } else if (dx > 0 && currentChapterIdx > 0) {
      setCurrentChapterIdx(prev => prev - 1)
    }
    setTouchStartX(null)
  }, [touchStartX, activeSection, currentBook, currentChapterIdx])

  const loadingFallback = (
    <div className="flex-1 flex items-center justify-center">
      <p className="text-slate-400">Carregando...</p>
    </div>
  )

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
            <button
              onClick={() => setActiveSection('search')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${activeSection === 'search' ? 'bg-white dark:bg-slate-700 text-amber-700 dark:text-amber-400 shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}`}
            >
              <SearchIcon className="w-3.5 h-3.5" />
              Buscar
            </button>
            <button
              onClick={() => setActiveSection('plan')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${activeSection === 'plan' ? 'bg-white dark:bg-slate-700 text-amber-700 dark:text-amber-400 shadow-sm' : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}`}
            >
              <Calendar className="w-3.5 h-3.5" />
              Plano
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
            onClick={() => setActiveSection('search')}
            className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 transition-colors"
            title="Buscar"
          >
            <SearchIcon className="w-4 h-4" />
          </button>
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

        <main className="flex-1 flex flex-col overflow-hidden" ref={mainRef} onTouchStart={handleTouchStart} onTouchEnd={handleTouchEnd}>
          <Suspense fallback={loadingFallback}>
            {activeSection === 'home' ? (
              <Home
                progress={progress}
                bookmarks={bookmarks}
                onStartReading={() => { if (!currentChapter) handleSelectChapter(currentBookId, 0); setActiveSection('reading') }}
                onShowDashboard={() => setActiveSection('dashboard')}
                onSelectChapter={handleSelectChapter}
                onContinueReading={firstUncompleted ? handleContinueReading : undefined}
              />
            ) : activeSection === 'dashboard' ? (
              <div className="flex-1 overflow-y-auto">
                <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                  <Dashboard progress={progress} />
                </div>
              </div>
            ) : activeSection === 'search' ? (
              <SearchView onSelectChapter={handleSelectChapter} />
            ) : activeSection === 'plan' ? (
              <ReadingPlanView
                planProgress={planProgress}
                onToggleDay={handleTogglePlanDay}
                onSelectChapter={handleSelectChapter}
                onGoToCurrentDay={() => setActiveSection('plan')}
              />
            ) : currentChapter ? (
              <ReadingView
                key={`${currentBookId}-${currentChapter.number}`}
                chapter={currentChapter}
                bookId={currentBookId}
                bookName={currentBook?.name}
                progress={progress}
                bookmarks={bookmarks}
                onToggleBookmark={handleToggleBookmark}
                onComplete={handleCompleteChapter}
                onQuizAnswer={handleQuizAnswer}
              />
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <p className="text-slate-400">Selecione um capítulo para começar</p>
              </div>
            )}
          </Suspense>
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
