import { createClient } from '@libsql/client';

const db = createClient({
  url: 'file:econometria.db',
});

async function main() {
  console.log('Iniciando migração da Fase 3 (LMS)...');

  await db.execute(`
    CREATE TABLE IF NOT EXISTS user_progress (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      question_id INTEGER NOT NULL,
      is_correct BOOLEAN NOT NULL,
      answered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (question_id) REFERENCES questions (id)
    );
  `);

  console.log('Tabela user_progress criada com sucesso!');
}

main().catch(console.error);
