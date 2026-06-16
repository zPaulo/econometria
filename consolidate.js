import { createClient } from '@libsql/client';
import fs from 'fs';
import path from 'path';

const db = createClient({
  url: 'file:econometria.db',
});

async function consolidate() {
  console.log('Consolidating generated JSON batches...');
  let totalInserted = 0;

  try {
    for (let i = 1; i <= 10; i++) {
      const batchFile = path.join(process.cwd(), `batch_${i}.json`);
      if (fs.existsSync(batchFile)) {
        console.log(`Processing ${batchFile}...`);
        const data = JSON.parse(fs.readFileSync(batchFile, 'utf8'));
        
        for (const q of data) {
          // Check if question exists
          const exist = await db.execute({
            sql: 'SELECT id FROM questions WHERE text = ?',
            args: [q.text]
          });
          if (exist.rows.length === 0) {
            const qRes = await db.execute({
              sql: 'INSERT INTO questions (theme_id, text, image_url, general_explanation, concept_slug) VALUES (?, ?, ?, ?, ?) RETURNING id',
              args: [
                q.theme_id || 1, 
                q.text, 
                q.image_url || null, 
                q.general_explanation || '', 
                q.concept_slug || 'conceito-geral'
              ]
            });
            const qId = qRes.rows[0].id;
            
            for (const opt of q.options) {
              await db.execute({
                sql: 'INSERT INTO options (question_id, text, is_correct, specific_explanation) VALUES (?, ?, ?, ?)',
                args: [
                  qId, 
                  opt.text, 
                  opt.is_correct ? 1 : 0, 
                  opt.specific_explanation || ''
                ]
              });
            }

            // Insert concept if not exists
            if (q.concept_slug) {
              await db.execute({
                sql: 'INSERT OR IGNORE INTO concepts (slug, title, content_md) VALUES (?, ?, ?)',
                args: [q.concept_slug, `Conceito: ${q.concept_slug}`, q.general_explanation || 'Revisão necessária.']
              });
            }

            totalInserted++;
          }
        }
        console.log(`Batch ${i} processed successfully.`);
      } else {
        console.log(`Batch ${i} not found yet.`);
      }
    }
    console.log(`Consolidation complete! Total new questions inserted: ${totalInserted}`);
  } catch(err) {
    console.error('Consolidation failed:', err);
  }
}

consolidate();
