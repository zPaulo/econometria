import { createClient } from '@libsql/client';
import fs from 'fs';
import path from 'path';

let dbUrl = process.env.TURSO_DATABASE_URL || 'file:econometria.db';

// Vercel Serverless Function specific fix for local SQLite
if (process.env.VERCEL) {
  const tmpPath = '/tmp/econometria.db';
  if (!fs.existsSync(tmpPath)) {
    try {
      const srcPath = path.join(process.cwd(), 'econometria.db');
      fs.copyFileSync(srcPath, tmpPath);
      console.log('Copied database to /tmp for write access.');
    } catch (e) {
      console.error('Failed to copy database:', e);
    }
  }
  dbUrl = `file:${tmpPath}`;
}

export const db = createClient({
  url: dbUrl,
});
