import { createClient } from '@libsql/client';

const db = createClient({
  url: 'file:econometria.db',
});

const videos = [
  'https://www.youtube.com/embed/prx1JOklZ3c', // Theme 1
  'https://www.youtube.com/embed/vopRggQ_FMo', // Theme 2
  'https://www.youtube.com/embed/5-2C4eO4cPQ', // Theme 3
  'https://www.youtube.com/embed/WbJqALx8x5I', // Theme 4
  'https://www.youtube.com/embed/oY-j2Wof51c', // Theme 5
  'https://www.youtube.com/embed/3cyqwPNsqD8', // Theme 6
  'https://www.youtube.com/embed/1PZq5gR3qG4', // Theme 7
];

async function updateVideos() {
  for (let i = 0; i < videos.length; i++) {
    const theme_id = i + 1;
    await db.execute({
      sql: 'UPDATE lessons SET video_url = ? WHERE theme_id = ?',
      args: [videos[i], theme_id]
    });
  }
  console.log("Videos updated successfully!");
}

updateVideos().catch(console.error);
