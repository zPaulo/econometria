'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, BookOpen, Activity } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

export default function TemaAulaPage() {
  const params = useParams();
  const id = params.id;
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    fetch(`/api/lessons/${id}`)
      .then(res => res.json())
      .then(resData => {
        if (resData && !resData.error) {
          setData(resData);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  const theme = data?.theme;
  const lesson = data?.lesson;

  return (
    <main style={{ padding: '60px 20px', maxWidth: '800px', margin: '0 auto' }}>
      <Link href={`/tema/${id}`} className="mono" style={{ color: 'var(--text-highlight)', marginBottom: '30px', display: 'inline-flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem' }}>
        <ArrowLeft size={16} /> VOLTAR AO PAINEL DO MÓDULO
      </Link>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '10px' }}>
        <BookOpen size={32} color="var(--text-highlight)" />
        <h1 className="title" style={{ margin: 0 }}>
          {theme ? `Aula: ${theme.name}` : `Carregando Aula...`}
        </h1>
      </div>
      {theme && (
        <p className="subtitle mono" style={{ borderLeft: '2px solid var(--text-highlight)', paddingLeft: '15px', marginBottom: '40px' }}>
          Módulo {theme.id} - Material Teórico
        </p>
      )}

      {loading ? (
        <div className="mono" style={{ color: 'var(--text-highlight)' }}>[ Sincronizando vídeo e textos... ]</div>
      ) : !lesson ? (
        <div className="glass-panel mono" style={{ color: 'var(--error-color)' }}>
          ERR: Conteúdo instrucional ainda não cadastrado para este módulo.
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '40px' }}>
          
          {lesson.video_url && (
            <div className="glass-panel" style={{ padding: '10px', borderColor: 'var(--text-highlight)' }}>
              <div style={{ position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden' }}>
                <iframe 
                  style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', border: 0 }}
                  src={lesson.video_url} 
                  title="YouTube video player" 
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                  allowFullScreen
                ></iframe>
              </div>
            </div>
          )}

          <div className="glass-panel" style={{ lineHeight: '1.8' }}>
            <div className="mono" style={{ color: 'var(--text-highlight)', marginBottom: '20px', borderBottom: '1px solid var(--surface-border)', paddingBottom: '10px' }}>
              &gt; TRANSCRIÇÃO / MATERIAL TEÓRICO_
            </div>
            <div style={{ color: 'var(--text-primary)', fontSize: '1.05rem', fontFamily: 'Inter, sans-serif' }}>
              <ReactMarkdown>{lesson.content_md}</ReactMarkdown>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '20px' }}>
             <Link href={`/tema/${id}/teste`} className="btn btn-primary" style={{ padding: '15px 30px' }}>
               <Activity size={20} /> INICIAR OPERAÇÃO DE TESTE
             </Link>
          </div>

        </div>
      )}
    </main>
  );
}
