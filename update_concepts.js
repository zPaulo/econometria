import { createClient } from '@libsql/client';

const db = createClient({
  url: 'file:econometria.db',
});

async function update() {
  await db.execute("UPDATE questions SET concept_slug = 'extrapolacao' WHERE theme_id = 1 OR theme_id = 2");
  await db.execute("UPDATE questions SET concept_slug = 'teste-adf' WHERE theme_id = 5");
  console.log('Updated existing questions with concept slugs.');
}
update();
