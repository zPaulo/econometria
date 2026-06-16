'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { Terminal, BrainCircuit, Activity, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function AnalyticsPage() {
  const [themes, setThemes] = useState([]);
  const [concepts, setConcepts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/progress')
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          // Format for Recharts
          const formattedThemes = data.themes.map(t => ({
            name: `Módulo ${t.theme_id}`,
            Acertos: t.correct_answers,
            Erros: t.total_answers - t.correct_answers,
            taxa: (t.correct_answers / t.total_answers) * 100
          }));
          
          const formattedConcepts = data.concepts.map(c => ({
            slug: c.concept_slug,
            total: c.total_answers,
            acertos: c.correct_answers,
            taxa: (c.correct_answers / c.total_answers) * 100
          })).sort((a,b) => a.taxa - b.taxa); // Sort by lowest accuracy (Weaknesses)

          setThemes(formattedThemes);
          setConcepts(formattedConcepts);
        }
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <Activity className="spin" size={48} color="var(--accent-color)" />
        <h2 className="mono" style={{ marginTop: '20px' }}>&gt; CARREGANDO DADOS_</h2>
      </div>
    );
  }

  const globalAccuracy = themes.length > 0 
    ? (themes.reduce((acc, t) => acc + t.Acertos, 0) / themes.reduce((acc, t) => acc + t.Acertos + t.Erros, 0) * 100).toFixed(1) 
    : 0;

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--surface-border)', paddingBottom: '20px', marginBottom: '40px' }}>
        <div>
          <h1 style={{ display: 'flex', alignItems: 'center', gap: '15px', color: 'var(--text-highlight)', margin: 0, fontSize: '2rem' }}>
            <Activity size={32} /> ANALYTICS &amp; PERFORMANCE
          </h1>
          <p className="mono" style={{ color: 'var(--text-secondary)', marginTop: '10px' }}>
            &gt; ACOMPANHAMENTO DE PROGRESSO | METRIFICADOR DE ACURÁCIA BJR
          </p>
        </div>
        <Link href="/" className="btn">
          &lt; VOLTAR AO TERMINAL
        </Link>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '30px', marginBottom: '40px' }}>
        
        {/* KPI Panel */}
        <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
          <h3 className="mono" style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>ACURÁCIA GLOBAL</h3>
          <div style={{ fontSize: '4rem', fontWeight: 'bold', color: globalAccuracy > 70 ? 'var(--success-color)' : 'var(--error-color)' }}>
            {globalAccuracy}%
          </div>
          <p style={{ color: 'var(--text-secondary)' }}>Média total de acertos</p>
        </div>

        {/* Radar Chart Panel */}
        <div className="glass-panel" style={{ height: '300px' }}>
          <h3 className="mono" style={{ marginBottom: '10px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>DESEMPENHO POR MÓDULO (RADAR)</h3>
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="70%" data={themes}>
              <PolarGrid stroke="var(--surface-border)" />
              <PolarAngleAxis dataKey="name" stroke="var(--text-secondary)" fontSize={12} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} stroke="var(--surface-border)" />
              <Radar name="Acurácia (%)" dataKey="taxa" stroke="var(--accent-color)" fill="var(--accent-color)" fillOpacity={0.4} />
              <Tooltip contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', borderColor: 'var(--surface-border)' }} />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Bar Chart Panel */}
        <div className="glass-panel" style={{ height: '300px' }}>
          <h3 className="mono" style={{ marginBottom: '10px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>ACERTOS x ERROS (ABSOLUTO)</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={themes}>
              <XAxis dataKey="name" stroke="var(--text-secondary)" fontSize={12} />
              <YAxis stroke="var(--text-secondary)" fontSize={12} />
              <Tooltip contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', borderColor: 'var(--surface-border)' }} />
              <Bar dataKey="Acertos" fill="var(--success-color)" />
              <Bar dataKey="Erros" fill="var(--error-color)" />
            </BarChart>
          </ResponsiveContainer>
        </div>

      </div>

      <h2 style={{ fontSize: '1.5rem', marginBottom: '20px', borderBottom: '1px solid var(--surface-border)', paddingBottom: '10px' }}>
        <BrainCircuit size={24} style={{ verticalAlign: 'middle', marginRight: '10px', color: 'var(--text-highlight)' }} />
        MAPA DE FRAQUEZAS CONCEITUAIS
      </h2>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '30px' }}>
        Identificamos os tópicos em que você tem as menores taxas de acerto. Clique em "Revisar" para focar nas suas vulnerabilidades.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '20px' }}>
        {concepts.map(c => (
          <div key={c.slug} className="glass-panel" style={{ borderLeft: c.taxa < 50 ? '4px solid var(--error-color)' : (c.taxa < 70 ? '4px solid #ffaa00' : '4px solid var(--success-color)') }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '15px' }}>
              <h4 className="mono" style={{ margin: 0, fontSize: '1.1rem', textTransform: 'uppercase' }}>{c.slug.replace(/-/g, ' ')}</h4>
              {c.taxa < 70 ? <AlertTriangle color={c.taxa < 50 ? 'var(--error-color)' : '#ffaa00'} size={20} /> : <CheckCircle2 color="var(--success-color)" size={20} />}
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
              <span>Taxa: <strong>{c.taxa.toFixed(1)}%</strong></span>
              <span>({c.acertos}/{c.total} corretas)</span>
            </div>

            <div style={{ background: 'rgba(255,255,255,0.1)', height: '6px', borderRadius: '3px', overflow: 'hidden', marginBottom: '20px' }}>
              <div style={{ width: `${c.taxa}%`, background: c.taxa < 50 ? 'var(--error-color)' : (c.taxa < 70 ? '#ffaa00' : 'var(--success-color)'), height: '100%' }}></div>
            </div>

            {c.taxa < 70 && (
              <Link href={`/conceito/${c.slug}`} className="btn" style={{ display: 'block', textAlign: 'center', borderColor: 'var(--text-highlight)', color: 'var(--text-highlight)' }}>
                [ REVISAR ESTE CONCEITO ]
              </Link>
            )}
          </div>
        ))}
        {concepts.length === 0 && (
           <div style={{ color: 'var(--text-secondary)', padding: '20px' }}>
              Sem dados suficientes. Comece a responder questões para mapear suas fraquezas.
           </div>
        )}
      </div>

    </div>
  );
}
