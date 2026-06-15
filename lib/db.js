import { createClient } from '@libsql/client';

export const db = createClient({
  url: process.env.TURSO_DATABASE_URL || 'libsql://econometria-zpaulo.aws-us-east-2.turso.io',
  authToken: process.env.TURSO_AUTH_TOKEN || 'eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlSmNuZW1pX0VmR1hzMWJ3QTJWU2pnIiwib3JnX2lkIjoxMDAwMTIwNzA2fQ.9zT-f4QG1kY28Q1auNa-BiU2gBd06ygPc7-qfNLPMLPgKDQBKnx6WBD0H_lOOoDmXJL7dvcHtvuyyZbM76J2Dw',
});
