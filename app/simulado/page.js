'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Clock, CheckCircle2, XCircle, ChevronRight, ChevronLeft, Flag } from 'lucide-react';

export default function SimuladoPage() {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({}); // { index: option_id }
  const [timeLeft, setTimeLeft] = useState(120 * 60); // 120 minutes
  const [isFinished, setIsFinished] = useState(false);

  useEffect(() => {
    fetch('/api/simulado?limit=50')
      .then(res => res.json())
      .then(data => {
        if(data.success) setQuestions(data.data);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (loading || isFinished) return;
    const timer = setInterval(() => setTimeLeft(t => t > 0 ? t - 1 : 0), 1000);
    return () => clearInterval(timer);
  }, [loading, isFinished]);

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <h2 className="mono" style={{ color: 'var(--text-highlight)' }}>&gt; GERANDO CADERNO DE PROVA...</h2>
      </div>
    );
  }

  if (questions.length === 0) {
    return <div style={{ padding: '40px', color: 'var(--error-color)' }}>[ ERRO ] Nenhuma questão encontrada.</div>;
  }

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  };

  const handleSelect = (optionId) => {
    if (!isFinished) {
      setAnswers(prev => ({ ...prev, [currentIndex]: optionId }));
    }
  };

  const handleFinish = () => {
    setIsFinished(true);
    // Post all answers to /api/progress silently to track analytics
    Object.keys(answers).forEach(idx => {
      const q = questions[idx];
      const optId = answers[idx];
      const selectedOpt = q.options.find(o => o.id === optId);
      if (selectedOpt) {
        fetch('/api/progress', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question_id: q.id, is_correct: selectedOpt.is_correct })
        }).catch(e => console.error(e));
      }
    });
  };

  if (isFinished) {
    let score = 0;
    questions.forEach((q, idx) => {
      const selectedOptId = answers[idx];
      const correctOpt = q.options.find(o => o.is_correct);
      if (correctOpt && selectedOptId === correctOpt.id) score++;
    });

    const grade = (score / questions.length) * 10;
    const passed = grade >= 5.0;

    return (
      <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '20px' }}>
        <div className="glass-panel" style={{ textAlign: 'center', marginBottom: '40px' }}>
          <h1 className="mono" style={{ color: passed ? 'var(--success-color)' : 'var(--error-color)' }}>
             [ RELATÓRIO DO SIMULADO: {passed ? 'APROVADO' : 'REPROVADO'} ]
          </h1>
          <div style={{ fontSize: '5rem', fontWeight: 'bold', margin: '20px 0', color: passed ? 'var(--success-color)' : 'var(--error-color)' }}>
            {grade.toFixed(1)} / 10
          </div>
          <p style={{ color: 'var(--text-secondary)' }}>Você acertou {score} de {questions.length} questões.</p>
          <div style={{ marginTop: '20px', display: 'flex', gap: '20px', justifyContent: 'center' }}>
             <Link href="/" className="btn">&lt; VOLTAR AO TERMINAL</Link>
             <Link href="/analytics" className="btn" style={{ borderColor: 'var(--text-highlight)', color: 'var(--text-highlight)' }}>ANALISAR FRAQUEZAS</Link>
          </div>
        </div>

        <h3>GABARITO E CORREÇÃO</h3>
        {questions.map((q, idx) => {
          const selectedOptId = answers[idx];
          const selectedOpt = q.options.find(o => o.id === selectedOptId);
          const isCorrect = selectedOpt?.is_correct;
          
          return (
            <div key={q.id} className="glass-panel" style={{ marginBottom: '20px', borderLeft: `4px solid ${isCorrect ? 'var(--success-color)' : 'var(--error-color)'}` }}>
              <div style={{ marginBottom: '10px' }}>
                <span className="mono" style={{ color: 'var(--text-secondary)', marginRight: '10px' }}>Q{idx + 1}</span>
                {q.text}
              </div>
              <div style={{ padding: '10px', background: 'rgba(0,0,0,0.3)', borderRadius: '4px' }}>
                <div style={{ color: isCorrect ? 'var(--success-color)' : 'var(--error-color)' }}>
                  <strong>Sua Resposta:</strong> {selectedOpt ? selectedOpt.text : 'Deixou em branco'}
                </div>
                {!isCorrect && (
                  <div style={{ color: 'var(--success-color)', marginTop: '5px' }}>
                    <strong>Correta:</strong> {q.options.find(o => o.is_correct)?.text}
                  </div>
                )}
                <div style={{ marginTop: '10px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  <em>Explicação:</em> {q.general_explanation}
                </div>
                {!isCorrect && q.concept_slug && (
                  <div style={{ marginTop: '10px' }}>
                     <Link href={`/conceito/${q.concept_slug}`} className="btn" style={{ fontSize: '0.8rem', padding: '5px 10px', borderColor: 'var(--error-color)', color: 'var(--error-color)' }}>
                       REVISAR CONCEITO: {q.concept_slug.toUpperCase()}
                     </Link>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    );
  }

  const q = questions[currentIndex];
  const answeredCount = Object.keys(answers).length;

  return (
    <div style={{ maxWidth: '1000px', margin: '0 auto', padding: '20px' }}>
      {/* Header Panel */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', padding: '15px', background: 'rgba(0,0,0,0.5)', border: '1px solid var(--surface-border)' }}>
        <div style={{ display: 'flex', gap: '20px', alignItems: 'center' }}>
          <div className="mono" style={{ color: 'var(--text-secondary)' }}>
             [ QUESTÃO {currentIndex + 1} / {questions.length} ]
          </div>
          <div className="mono" style={{ color: 'var(--text-highlight)' }}>
             &gt; RESPONDIDAS: {answeredCount}
          </div>
        </div>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center', color: timeLeft < 300 ? 'var(--error-color)' : 'var(--success-color)' }}>
          <Clock size={20} />
          <span className="mono" style={{ fontSize: '1.2rem' }}>{formatTime(timeLeft)}</span>
        </div>
      </div>

      {/* Progress Bar */}
      <div style={{ width: '100%', height: '4px', background: 'rgba(255,255,255,0.1)', marginBottom: '40px' }}>
         <div style={{ width: `${(answeredCount / questions.length) * 100}%`, height: '100%', background: 'var(--text-highlight)', transition: 'width 0.3s ease' }} />
      </div>

      {/* Question Card (Exam Mode - No instant feedback) */}
      <div className="glass-panel" style={{ minHeight: '400px', marginBottom: '30px' }}>
        <h3 style={{ fontSize: '1.2rem', marginBottom: '30px', lineHeight: '1.6', fontWeight: '400' }}>
          {q.text}
        </h3>
        
        {q.image_url && (
          <div style={{ marginBottom: '20px', textAlign: 'center' }}>
            <img src={q.image_url} alt="Reference" style={{ maxWidth: '100%', border: '1px solid var(--surface-border)' }} />
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          {q.options.map(opt => {
            const isSelected = answers[currentIndex] === opt.id;
            return (
              <button
                key={opt.id}
                onClick={() => handleSelect(opt.id)}
                style={{
                  background: isSelected ? 'rgba(0, 240, 255, 0.1)' : 'rgba(0,0,0,0.4)',
                  border: isSelected ? '1px solid var(--text-highlight)' : '1px solid var(--surface-border)',
                  padding: '20px',
                  color: isSelected ? '#fff' : 'var(--text-primary)',
                  textAlign: 'left',
                  fontSize: '1rem',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '15px'
                }}
              >
                <div style={{ 
                  width: '20px', 
                  height: '20px', 
                  borderRadius: '50%', 
                  border: isSelected ? '5px solid var(--text-highlight)' : '2px solid var(--surface-border)',
                  transition: 'all 0.2s ease'
                }} />
                {opt.text}
              </button>
            );
          })}
        </div>
      </div>

      {/* Navigation */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <button 
          className="btn" 
          onClick={() => setCurrentIndex(c => Math.max(0, c - 1))}
          disabled={currentIndex === 0}
          style={{ opacity: currentIndex === 0 ? 0.3 : 1 }}
        >
          <ChevronLeft size={20} style={{ verticalAlign: 'middle', marginRight: '5px' }} /> ANTERIOR
        </button>

        {currentIndex === questions.length - 1 ? (
          <button 
            className="btn" 
            onClick={handleFinish}
            style={{ borderColor: 'var(--success-color)', color: 'var(--success-color)', background: 'rgba(0,255,102,0.1)' }}
          >
            <Flag size={20} style={{ verticalAlign: 'middle', marginRight: '5px' }} /> ENCERRAR PROVA
          </button>
        ) : (
          <button 
            className="btn" 
            onClick={() => setCurrentIndex(c => Math.min(questions.length - 1, c + 1))}
          >
            PRÓXIMA <ChevronRight size={20} style={{ verticalAlign: 'middle', marginLeft: '5px' }} />
          </button>
        )}
      </div>

      {/* Grid Jump */}
      <div style={{ marginTop: '40px', padding: '20px', background: 'rgba(0,0,0,0.5)', border: '1px solid var(--surface-border)', display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(40px, 1fr))', gap: '10px' }}>
        {questions.map((_, idx) => (
          <button
            key={idx}
            onClick={() => setCurrentIndex(idx)}
            style={{
              padding: '10px',
              background: currentIndex === idx ? 'var(--text-highlight)' : (answers[idx] ? 'rgba(0,240,255,0.2)' : 'transparent'),
              color: currentIndex === idx ? '#000' : (answers[idx] ? '#fff' : 'var(--text-secondary)'),
              border: `1px solid ${answers[idx] ? 'var(--text-highlight)' : 'var(--surface-border)'}`,
              cursor: 'pointer',
              fontWeight: 'bold',
              fontFamily: 'monospace'
            }}
          >
            {idx + 1}
          </button>
        ))}
      </div>
    </div>
  );
}
