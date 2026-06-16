import { NextResponse } from 'next/server';
import { db } from '../../../lib/db';

export async function GET() {
  try {
    const res = await db.execute('SELECT * FROM themes ORDER BY id ASC');
    return NextResponse.json(res.rows);
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: 'Erro ao buscar temas' }, { status: 500 });
  }
}
