'use client';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { Activity, TrendingUp, BarChart2 } from 'lucide-react';

export default function Home() {
  const [themes, setThemes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/themes')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) setThemes(data);
        else setThemes([]);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <main style={{ padding: '60px 20px', maxWidth: '1200px', margin: '0 auto' }}>
      <header style={{ textAlign: 'center', marginBottom: '80px' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '15px', marginBottom: '20px' }}>
          <TrendingUp size={40} color="var(--success-color)" />
          <h1 className="title" style={{ margin: 0 }}>Terminal Econometria</h1>
        </div>
        <p className="subtitle" style={{ maxWidth: '600px', margin: '0 auto 40px auto' }}>
          Análise de Séries Temporais, Modelagem BJR e Cointegração. 
          Sistema de testes e simulados integrado para alta performance de estudos.
        </p>
        <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', flexWrap: 'wrap' }}>
          <Link href="/simulado" className="btn btn-primary" style={{ padding: '16px 32px', fontSize: '1rem' }}>
            <Activity size={20} style={{ marginRight: '10px', verticalAlign: 'middle' }} />
            Iniciar Simulado Geral
          </Link>
          <Link href="/analytics" className="btn" style={{ padding: '16px 32px', fontSize: '1rem', borderColor: 'var(--text-highlight)', color: 'var(--text-highlight)' }}>
            <BarChart2 size={20} style={{ marginRight: '10px', verticalAlign: 'middle' }} />
            Painel de Analytics
          </Link>
        </div>
      </header>

      <section>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '30px' }}>
          <BarChart2 color="var(--text-highlight)" />
          <h2 className="mono" style={{ fontSize: '1.5rem', color: '#fff', textTransform: 'uppercase', letterSpacing: '1px' }}>
            Módulos do Curso
          </h2>
        </div>
        
        {loading ? (
          <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
            <div className="mono" style={{ color: 'var(--text-highlight)' }}>Aguardando conexão com o servidor...</div>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '24px' }}>
            {themes.map(theme => (
              <Link href={`/tema/${theme.id}`} key={theme.id}>
                <div className="glass-panel" style={{ 
                  cursor: 'pointer', height: '100%', display: 'flex', flexDirection: 'column',
                  transition: 'all 0.2s ease', borderLeft: '3px solid var(--text-highlight)'
                }}
                onMouseOver={e => {
                  e.currentTarget.style.transform = 'translateY(-5px)';
                  e.currentTarget.style.boxShadow = '0 10px 40px rgba(0, 240, 255, 0.15)';
                  e.currentTarget.style.borderColor = 'var(--success-color)';
                }}
                onMouseOut={e => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.5)';
                  e.currentTarget.style.borderColor = 'var(--text-highlight)';
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '15px' }}>
                    <span className="mono" style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                      MOD-{theme.id.toString().padStart(2, '0')}
                    </span>
                    <span className="mono" style={{ color: 'var(--success-color)', fontSize: '0.85rem' }}>
                      +1.42% ▲
                    </span>
                  </div>
                  <h3 className="mono" style={{ fontSize: '1.2rem', marginBottom: '15px', color: '#fff', lineHeight: '1.4' }}>
                    {theme.name}
                  </h3>
                  <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: '1.6', flex: 1 }}>
                    {theme.description}
                  </p>
                  <div style={{ marginTop: '25px', display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-highlight)', fontWeight: 'bold', fontSize: '0.9rem' }} className="mono">
                    EXECUTAR TESTE ➔
                  </div>
                </div>
              </Link>
            ))}
            {themes.length === 0 && (
              <div className="glass-panel mono" style={{ color: 'var(--error-color)' }}>
                ERR: Nenhum dado encontrado na base.
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}
