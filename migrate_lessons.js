import { createClient } from '@libsql/client';
import fs from 'fs';
import path from 'path';

const db = createClient({
  url: 'file:econometria.db',
});

async function migrate_lessons() {
  console.log('Inserting extra lessons...');
  try {
    const lessonsFile = path.join(process.cwd(), 'extra_lessons.json');
    if (fs.existsSync(lessonsFile)) {
      const lessons = JSON.parse(fs.readFileSync(lessonsFile, 'utf8'));
      for (const lesson of lessons) {
        await db.execute({
          sql: 'INSERT OR REPLACE INTO lessons (theme_id, video_url, content_md) VALUES (?, ?, ?)',
          args: [lesson.theme_id, lesson.video_url, lesson.content_md]
        });
      }
      console.log('Extra lessons inserted successfully!');
    }
  } catch(err) {
    console.error('Migration failed:', err);
  }
}

migrate_lessons();
