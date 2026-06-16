import { createClient } from '@libsql/client';
import { NextResponse } from 'next/server';

const db = createClient({
  url: 'file:econometria.db',
});

export async function POST(request) {
  try {
    const { question_id, is_correct } = await request.json();
    
    await db.execute({
      sql: 'INSERT INTO user_progress (question_id, is_correct) VALUES (?, ?)',
      args: [question_id, is_correct ? 1 : 0]
    });

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Failed to save progress:', error);
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}

export async function GET() {
  try {
    const res = await db.execute(`
      SELECT 
        q.theme_id, 
        COUNT(up.id) as total_answers,
        SUM(up.is_correct) as correct_answers
      FROM user_progress up
      JOIN questions q ON up.question_id = q.id
      GROUP BY q.theme_id
    `);

    // Obter também as estatísticas por conceito (fraquezas)
    const conceptsRes = await db.execute(`
      SELECT 
        q.concept_slug,
        COUNT(up.id) as total_answers,
        SUM(up.is_correct) as correct_answers
      FROM user_progress up
      JOIN questions q ON up.question_id = q.id
      WHERE q.concept_slug IS NOT NULL
      GROUP BY q.concept_slug
      HAVING total_answers > 0
    `);

    return NextResponse.json({ 
      success: true, 
      themes: res.rows,
      concepts: conceptsRes.rows
    });
  } catch (error) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
