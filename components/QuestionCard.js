'use client';
import { useState } from 'react';
import { CheckCircle2, XCircle, MousePointer2 } from 'lucide-react';
import GlossaryTooltip from './GlossaryTooltip';

export default function QuestionCard({ question, glossary }) {
  const [selectedOption, setSelectedOption] = useState(null);
  const [isConfirmed, setIsConfirmed] = useState(false);
  const [confirmedOption, setConfirmedOption] = useState(null);
  const [viewingExplanationFor, setViewingExplanationFor] = useState(null);

  const handleSelect = (opt) => {
    if (!isConfirmed) {
      setSelectedOption(opt);
    } else {
      // After confirmation, clicking an option just views its explanation
      setViewingExplanationFor(opt);
    }
  };

  const handleConfirm = () => {
    if (selectedOption && !isConfirmed) {
      setIsConfirmed(true);
      setConfirmedOption(selectedOption);
      setViewingExplanationFor(selectedOption);
      
      // Save progress
      fetch('/api/progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          question_id: question.id, 
          is_correct: selectedOption.is_correct 
        })
      }).catch(err => console.error('Failed to log progress:', err));
    }
  };

  return (
    <div className="glass-panel" style={{ marginBottom: '24px' }}>
      {isConfirmed && confirmedOption && (
        <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: '2px', background: confirmedOption.is_correct ? 'var(--success-color)' : 'var(--error-color)', boxShadow: `0 0 10px ${confirmedOption.is_correct ? 'var(--success-color)' : 'var(--error-color)'}` }} />
      )}
      
      <h3 style={{ fontSize: '1.2rem', marginBottom: '20px', lineHeight: '1.6', fontWeight: '400', fontFamily: 'var(--font-inter)' }}>
        <GlossaryTooltip text={question.text} glossary={glossary} />
      </h3>

      {question.image_url && (
        <div style={{ marginBottom: '20px', textAlign: 'center', border: '1px solid var(--surface-border)', padding: '10px', background: 'rgba(0,0,0,0.5)' }}>
          <img src={question.image_url} alt="Referência da questão" style={{ maxWidth: '100%' }} />
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '20px' }}>
        {question.options.map(opt => {
          let bg = 'rgba(0, 0, 0, 0.4)';
          let border = '1px solid var(--surface-border)';
          let color = 'var(--text-primary)';
          let opacity = 1;
          let boxShadow = 'none';
          
          if (!isConfirmed) {
            // Before confirmation
            if (selectedOption?.id === opt.id) {
              bg = 'rgba(0, 240, 255, 0.1)';
              border = '1px solid var(--text-highlight)';
              color = '#fff';
            }
          } else {
            // After confirmation
            if (opt.is_correct) {
              bg = 'rgba(0, 255, 102, 0.1)';
              border = '1px solid var(--success-color)';
              color = '#fff';
            } else if (confirmedOption?.id === opt.id) {
              bg = 'rgba(255, 0, 85, 0.1)';
              border = '1px solid var(--error-color)';
              color = '#fff';
            } else {
              color = 'var(--text-secondary)';
              opacity = 0.6;
            }
            
            // Highlight the one we are currently viewing
            if (viewingExplanationFor?.id === opt.id) {
               opacity = 1;
               boxShadow = 'inset 0 0 15px rgba(255,255,255,0.1)';
            }
          }

          if (isConfirmed && viewingExplanationFor?.id === opt.id) {
            boxShadow = 'inset 0 0 10px rgba(0,240,255,0.2)';
            border = `1px solid var(--text-highlight)`;
          }

          return (
            <button
              key={opt.id}
              onClick={() => handleSelect(opt)}
              style={{
                background: bg,
                border: border,
                padding: '16px 20px',
                color: color,
                opacity: opacity,
                textAlign: 'left',
                fontSize: '1rem',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                fontFamily: 'Inter, sans-serif',
                boxShadow: boxShadow
              }}
              onMouseOver={e => {
                if (!isConfirmed) {
                  e.currentTarget.style.borderColor = 'var(--text-highlight)';
                  e.currentTarget.style.boxShadow = '0 0 10px rgba(0,240,255,0.2)';
                } else {
                  e.currentTarget.style.opacity = '1';
                }
              }}
              onMouseOut={e => {
                if (!isConfirmed) {
                  e.currentTarget.style.borderColor = selectedOption?.id === opt.id ? 'var(--text-highlight)' : 'var(--surface-border)';
                  e.currentTarget.style.boxShadow = 'none';
                } else {
                  if (viewingExplanationFor?.id !== opt.id) {
                     e.currentTarget.style.opacity = opacity.toString();
                  }
                }
              }}
            >
              <span style={{ flex: 1, paddingRight: '15px', lineHeight: '1.5' }}>
                <GlossaryTooltip text={opt.text} glossary={glossary} />
              </span>
              {isConfirmed && opt.is_correct && <CheckCircle2 color="var(--success-color)" size={20} />}
              {isConfirmed && !opt.is_correct && confirmedOption?.id === opt.id && <XCircle color="var(--error-color)" size={20} />}
              {isConfirmed && viewingExplanationFor?.id === opt.id && viewingExplanationFor?.id !== confirmedOption?.id && !opt.is_correct && <MousePointer2 color="var(--text-highlight)" size={18} />}
            </button>
          );
        })}
      </div>

      {!isConfirmed && (
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '10px' }}>
          <button 
            className="btn btn-primary" 
            onClick={handleConfirm}
            disabled={!selectedOption}
            style={{ 
              opacity: selectedOption ? 1 : 0.5, 
              cursor: selectedOption ? 'pointer' : 'not-allowed',
              pointerEvents: selectedOption ? 'auto' : 'none'
            }}
          >
            CONFIRMAR OPERAÇÃO
          </button>
        </div>
      )}

      {isConfirmed && viewingExplanationFor && (
        <div style={{ padding: '20px', background: 'rgba(0,0,0,0.5)', borderLeft: `2px solid ${viewingExplanationFor.is_correct ? 'var(--success-color)' : 'var(--error-color)'}`, animation: 'fadeIn 0.3s ease forwards' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
             <h4 className="mono" style={{ color: viewingExplanationFor.is_correct ? 'var(--success-color)' : 'var(--error-color)', fontSize: '1.1rem', textTransform: 'uppercase', margin: 0 }}>
               STATUS DA ALTERNATIVA: {viewingExplanationFor.is_correct ? 'CORRETA' : 'INCORRETA'}
             </h4>
             {viewingExplanationFor.id === confirmedOption.id && (
                <span className="mono" style={{ fontSize: '0.8rem', background: confirmedOption.is_correct ? 'var(--success-color)' : 'var(--error-color)', color: '#000', padding: '2px 8px', borderRadius: '4px', fontWeight: 'bold' }}>
                  SUA ESCOLHA
                </span>
             )}
          </div>
          
          <p style={{ marginBottom: '15px', lineHeight: '1.6' }}>
            <span className="mono" style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>&gt; LOG DE ANALISE_</span> <br/>
            <GlossaryTooltip text={viewingExplanationFor.specific_explanation} glossary={glossary} />
          </p>
          <hr style={{ border: 'none', borderTop: '1px dashed var(--surface-border)', margin: '15px 0' }} />
          <p style={{ lineHeight: '1.6', color: '#fff' }}>
            <span className="mono" style={{ color: 'var(--text-highlight)', fontSize: '0.85rem' }}>&gt; CONCEITO GLOBAL DA QUESTÃO_</span> <br/>
            <GlossaryTooltip text={question.general_explanation} glossary={glossary} />
          </p>

          {!viewingExplanationFor.is_correct && viewingExplanationFor.id === confirmedOption?.id && question.concept_slug && (
            <div style={{ marginTop: '20px', textAlign: 'center' }}>
               <a href={`/conceito/${question.concept_slug}`} className="btn" style={{ borderColor: 'var(--error-color)', color: 'var(--error-color)' }}>
                 [ REVISAR CONCEITO: {question.concept_slug.toUpperCase()} ]
               </a>
            </div>
          )}
        </div>
      )}
      
      {isConfirmed && (
        <div className="mono" style={{ textAlign: 'center', marginTop: '15px', color: 'var(--text-secondary)', fontSize: '0.8rem', animation: 'fadeIn 1s ease forwards' }}>
          &gt; Clique em outras alternativas para inspecionar seus respectivos logs de erro.
        </div>
      )}
    </div>
  );
}
