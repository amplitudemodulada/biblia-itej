import { useState, useMemo } from 'react'
import { Search as SearchIcon, BookOpen, ChevronDown } from 'lucide-react'
import { BIBLE_DATA } from '../data/bibleData'

export default function SearchView({ onSelectChapter }) {
  const [query, setQuery] = useState('')
  const [expandedResults, setExpandedResults] = useState({})

  const results = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q || q.length < 2) return []
    const out = []
    for (const book of BIBLE_DATA) {
      const matches = []
      for (const ch of book.chapters) {
        const fields = [ch.title, ch.text, ch.reflection, ...(ch.verses || [])]
        for (const field of fields) {
          const idx = field.toLowerCase().indexOf(q)
          if (idx !== -1) {
            const start = Math.max(0, idx - 60)
            const end = Math.min(field.length, idx + q.length + 60)
            let snippet = (start > 0 ? '...' : '') + field.slice(start, end) + (end < field.length ? '...' : '')
            matches.push({ chapter: ch.number, title: ch.title, snippet, bookId: book.id, bookName: book.name })
            break
          }
        }
      }
      if (matches.length > 0) out.push({ bookId: book.id, bookName: book.name, matches })
    }
    return out
  }, [query])

  const toggleBook = (bookId) => {
    setExpandedResults(prev => ({ ...prev, [bookId]: !prev[bookId] }))
  }

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
        <div className="relative mb-6">
          <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Pesquisar na Bíblia (mín. 2 caracteres)..."
            className="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500/50 text-sm"
            autoFocus
          />
        </div>

        {results.length === 0 && query.trim().length >= 2 && (
          <p className="text-center text-slate-400 py-12">Nenhum resultado encontrado para "{query}"</p>
        )}

        {query.trim().length < 2 && (
          <p className="text-center text-slate-400 py-12">Digite pelo menos 2 caracteres para pesquisar no texto de todos os capítulos.</p>
        )}

        <div className="space-y-3">
          {results.map(book => {
            const isExpanded = expandedResults[book.bookId] !== false
            return (
              <div key={book.bookId} className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden">
                <button
                  onClick={() => toggleBook(book.bookId)}
                  className="w-full flex items-center justify-between px-4 py-3 hover:bg-slate-50 dark:hover:bg-slate-750 transition-colors"
                >
                  <div className="flex items-center gap-2">
                    <BookOpen className="w-4 h-4 text-amber-500 shrink-0" />
                    <span className="font-semibold text-sm text-slate-800 dark:text-slate-200">{book.bookName}</span>
                    <span className="text-xs text-slate-400">({book.matches.length} {book.matches.length === 1 ? 'capítulo' : 'capítulos'})</span>
                  </div>
                  <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
                </button>
                {isExpanded && (
                  <div className="border-t border-slate-100 dark:border-slate-700">
                    {book.matches.map((m, i) => (
                      <button
                        key={`${m.bookId}-${m.chapter}-${i}`}
                        onClick={() => { onSelectChapter(m.bookId, m.chapter - 1) }}
                        className="w-full text-left px-4 py-3 hover:bg-amber-50 dark:hover:bg-amber-900/10 transition-colors border-b border-slate-50 dark:border-slate-700/50 last:border-b-0"
                      >
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs font-bold text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 px-2 py-0.5 rounded">{m.chapter}</span>
                          <span className="text-sm font-medium text-slate-700 dark:text-slate-300">{m.title}</span>
                        </div>
                        <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed line-clamp-2">{m.snippet}</p>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
