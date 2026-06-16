import fs from 'fs';
import path from 'path';

function walkDir(dir, callback) {
  fs.readdirSync(dir).forEach(f => {
    const dirPath = path.join(dir, f);
    const isDirectory = fs.statSync(dirPath).isDirectory();
    isDirectory ? walkDir(dirPath, callback) : callback(dirPath);
  });
}

walkDir(path.join(process.cwd(), 'app', 'api'), (filePath) => {
  if (filePath.endsWith('.js')) {
    let content = fs.readFileSync(filePath, 'utf8');
    let changed = false;

    // Remove createClient import
    if (content.includes("import { createClient } from '@libsql/client';")) {
      content = content.replace("import { createClient } from '@libsql/client';", "import { db } from '@/lib/db';");
      changed = true;
    }

    // Remove db initialization
    const initRegex = /const db = createClient\(\{\s*url:\s*'file:econometria\.db',?\s*\}\);/g;
    if (initRegex.test(content)) {
      content = content.replace(initRegex, "");
      changed = true;
    }

    if (changed) {
      fs.writeFileSync(filePath, content);
      console.log(`Updated ${filePath}`);
    }
  }
});
