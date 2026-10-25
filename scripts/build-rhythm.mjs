import { mkdir, copyFile, access } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const files = ['index.html', 'styles.css', 'app.mjs', 'core.mjs', 'api.mjs', 'storage.mjs', 'config.mjs', 'favicon.svg'];
await access(join(root, 'docs', 'index.html'));
await mkdir(join(root, 'docs', 'rhythm'), { recursive: true });
for (const file of files) await copyFile(join(root, 'rhythm', file), join(root, 'docs', 'rhythm', file));
console.log(`rhythm: copied ${files.length} files to docs/rhythm/`);
