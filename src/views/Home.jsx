import { useMemo } from 'react'
import { Book, Sparkles, BookOpen, BarChart3, Flame, Star, ChevronRight, Download } from 'lucide-react'
import { BIBLE_DATA } from '../data/bibleData'

export default function Home({ progress, bookmarks, onStartReading, onShowDashboard, onSelectChapter, onContinueReading }) {
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

         <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 mb-6">
           <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-4">Como funciona</h2>
           <div className="space-y-4">
             <div className="flex items-start gap-3">
               <div className="w-8 h-8 rounded-full bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center shrink-0 mt-0.5">
                 <BookOpen className="w-4 h-4 text-amber-600 dark:text-amber-400" />
               </div>
               <div>
                 <h3 className="text-sm font-medium text-slate-800 dark:text-slate-200 mb-0.5">1. Leitura passo a passo</h3>
                 <p className="text-sm text-slate-500 dark:text-slate-400">
                   O objetivo é ler toda a Bíblia (versão NTLH) um capítulo por vez. Cada capítulo tem reflexão, quiz e até leitura por áudio.
                 </p>
               </div>
             </div>

             <div className="flex items-start gap-3">
               <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center shrink-0 mt-0.5">
                 <Download className="w-4 h-4 text-blue-600 dark:text-blue-400" />
               </div>
               <div>
                 <h3 className="text-sm font-medium text-slate-800 dark:text-slate-200 mb-0.5">2. Use no navegador ou instale no celular</h3>
                 <p className="text-sm text-slate-500 dark:text-slate-400">
                   Funciona diretamente no navegador, mas também pode ser instalado como aplicativo. Se aparecer o botão <span className="font-medium">"Instalar"</span> no cabeçalho, clique para adicionar à tela inicial do celular.
                 </p>
               </div>
             </div>

             <div className="flex items-start gap-3">
               <div className="w-8 h-8 rounded-full bg-emerald-100 dark:bg-emerald-900/30 flex items-center justify-center shrink-0 mt-0.5">
                 <Star className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
               </div>
               <div>
                 <h3 className="text-sm font-medium text-slate-800 dark:text-slate-200 mb-0.5">3. Progresso salvo automaticamente</h3>
                 <p className="text-sm text-slate-500 dark:text-slate-400">
                   Não precisa criar conta. Tudo fica salvo no próprio navegador: progresso, marcadores, configurações de tamanho de fonte e plano de leitura.
                 </p>
               </div>
             </div>

             <div className="flex items-start gap-3">
               <div className="w-8 h-8 rounded-full bg-orange-100 dark:bg-orange-900/30 flex items-center justify-center shrink-0 mt-0.5">
                 <Flame className="w-4 h-4 text-orange-600 dark:text-orange-400" />
               </div>
               <div>
                 <h3 className="text-sm font-medium text-slate-800 dark:text-slate-200 mb-0.5">4. Dica: siga o plano de 1 ano</h3>
                 <p className="text-sm text-slate-500 dark:text-slate-400">
                   Use a aba <span className="font-medium">"Plano"</span> no cabeçalho para seguir um plano de leitura de 1 ano (1189 capítulos / ~4 capítulos por dia). É a melhor forma de manter a consistência!
                 </p>
               </div>
             </div>
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
          {onContinueReading && (
            <button
              onClick={onContinueReading}
              className="inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-semibold shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40 transition-all active:scale-[0.98]"
            >
              <BookOpen className="w-5 h-5" />
              Continuar Leitura
            </button>
          )}
          <button
            onClick={onShowDashboard}
            className="inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl border border-slate-200 dark:border-slate-600 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800 font-medium transition-all"
          >
            <BarChart3 className="w-5 h-5" />
            Ver Progresso
          </button>
        </div>

        {bookmarks && bookmarks.length > 0 && (
          <div className="mt-8">
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100 mb-3 flex items-center gap-2">
              <Star className="w-4 h-4 text-amber-500 fill-amber-500" />
              Capítulos Marcados
            </h2>
            <div className="flex flex-wrap gap-2">
              {bookmarks.map(key => {
                const parts = key.split('-')
                const bkId = parts.slice(0, -1).join('-')
                const chNum = parseInt(parts[parts.length - 1])
                const bk = BIBLE_DATA.find(b => b.id === bkId)
                if (!bk) return null
                return (
                  <button
                    key={key}
                    onClick={() => onSelectChapter(bkId, chNum - 1)}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-medium text-slate-600 dark:text-slate-400 hover:bg-amber-50 dark:hover:bg-amber-900/10 hover:text-amber-700 dark:hover:text-amber-400 transition-colors"
                  >
                    <BookOpen className="w-3 h-3" />
                    {bk.name} {chNum}
                  </button>
                )
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
