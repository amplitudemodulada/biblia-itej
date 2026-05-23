import { useMemo } from 'react'
import { Trophy, Target, Flame } from 'lucide-react'
import { BIBLE_DATA } from '../data/bibleData'

export default function Dashboard({ progress }) {
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
