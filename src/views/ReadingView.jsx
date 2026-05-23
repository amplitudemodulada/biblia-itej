import { useState, useEffect, useCallback } from 'react'
import {
  BookOpen, Star, Share2, Play, Pause, SkipBack, SkipForward,
  X, Volume2, Sparkles, Target, CheckCircle, ChevronRight, RotateCcw
} from 'lucide-react'
import QuizSection from './QuizSection'

export default function ReadingView({ chapter, bookId, bookName, progress, bookmarks, version = 'NTLH', onToggleBookmark, onComplete, onQuizAnswer }) {
  const [showIrAlem, setShowIrAlem] = useState(false)
  const [irAlemTab, setIrAlemTab] = useState('reflection')
  const [audioPlaying, setAudioPlaying] = useState(false)
  const [audioPaused, setAudioPaused] = useState(false)
  const [audioVerseIdx, setAudioVerseIdx] = useState(null)
  const [audioRate, setAudioRate] = useState(1)
  const [fontSize, setFontSize] = useState(() => { try { return localStorage.getItem('pv-fontsize') || 'base' } catch { return 'base' } })

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
  const isBookmarked = bookmarks?.includes(key)

  const handleFontSize = (size) => {
    setFontSize(size)
    localStorage.setItem('pv-fontsize', size)
  }

  const handleShare = async () => {
    const text = `${bookName} ${chapter.number}: ${chapter.title}\n\n` +
      (chapter.verses || [chapter.text]).slice(0, 5).join(' ') + '...'
    if (navigator.share) {
      try { await navigator.share({ title: `${bookName} ${chapter.number}`, text }) } catch {}
    } else {
      try { await navigator.clipboard.writeText(text) } catch {}
    }
  }

  const fontSizeClasses = {
    sm: 'text-sm sm:text-base',
    base: 'text-base sm:text-lg',
    lg: 'text-lg sm:text-xl',
    xl: 'text-xl sm:text-2xl',
  }

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
            <span className="px-1.5 py-0.5 rounded bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300 text-[10px] font-semibold uppercase tracking-wide">{version}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-800 dark:text-slate-100 mb-6">{chapter.title}</h1>

          <div className="flex items-center gap-2 mb-4">
            <button
              onClick={() => onToggleBookmark(key)}
              className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${isBookmarked ? 'bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400' : 'bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'}`}
              title={isBookmarked ? 'Remover marcador' : 'Adicionar marcador'}
            >
              <Star className={`w-3.5 h-3.5 ${isBookmarked ? 'fill-amber-500 text-amber-500' : ''}`} />
              {isBookmarked ? 'Marcado' : 'Marcar'}
            </button>
            <button
              onClick={handleShare}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 hover:text-amber-600 dark:hover:text-amber-400 transition-colors"
              title="Compartilhar capítulo"
            >
              <Share2 className="w-3.5 h-3.5" />
              Compartilhar
            </button>
          </div>

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
            <div className="flex items-center gap-1.5">
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
            <div className="flex items-center gap-1">
              {['sm','base','lg','xl'].map(size => (
                <button
                  key={size}
                  onClick={() => handleFontSize(size)}
                  className={`px-1.5 py-0.5 rounded text-[11px] font-medium transition-all uppercase ${fontSize === size ? 'bg-amber-500 text-white' : 'text-slate-400 hover:text-slate-600 dark:hover:text-slate-300'}`}
                  title={`Fonte ${size === 'sm' ? 'pequena' : size === 'base' ? 'normal' : size === 'lg' ? 'grande' : 'extra grande'}`}
                >
                  {size === 'sm' ? 'A' : size === 'base' ? 'A\u0300' : size === 'lg' ? 'A\u0301' : 'A\u0302'}
                </button>
              ))}
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
                    className={`${fontSizeClasses[fontSize]} leading-relaxed font-serif cursor-pointer rounded-lg transition-all ${audioVerseIdx === i && audioPlaying ? 'bg-amber-50 dark:bg-amber-900/20 px-4 -mx-4 py-3 text-amber-800 dark:text-amber-200 shadow-sm' : audioVerseIdx === i && audioPaused ? 'bg-amber-50/50 dark:bg-amber-900/10 px-4 -mx-4 py-3 text-slate-700 dark:text-slate-300' : 'text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800/50 px-2 -mx-2'}`}
                  >
                    <sup className="text-amber-500 dark:text-amber-400 font-semibold text-xs sm:text-sm mr-1.5 select-none">{i + 1}</sup>
                    {v}
                  </p>
                ))}
              </div>
            ) : (
              chapter.text.split('\n\n').map((paragraph, i) => (
                <p key={i} className={`${fontSizeClasses[fontSize]} leading-relaxed text-slate-700 dark:text-slate-300 mb-4 font-serif`}>
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
