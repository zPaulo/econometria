'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, MonitorPlay } from 'lucide-react';
import QuestionCard from '../../../../components/QuestionCard';

export default function TemaTestePage() {
  const params = useParams();
  const id = params.id;
  const [data, setData] = useState(null);
  const [glossary, setGlossary] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    Promise.all([
      fetch(`/api/questions/${id}`).then(res => res.json()),
      fetch('/api/glossary').then(res => res.json())
    ]).then(([resData, gData]) => {
      if (resData && Array.isArray(resData.questions)) {
        setData(resData);
      } else {
        setData({ theme: null, questions: [] });
      }
      setGlossary(gData);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [id]);

  const questions = data?.questions || [];
  const theme = data?.theme;

  return (
    <main style={{ padding: '60px 20px', maxWidth: '800px', margin: '0 auto' }}>
      <Link href={`/tema/${id}`} className="mono" style={{ color: 'var(--text-highlight)', marginBottom: '30px', display: 'inline-flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem' }}>
        <ArrowLeft size={16} /> VOLTAR AO PAINEL DO MÓDULO
      </Link>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '10px' }}>
        <MonitorPlay size={32} color="var(--text-highlight)" />
        <h1 className="title" style={{ margin: 0 }}>
          {theme ? `Módulo ${theme.id}: Operações` : `Módulo ${id}: Operações`}
        </h1>
      </div>
      {theme && (
        <p className="subtitle mono" style={{ borderLeft: '2px solid var(--text-highlight)', paddingLeft: '15px', marginBottom: '40px' }}>
          {theme.description} - Testes de fixação
        </p>
      )}
      
      {loading ? (
        <div className="mono" style={{ color: 'var(--text-highlight)' }}>[ Sincronizando operações... ]</div>
      ) : questions.length === 0 ? (
        <div className="glass-panel mono" style={{ color: 'var(--error-color)' }}>
          ERR: Nenhuma operação (questão) cadastrada para este módulo no servidor.
        </div>
      ) : (
        <div>
          {questions.map((q, index) => (
            <div key={q.id} style={{ marginBottom: '40px' }}>
              <div className="mono" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '15px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span style={{ 
                    background: 'rgba(59, 130, 246, 0.2)', 
                    border: '1px solid var(--accent-color)', 
                    color: 'var(--text-highlight)', 
                    padding: '4px 12px', 
                    fontSize: '0.85rem' 
                  }}>
                    OPERAÇÃO #{index + 1} / {questions.length}
                  </span>
                </div>
                <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>ID: {q.id.toString().padStart(4, '0')}</span>
              </div>
              <QuestionCard question={q} glossary={glossary} />
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
