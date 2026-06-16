'use client';
import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, BookOpen, AlertTriangle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function ConceitoPage() {
  const params = useParams();
  const router = useRouter();
  const slug = params.slug;
  const [concept, setConcept] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!slug) return;
    fetch(`/api/conceito/${slug}`)
      .then(res => res.json())
      .then(data => {
        if (!data.error) setConcept(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [slug]);

  return (
    <main style={{ padding: '60px 20px', maxWidth: '800px', margin: '0 auto' }}>
      <button onClick={() => router.back()} className="mono" style={{ background: 'transparent', border: 'none', color: 'var(--text-highlight)', marginBottom: '30px', display: 'inline-flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem', cursor: 'pointer' }}>
        <ArrowLeft size={16} /> VOLTAR PARA A OPERAÇÃO
      </button>
      
      {loading ? (
        <div className="mono" style={{ color: 'var(--text-highlight)' }}>[ Descriptografando base de conhecimento... ]</div>
      ) : !concept ? (
        <div className="glass-panel mono" style={{ color: 'var(--error-color)' }}>
          ERR: Conceito "{slug}" não encontrado nos arquivos da base.
        </div>
      ) : (
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '10px' }}>
            <AlertTriangle size={32} color="var(--error-color)" />
            <h1 className="title" style={{ margin: 0, color: '#fff' }}>
              Revisão de Falha: {concept.title}
            </h1>
          </div>
          <p className="subtitle mono" style={{ borderLeft: '2px solid var(--error-color)', paddingLeft: '15px', marginBottom: '40px' }}>
            ID DO CONCEITO: {slug.toUpperCase()} - MODO DE APRENDIZAGEM ATIVADO.
          </p>

          <div className="glass-panel" style={{ lineHeight: '1.8' }}>
            <div className="mono" style={{ color: 'var(--text-highlight)', marginBottom: '20px', borderBottom: '1px solid var(--surface-border)', paddingBottom: '10px' }}>
              &gt; RELATÓRIO DO CONCEITO_
            </div>
            <div style={{ color: 'var(--text-primary)', fontSize: '1.05rem', fontFamily: 'Inter, sans-serif' }}>
              <ReactMarkdown>{concept.content_md}</ReactMarkdown>
            </div>
          </div>
          
          <div style={{ marginTop: '30px', textAlign: 'center' }}>
            <button onClick={() => router.back()} className="btn btn-primary" style={{ padding: '15px 30px' }}>
              COMPREENDIDO - RETOMAR TESTE
            </button>
          </div>
        </div>
      )}
    </main>
  );
}
