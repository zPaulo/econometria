import { NextResponse } from 'next/server';
import { db } from '../../../../lib/db';

export async function GET(request, context) {
  try {
    const params = await context.params;
    const theme_id = params.theme_id;

    let query = 'SELECT * FROM questions WHERE theme_id = ?';
    let args = [theme_id];
    let themeInfo = null;
    
    if (theme_id === 'all') {
      query = 'SELECT * FROM questions ORDER BY RANDOM() LIMIT 20';
      args = [];
      themeInfo = { id: 'all', name: 'Simulado Geral', description: 'Todas as disciplinas' };
    } else {
      const tRes = await db.execute({ sql: 'SELECT * FROM themes WHERE id = ?', args: [theme_id] });
      if (tRes.rows.length > 0) {
        themeInfo = tRes.rows[0];
      }
    }

    const qRes = await db.execute({ sql: query, args });
    const questions = qRes.rows;

    const result = [];
    for (let q of questions) {
      const optRes = await db.execute({
        sql: 'SELECT * FROM options WHERE question_id = ?',
        args: [q.id]
      });
      const options = optRes.rows.map(o => ({
        ...o,
        is_correct: o.is_correct === 1
      }));
      result.push({ ...q, options });
    }

    return NextResponse.json({ theme: themeInfo, questions: result });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Erro ao buscar questoes' }, { status: 500 });
  }
}
