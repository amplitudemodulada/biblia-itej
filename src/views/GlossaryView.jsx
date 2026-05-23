import { useState, useMemo } from 'react'
import { BookOpen, ChevronDown, Search as SearchIcon, Sparkles, Tag, Volume2 } from 'lucide-react'
import { GLOSSARY_DATA, GLOSSARY_CATEGORIES, searchGlossary } from '../data/glossaryData'

export default function GlossaryView() {
  const [query, setQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('Todos')
  const [expandedItems, setExpandedItems] = useState({})

  const results = useMemo(() => {
    return searchGlossary(query, selectedCategory)
  }, [query, selectedCategory])

  const toggleItem = (term) => {
    setExpandedItems(prev => ({
      ...prev,
      [term]: !prev[term]
    }))
  }

  const expandAll = () => {
    const all = {}
    results.forEach(item => {
      all[item.term] = true
    })
    setExpandedItems(all)
  }

  const collapseAll = () => {
    setExpandedItems({})
  }

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in">
        
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-xl bg-gradient-to-br from-amber-400 to-amber-600 shrink-0">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-slate-800 dark:text-slate-100">
                Glossário Judaico
              </h1>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                Termos hebraicos e judaicos comuns na Bíblia, novelas e séries
              </p>
            </div>
          </div>
        </div>

        <div className="space-y-3 mb-6">
          <div className="flex flex-col sm:flex-row gap-3">
            <div className="flex-1 relative">
              <SearchIcon className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Buscar termo (ex: Shabat, Torá, Kosher)..."
                className="w-full pl-9 pr-4 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500/50 focus:border-amber-500/50 text-sm"
              />
            </div>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-3 py-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500/50 cursor-pointer"
            >
              {GLOSSARY_CATEGORIES.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          {results.length > 0 && (
            <div className="flex items-center justify-between px-1">
              <p className="text-xs text-slate-500 dark:text-slate-400">
                {results.length} termo{results.length !== 1 ? 's' : ''} encontrado{results.length !== 1 ? 's' : ''}
              </p>
              <div className="flex gap-2">
                <button
                  onClick={expandAll}
                  className="text-xs text-amber-600 dark:text-amber-400 hover:text-amber-700 dark:hover:text-amber-300 font-medium"
                >
                  Expandir todos
                </button>
                <span className="text-xs text-slate-300 dark:text-slate-600">|</span>
                <button
                  onClick={collapseAll}
                  className="text-xs text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 font-medium"
                >
                  Recolher todos
                </button>
              </div>
            </div>
          )}
        </div>

        {results.length === 0 ? (
          <div className="text-center py-16">
            <SearchIcon className="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-200 mb-2">
              Nenhum termo encontrado
            </h3>
            <p className="text-sm text-slate-500 dark:text-slate-400">
              Tente uma busca diferente ou selecione outra categoria.
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {results.map((item, index) => {
              const isExpanded = expandedItems[item.term]
              return (
                <div
                  key={item.term}
                  className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden transition-all"
                >
                  <button
                    onClick={() => toggleItem(item.term)}
                    className="w-full text-left px-4 py-3 flex items-center justify-between gap-3 hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors"
                  >
                    <div className="flex items-start gap-3 min-w-0">
                      <div className="p-1.5 rounded-lg bg-amber-50 dark:bg-amber-900/20 shrink-0 mt-0.5">
                        <BookOpen className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                      </div>
                      <div className="min-w-0">
                        <div className="flex items-center gap-2 mb-1 flex-wrap">
                          <span className="font-semibold text-slate-800 dark:text-slate-100">
                            {item.term}
                          </span>
                          <span className="px-2 py-0.5 rounded-md bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 text-[10px] font-medium">
                            {item.hebrew}
                          </span>
                          <span className="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-400 text-[10px] font-medium flex items-center gap-1">
                            <Volume2 className="w-3 h-3" />
                            {item.pronunciation}
                          </span>
                        </div>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="px-2 py-0.5 rounded-md bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 text-xs font-medium flex items-center gap-1">
                            <Tag className="w-3 h-3" />
                            {item.category}
                          </span>
                          {!isExpanded && (
                            <p className="text-xs text-slate-500 dark:text-slate-400 truncate max-w-md">
                              {item.meaning}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                    <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform shrink-0 ${isExpanded ? 'rotate-180' : ''}`} />
                  </button>

                  {isExpanded && (
                    <div className="px-4 pb-4 pt-1 border-t border-slate-100 dark:border-slate-700/50">
                      
                      <div className="mb-4">
                        <h4 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-2">
                          Significado
                        </h4>
                        <p className="text-sm text-slate-700 dark:text-slate-200 leading-relaxed">
                          {item.meaning}
                        </p>
                      </div>

                      <div className="mb-4">
                        <h4 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-2">
                          Exemplos
                        </h4>
                        <div className="space-y-2">
                          {item.examples.map((example, i) => (
                            <p key={i} className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed pl-3 border-l-2 border-amber-300 dark:border-amber-700">
                              {example}
                            </p>
                          ))}
                        </div>
                      </div>

                      {item.related && item.related.length > 0 && (
                        <div>
                          <h4 className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-2">
                            Termos Relacionados
                          </h4>
                          <div className="flex flex-wrap gap-1.5">
                            {item.related.map((rel, i) => (
                              <span
                                key={i}
                                className="px-2 py-1 rounded-md bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs cursor-pointer hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors"
                                onClick={() => setQuery(rel.split(' ')[0])}
                              >
                                {rel}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}

        <div className="mt-12 pt-6 border-t border-slate-200 dark:border-slate-700">
          <div className="bg-gradient-to-r from-amber-50 to-orange-50 dark:from-amber-900/10 dark:to-orange-900/10 rounded-xl p-5 border border-amber-200/50 dark:border-amber-800/30">
            <div className="flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
              <div>
                <h3 className="text-sm font-semibold text-slate-800 dark:text-slate-100 mb-1">
                  Dica: Use a busca para encontrar termos específicos
                </h3>
                <p className="text-xs text-slate-600 dark:text-slate-400">
                  Você pode buscar pelo termo em português (ex: "Sábado"), pelo hebraico (ex: "שַׁבָּת"), ou pela pronúncia (ex: "sha-BAT").
                </p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}
