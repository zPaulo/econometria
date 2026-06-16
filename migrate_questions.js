import { createClient } from '@libsql/client';
import fs from 'fs';
import path from 'path';

const db = createClient({
  url: 'file:econometria.db',
});

async function migrate_questions() {
  console.log('Inserting extra questions...');
  try {
    const questionsFile = path.join(process.cwd(), 'extra_questions.json');
    if (fs.existsSync(questionsFile)) {
      const qData = JSON.parse(fs.readFileSync(questionsFile, 'utf8'));
      for (const q of qData) {
        const exist = await db.execute({
          sql: 'SELECT id FROM questions WHERE text = ?',
          args: [q.text]
        });
        if (exist.rows.length === 0) {
          const qRes = await db.execute({
            sql: 'INSERT INTO questions (theme_id, text, image_url, general_explanation, concept_slug) VALUES (?, ?, ?, ?, ?)',
            args: [q.theme_id, q.text, q.image_url || null, q.general_explanation, 'extrapolacao']
          });
          const qId = qRes.rows[0].id;

          for (const opt of q.options) {
            await db.execute({
              sql: 'INSERT INTO options (question_id, text, is_correct, specific_explanation) VALUES (?, ?, ?, ?)',
              args: [qId, opt.text, opt.is_correct ? 1 : 0, opt.specific_explanation]
            });
          }
        }
      }
      console.log('Extra questions inserted successfully!');
    }
  } catch(err) {
    console.error('Migration failed:', err);
  }
}

migrate_questions();
