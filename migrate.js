import { createClient } from '@libsql/client';

const db = createClient({
  url: 'file:econometria.db',
});

async function migrate() {
  console.log('Migrating database...');
  try {
    await db.execute(`
      CREATE TABLE IF NOT EXISTS concepts (
        slug TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        content_md TEXT NOT NULL
      );
    `);
    console.log('Table concepts created/verified.');

    try {
      await db.execute('ALTER TABLE questions ADD COLUMN concept_slug TEXT;');
      console.log('Column concept_slug added to questions.');
    } catch(e) {
      if (e.message.includes('duplicate column name')) {
        console.log('Column concept_slug already exists.');
      } else {
        console.log('Note on ALTER TABLE:', e.message);
      }
    }

    // Insert some default concepts
    const concepts = [
      {
        slug: 'teste-adf',
        title: 'Teste de Dickey-Fuller Aumentado (ADF)',
        content_md: `## O que é o Teste ADF?
O Teste Dickey-Fuller Aumentado é utilizado para detectar a presença de raiz unitária em uma série temporal. Se uma série tem raiz unitária, ela é não-estacionária.

### Hipóteses:
- **H0 (Nula)**: A série possui raiz unitária (Não-Estacionária).
- **H1 (Alternativa)**: A série não possui raiz unitária (Estacionária).

> Se o p-valor for menor que 0.05, rejeitamos H0 e concluímos que a série é estacionária.`
      },
      {
        slug: 'extrapolacao',
        title: 'Extrapolação Simples',
        content_md: `## O que é Extrapolação?
Extrapolar significa projetar valores futuros baseados estritamente na tendência passada, sem usar variáveis explicativas causais externas. É útil para previsões rápidas de curtíssimo prazo.`
      }
    ];

    for (const c of concepts) {
      await db.execute({
        sql: 'INSERT OR IGNORE INTO concepts (slug, title, content_md) VALUES (?, ?, ?)',
        args: [c.slug, c.title, c.content_md]
      });
    }
    console.log('Default concepts inserted.');

  } catch(err) {
    console.error('Migration failed:', err);
  }
}

migrate();
