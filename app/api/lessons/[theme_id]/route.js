import { NextResponse } from 'next/server';
import { db } from '../../../../lib/db';

export async function GET(request, context) {
  try {
    const params = await context.params;
    const theme_id = params.theme_id;

    // Fetch theme
    const tRes = await db.execute({ sql: 'SELECT * FROM themes WHERE id = ?', args: [theme_id] });
    if (tRes.rows.length === 0) {
      return NextResponse.json({ error: 'Theme not found' }, { status: 404 });
    }
    const theme = tRes.rows[0];

    // Fetch lesson
    const lRes = await db.execute({ sql: 'SELECT * FROM lessons WHERE theme_id = ?', args: [theme_id] });
    const lesson = lRes.rows.length > 0 ? lRes.rows[0] : null;

    return NextResponse.json({ theme, lesson });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Erro ao buscar aula' }, { status: 500 });
  }
}
