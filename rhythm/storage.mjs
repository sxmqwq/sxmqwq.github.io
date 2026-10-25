import { SCHEMA_VERSION, isValidSession, lyricsRevision } from './core.mjs';
import { MAX_LIBRARY } from './config.mjs';

export const STORAGE_KEY = 'rhythm:netease:v1';
export function emptyState() { return { version: SCHEMA_VERSION, library: [], sessions: {}, activeId: null, best: {} }; }

export function loadState(storage) {
  const initial = emptyState();
  try {
    storage ??= globalThis.localStorage;
    const raw = storage.getItem(STORAGE_KEY);
    if (!raw) return { state: initial, warning: '' };
    const value = JSON.parse(raw);
    if (value.version !== SCHEMA_VERSION || !Array.isArray(value.library)) throw new Error('version');
    for (const item of value.library.slice(0, MAX_LIBRARY)) {
      if (!/^[1-9]\d{0,19}$/u.test(String(item?.id)) || !Array.isArray(item.lines) || item.lines.length < 2 || item.lines.length > 2000) continue;
      if (!item.lines.every(line => typeof line?.text === 'string' && line.text.length > 0 && line.text.length <= 2000 && (line.time === null || (Number.isFinite(line.time) && line.time >= 0)))) continue;
      const song = { ...item, id: String(item.id), name: String(item.name || '未命名歌曲').slice(0, 300), artist: String(item.artist || '未知歌手').slice(0, 300), revision: lyricsRevision(item.lines) };
      if (initial.library.some(existing => existing.id === song.id)) continue;
      initial.library.push(song);
      const session = value.sessions?.[song.id];
      if (isValidSession(session, song)) initial.sessions[song.id] = session;
      initial.best[song.id] = Number.isInteger(value.best?.[song.id]) && value.best[song.id] >= 0 ? value.best[song.id] : 0;
    }
    initial.activeId = initial.sessions[value.activeId]?.phase === 'playing' ? value.activeId : null;
    return { state: initial, warning: '' };
  } catch {
    return { state: initial, warning: '未能恢复之前的曲库。你仍可读取网易云歌曲开始接龙。' };
  }
}

export function saveState(state, storage) {
  try { (storage ?? globalThis.localStorage).setItem(STORAGE_KEY, JSON.stringify(state)); return true; } catch { return false; }
}
