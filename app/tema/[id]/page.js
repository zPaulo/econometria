'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, BookOpen, MonitorPlay, Activity } from 'lucide-react';

export default function TemaDashboardPage() {
  const params = useParams();
  const id = params.id;
  const [theme, setTheme] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    fetch(`/api/questions/${id}`)
      .then(res => res.json())
      .then(data => {
        if (data && data.theme) {
          setTheme(data.theme);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  return (
    <main style={{ padding: '60px 20px', maxWidth: '1000px', margin: '0 auto' }}>
      <Link href="/" className="mono" style={{ color: 'var(--text-highlight)', marginBottom: '30px', display: 'inline-flex', alignItems: 'center', gap: '8px', fontSize: '0.9rem' }}>
        <ArrowLeft size={16} /> VOLTAR AO TERMINAL
      </Link>
      
      <div style={{ marginBottom: '40px' }}>
        <h1 className="title" style={{ margin: 0 }}>
          {loading ? 'Carregando Módulo...' : (theme ? `Módulo ${theme.id}: ${theme.name}` : `Módulo ${id}`)}
        </h1>
        {theme && (
          <p className="subtitle mono" style={{ borderLeft: '2px solid var(--text-highlight)', paddingLeft: '15px', marginTop: '15px' }}>
            {theme.description}
          </p>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px' }}>
        
        {/* Cartão de Aulas */}
        <Link href={`/tema/${id}/aula`}>
          <div className="glass-panel" style={{ 
            cursor: 'pointer', height: '100%', display: 'flex', flexDirection: 'column',
            transition: 'all 0.2s ease', borderLeft: '3px solid var(--text-highlight)'
          }}
          onMouseOver={e => {
            e.currentTarget.style.transform = 'translateY(-5px)';
            e.currentTarget.style.boxShadow = '0 10px 40px rgba(0, 240, 255, 0.15)';
          }}
          onMouseOut={e => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.5)';
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
              <BookOpen size={40} color="var(--text-highlight)" />
              <h2 className="mono" style={{ color: '#fff', fontSize: '1.5rem', textTransform: 'uppercase' }}>Modo Aula</h2>
            </div>
            <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '20px', flex: 1 }}>
              Acesse o conteúdo teórico profundo, materiais em vídeo e documentação sobre este módulo.
            </p>
            <div className="btn" style={{ width: '100%' }}>INICIAR TREINAMENTO</div>
          </div>
        </Link>

        {/* Cartão de Testes */}
        <Link href={`/tema/${id}/teste`}>
          <div className="glass-panel" style={{ 
            cursor: 'pointer', height: '100%', display: 'flex', flexDirection: 'column',
            transition: 'all 0.2s ease', borderLeft: '3px solid var(--success-color)'
          }}
          onMouseOver={e => {
            e.currentTarget.style.transform = 'translateY(-5px)';
            e.currentTarget.style.boxShadow = '0 10px 40px rgba(0, 255, 102, 0.15)';
            e.currentTarget.style.borderColor = 'var(--success-color)';
          }}
          onMouseOut={e => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.5)';
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
              <Activity size={40} color="var(--success-color)" />
              <h2 className="mono" style={{ color: '#fff', fontSize: '1.5rem', textTransform: 'uppercase' }}>Modo Operação</h2>
            </div>
            <p style={{ color: 'var(--text-secondary)', lineHeight: '1.6', marginBottom: '20px', flex: 1 }}>
              Teste seus conhecimentos com questões elaboradas por IA focadas na didática da disciplina.
            </p>
            <div className="btn btn-primary" style={{ width: '100%' }}>INICIAR OPERAÇÃO</div>
          </div>
        </Link>

      </div>
    </main>
  );
}
