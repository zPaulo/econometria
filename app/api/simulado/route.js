import { db } from '@/lib/db';
import { NextResponse } from 'next/server';



export async function GET(request) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit')) || 50;

    // Fetch random questions
    const questionsRes = await db.execute({
      sql: 'SELECT * FROM questions ORDER BY RANDOM() LIMIT ?',
      args: [limit]
    });

    const questions = [];

    for (const q of questionsRes.rows) {
      const optionsRes = await db.execute({
        sql: 'SELECT * FROM options WHERE question_id = ? ORDER BY RANDOM()',
        args: [q.id]
      });

      questions.push({
        ...q,
        options: optionsRes.rows
      });
    }

    return NextResponse.json({ success: true, data: questions });
  } catch (error) {
    return NextResponse.json({ success: false, error: error.message }, { status: 500 });
  }
}
