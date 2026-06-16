const fs = require('fs');
const path = 'C:\\\\Users\\\\paulo.arruda\\\\.gemini\\\\antigravity\\\\brain\\\\d41c0b71-b79c-424d-90ae-cd0d303d798e\\\\.system_generated\\\\logs\\\\transcript.jsonl';

const lines = fs.readFileSync(path, 'utf8').split('\n');
for (let line of lines) {
  if (!line) continue;
  try {
    const obj = JSON.parse(line);
    if (obj.content && obj.content.includes('```json')) {
      const jsonStr = obj.content.split('```json')[1].split('```')[0].trim();
      fs.writeFileSync('questions.json', jsonStr);
      console.log('JSON extracted to questions.json successfully!');
      break;
    }
  } catch(e) {}
}
