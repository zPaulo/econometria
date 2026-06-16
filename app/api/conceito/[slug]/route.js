import { NextResponse } from 'next/server';
import { db } from '../../../../lib/db';

export async function GET(request, context) {
  try {
    const params = await context.params;
    const slug = params.slug;

    const res = await db.execute({ sql: 'SELECT * FROM concepts WHERE slug = ?', args: [slug] });
    if (res.rows.length === 0) {
      return NextResponse.json({ error: 'Concept not found' }, { status: 404 });
    }
    
    return NextResponse.json(res.rows[0]);
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Erro ao buscar conceito' }, { status: 500 });
  }
}
