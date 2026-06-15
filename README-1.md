# ARCANA — Divination Engine PWA

Computational divination app: Astromancy, Bazi, Numerology, Onomancy, Cleromancy,
Palmistry OCR & Face Reading OCR. Installs as a native-like app on Android.

---

## Repo File Structure

```
arcana/
├── divination_engine.html   ← Main app
├── manifest.json            ← PWA manifest
├── sw.js                    ← Service worker
├── generate_icons.html      ← Icon generator (dev tool only)
├── icons/
│   ├── icon-192.png         ← Required app icon
│   └── icon-512.png         ← Required app icon
└── README.md
```

---

## Step 1 — Generate Icons

1. Open `generate_icons.html` in any browser
2. Click **Download icon-192.png** and **Download icon-512.png**
3. Create an `icons/` folder in your repo and place both files inside it

---

## Step 2 — Deploy to GitHub Pages

```bash
# Create a new repo (e.g. arcana) on GitHub, then:
git clone https://github.com/YOUR_USERNAME/arcana.git
cd arcana

# Copy all files in
cp /path/to/divination_engine.html .
cp /path/to/manifest.json .
cp /path/to/sw.js .
mkdir icons
cp /path/to/icon-192.png icons/
cp /path/to/icon-512.png icons/

git add .
git commit -m "feat: initial ARCANA PWA release"
git push origin main
```

Then in GitHub → repo Settings → Pages → set Source to `main` branch, root `/`.

Your app will be live at:
```
https://YOUR_USERNAME.github.io/arcana/divination_engine.html
```

---

## Step 3 — Install on Android

1. Open the URL above in **Chrome for Android**
2. A banner will appear at the bottom: **"Install ARCANA as an app"** — tap **INSTALL**
3. If the banner doesn't appear, tap Chrome menu (⋮) → **Add to Home screen**
4. ARCANA appears on your home screen like a native app

---

## Step 4 — Using the Camera on Android

In the **Palmistry** and **Face Reading** tabs:

| Mode | What happens on Android |
|------|--------------------------|
| 📷 Take Photo (Camera) | Opens rear camera directly — point at palm |
| 🤳 Take Selfie (Front Camera) | Opens front camera — for face reading |
| 🖼 Choose from Gallery | Opens photo gallery |

The camera opens **without any file picker** — straight to the lens.

> **Note:** The first time you use camera mode, Android will ask for camera permission.
> Tap **Allow** to grant it. This is a one-time prompt.

---

## Offline Capability

| Section | Works offline? |
|---------|---------------|
| Bazi / Four Pillars | ✅ Fully offline |
| Numerology | ✅ Fully offline |
| Onomancy | ✅ Fully offline |
| Cleromancy | ✅ Fully offline |
| Astromancy | ❌ Needs internet (Claude API) |
| Palmistry OCR | ❌ Needs internet (Claude API) |
| Face Reading OCR | ❌ Needs internet (Claude API) |

---

## Updating the App

After pushing changes to GitHub:

1. Open the app on Android
2. Pull down to refresh, or close and reopen
3. The service worker auto-updates within 24 hours, or immediately on next visit

To force an immediate update: Chrome menu → **More tools** → **Clear browsing data**,
then re-open the app.

---

## Tech Stack

- Pure vanilla HTML/CSS/JS — zero build step, zero dependencies
- PWA: Web App Manifest + Service Worker (Cache-First strategy)
- Claude Sonnet API (`claude-sonnet-4-6`) for Astromancy + Vision OCR
- Cryptographic entropy (`crypto.getRandomValues`) for Cleromancy
- Sexagenary calendar engine for Bazi (client-side)
- Pythagorean & Chaldean numeric reduction for Numerology/Onomancy
