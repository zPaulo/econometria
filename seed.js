import { createClient } from '@libsql/client';
import fs from 'fs';
import path from 'path';

const db = createClient({
  url: 'libsql://econometria-zpaulo.aws-us-east-2.turso.io',
  authToken: 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlSmNuZW1pX0VmR1hzMWJ3QTJWU2pnIiwib3JnX2lkIjoxMDAwMTIwNzA2fQ.9zT-f4QG1kY28Q1auNa-BiU2gBd06ygPc7-qfNLPMLPgKDQBKnx6WBD0H_lOOoDmXJL7dvcHtvuyyZbM76J2Dw',
});

async function main() {
  console.log('Iniciando seed do banco de dados Turso...');

  // Criar tabelas
  await db.execute(`
    CREATE TABLE IF NOT EXISTS themes (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      description TEXT
    );
  `);

  await db.execute(`
    CREATE TABLE IF NOT EXISTS questions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      theme_id INTEGER NOT NULL,
      text TEXT NOT NULL,
      image_url TEXT,
      general_explanation TEXT,
      FOREIGN KEY (theme_id) REFERENCES themes (id)
    );
  `);

  await db.execute(`
    CREATE TABLE IF NOT EXISTS options (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      question_id INTEGER NOT NULL,
      text TEXT NOT NULL,
      is_correct BOOLEAN NOT NULL,
      specific_explanation TEXT,
      FOREIGN KEY (question_id) REFERENCES questions (id)
    );
  `);

  await db.execute(`
    CREATE TABLE IF NOT EXISTS glossary (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      term TEXT NOT NULL UNIQUE,
      definition TEXT NOT NULL
    );
  `);

  await db.execute(`
    CREATE TABLE IF NOT EXISTS question_terms (
      question_id INTEGER,
      term_id INTEGER,
      PRIMARY KEY (question_id, term_id),
      FOREIGN KEY (question_id) REFERENCES questions (id),
      FOREIGN KEY (term_id) REFERENCES glossary (id)
    );
  `);

  console.log('Tabelas criadas com sucesso!');

  // Inserir temas
  const themes = [
    { id: 1, name: 'Introdução e História', description: 'Cowles Commission e Concursos de Previsão.' },
    { id: 2, name: 'Modelos Determinísticos', description: 'Extrapolação Simples.' },
    { id: 3, name: 'Alisamento e Decomposição', description: 'Médias Móveis, Sazonalidade, X11, SEAT.' },
    { id: 4, name: 'Suavização Exponencial Linear (SEL)', description: 'Simples, Holt, Holt-Winters e erro estocástico.' },
    { id: 5, name: 'Processos Estocásticos Lineares', description: 'Séries Estacionárias e Teste de Raiz Unitária.' },
    { id: 6, name: 'Modelos Estocásticos Lineares (BJR)', description: 'AR, MA, ARMA, ARIMA, Identificação, Estimação e Diagnósticos.' },
    { id: 7, name: 'Cointegração e Causalidade', description: 'Cointegração e Causalidade.' }
  ];

  for (const theme of themes) {
    await db.execute({
      sql: 'INSERT OR IGNORE INTO themes (id, name, description) VALUES (?, ?, ?)',
      args: [theme.id, theme.name, theme.description]
    });
  }

  // Inserir Glossário Básico
  const terms = [
    { term: 'estacionária', definition: 'Uma série temporal é dita estacionária quando sua média, variância e autocovariância são constantes ao longo do tempo.' },
    { term: 'raiz unitária', definition: 'Um processo estocástico com raiz unitária é não-estacionário. O teste de Dickey-Fuller (ADF) é usado para verificar a existência.' },
    { term: 'sazonalidade', definition: 'Padrões de variação em uma série temporal que se repetem em intervalos regulares de tempo (ex: estações do ano, meses).' },
    { term: 'holt-winters', definition: 'Método de suavização exponencial que lida com séries que possuem nível, tendência e sazonalidade.' },
    { term: 'ARIMA', definition: 'Modelo Autorregressivo Integrado de Médias Móveis. Usado para prever valores futuros em séries não-estacionárias que precisam ser diferenciadas.' }
  ];

  for (const t of terms) {
    await db.execute({
      sql: 'INSERT OR IGNORE INTO glossary (term, definition) VALUES (?, ?)',
      args: [t.term, t.definition]
    });
  }

  console.log('Temas e Glossário inseridos.');

  try {
    const questionsFile = path.join(process.cwd(), 'questions.json');
    if (fs.existsSync(questionsFile)) {
      const qData = JSON.parse(fs.readFileSync(questionsFile, 'utf8'));
      console.log(`Encontradas ${qData.length} questões no arquivo questions.json`);
      for (const q of qData) {
        const qRes = await db.execute({
          sql: 'INSERT INTO questions (theme_id, text, image_url, general_explanation) VALUES (?, ?, ?, ?) RETURNING id',
          args: [q.theme_id, q.text, q.image_url || null, q.general_explanation]
        });
        const qId = qRes.rows[0].id;

        for (const opt of q.options) {
          await db.execute({
            sql: 'INSERT INTO options (question_id, text, is_correct, specific_explanation) VALUES (?, ?, ?, ?)',
            args: [qId, opt.text, opt.is_correct ? 1 : 0, opt.specific_explanation]
          });
        }
      }
      console.log('Questões do JSON inseridas com sucesso!');
    }
  } catch (e) {
    console.error('Erro ao inserir questions.json:', e);
  }

  console.log('Seed completo!');
}

main().catch(e => console.error(e));
