import { createClient } from '@libsql/client';

export const db = createClient({
  // Fallback to local SQLite file since Turso token was unauthorized
  url: process.env.TURSO_DATABASE_URL || 'file:econometria.db',
});
