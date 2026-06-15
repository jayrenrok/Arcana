// ARCANA Service Worker — v1.0.0
// Caches the app shell for offline access.
// The Claude API calls still require internet; all computation-only
// sections (Bazi, Numerology, Onomancy, Cleromancy) work fully offline.

const CACHE_NAME = 'arcana-v1.0.0';

// App shell — files to cache on install
const SHELL = [
  './divination_engine.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  // Google Fonts — pre-cache for offline typography
  'https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&family=Cinzel+Decorative:wght@400;700&display=swap'
];

// ── Install: cache app shell ─────────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[ARCANA SW] Caching app shell');
      // Cache what we can; don't fail install if font CDN is offline
      return Promise.allSettled(
        SHELL.map(url => cache.add(url).catch(err => console.warn('[SW] Could not cache:', url, err)))
      );
    }).then(() => self.skipWaiting())
  );
});

// ── Activate: remove old caches ──────────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => {
            console.log('[ARCANA SW] Deleting old cache:', key);
            return caches.delete(key);
          })
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch: cache-first for shell, network-first for API ──────────
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Always go network for Anthropic API calls — never cache AI responses
  if (url.hostname === 'api.anthropic.com') {
    event.respondWith(fetch(request));
    return;
  }

  // Cache-first strategy for everything else (app shell, fonts, icons)
  event.respondWith(
    caches.match(request).then(cached => {
      if (cached) return cached;

      // Not in cache — fetch from network and cache a copy
      return fetch(request).then(response => {
        // Only cache valid same-origin or CORS responses
        if (!response || response.status !== 200 ||
            (response.type !== 'basic' && response.type !== 'cors')) {
          return response;
        }

        const responseClone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(request, responseClone));
        return response;
      }).catch(() => {
        // Offline fallback: return cached main page for navigation requests
        if (request.mode === 'navigate') {
          return caches.match('./divination_engine.html');
        }
      });
    })
  );
});

// ── Message: force update from app ───────────────────────────────
self.addEventListener('message', event => {
  if (event.data === 'SKIP_WAITING') self.skipWaiting();
});
