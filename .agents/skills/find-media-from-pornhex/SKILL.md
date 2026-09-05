---
name: find-media-from-pornhex
description: Use when you need to find and download media from Pornhex (pornhex.com / no.pornhex.com), a free adult video aggregator with signed-URL MP4 downloads and per-video thumbnail sets.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# Use this skill when

- Searching for a specific performer on Pornhex (a free porn video aggregator)
- Downloading MP4 videos from Pornhex pages like `pornhex.com/video/<slug>`
- Enumerating the 8 still thumbnails a Pornhex video page exposes

# Find media from Pornhex

Main site: `https://pornhex.com` (regional subdomains exist, e.g. `https://no.pornhex.com` — they mirror the same catalog).

## URL Patterns

- **Video page**: `https://pornhex.com/video/<slug>` (slug is derived from the title but with some consonant runs dropped, e.g. `"andrea rincon alarma tv #1"` -> `re-rcon-lrm-tv-1`)
- **Search**: `https://pornhex.com/search?q=<query>` — returns a results list (title + duration + views + age) mixed with unrelated "recommended" videos; always filter by title
- **NOT a search**: `pornhex.com/s/<slug>` is a dead video path (404 "Video Removed"), not a search endpoint
- **Embed**: `https://pornhex.com/video/embed/<videoId>`
- Video ids look like `BTjz60RaF8oD` (12-char base62); media is hosted on `<model>.pornhex.com/volN/media/video/<id>/...` subdomains (e.g. `rhea.`, `theia.`, `iluna.`, `itheia.`, `itethys.`)

## Access: Cloudflare protected

- Plain `curl`/requests get 403 "Verifying Your Connection" (Cloudflare challenge).
- **Use `curl_cffi` with browser impersonation** — this works without any cookies/login:

```python
from curl_cffi import requests
s = requests.Session(impersonate='chrome')
r = s.get('https://pornhex.com/search?q=andrea+espada', timeout=30)
```

- `yt-dlp` and `gallery-dl` have **no extractor** for Pornhex. yt-dlp also gets 403 on the MP4s (no impersonation). Do all fetching via curl_cffi sessions.
- A `pornhex_session` cookie is set automatically; keep it in one session for the whole crawl.

## Finding media

1. Search each known name/alias separately: `search?q=<alias>` (URL-encode spaces as `+` or `%20`).
2. Parse `/video/<slug>` links with the following title text from the results page JSON/HTML. Titles are the reliable identity signal (hair color, ethnicity, country words like the person's birthplace, documented aliases).
3. Low view counts (tens of views) are normal for webcam-era performer clips — do not dismiss as fake on that basis.

## Downloading videos (signed URLs)

- Direct `.mp4` URLs are **signed**: the CDN answers bare URLs with `403 Missing signature`.
- The video page contains inline JS with the signature per quality:

```javascript
var videoSources = [
  {"src":"https://rhea.pornhex.com/vol3/media/video/XXX/720p.mp4","k":"<base64 sig>","label":"720p","type":"video/mp4"},
  {"src":"https://rhea.pornhex.com/vol3/media/video/XXX/480p.mp4","k":"<base64 sig>","label":"480p","type":"video/mp4"}
];
// player2.*.js: videoSources.forEach(n => n.src = n.src + "?h=" + n.k)
```

So the working URL is simply `src + "?h=" + k`. Parse with:

```python
import re, json
m = re.search(r'var videoSources = (\[.*?\]);', html)
sources = json.loads(m.group(1))
url = s480['src'] + '?h=' + s480['k']
data = session.get(url, timeout=900, headers={'Referer': 'https://pornhex.com/'}).content
```

- Quality labels seen: `low_res` (can be odd aspect ratios like 640x554 for webcam content), `480p`, `720p`, sometimes `1080p`. Prefer 480p to save bandwidth.
- 7-minute clips at 480p/low_res are ~40-50MB.
- `preview.mp4` (~290KB teaser clip) works **unsigned** — useful for probing without spending bandwidth.

## Thumbnails (unsigned)

Each video exposes 8 still frames plus a poster, all downloadable without a signature (same session + Referer header recommended):

```
https://<host>/volN/media/video/<id>/thumb/1.jpg ... thumb/8.jpg
https://<host>/volN/media/video/<id>/poster.jpg
https://<host>/volN/media/video/<id>/thumb/timeline.vtt
```

These are full-video stills of the performer — cheap extra media to archive alongside the video.

## Pitfalls

- **`/s/<slug>` is not search** — it 404s with "Video Removed" (title `Video Removed • Pornhex`). Use `/search?q=`.
- **HEAD requests 403** — probe media files with a ranged GET (`Range: bytes=0-1023`) to read `Content-Range` for file size.
- **curl_cffi has no streaming context manager** (`with r: ...` raises); use plain `session.get(url, timeout=...)` and `r.content` (files here are small enough for memory).
- **Search results include generic "related" videos** — the page mixes true matches with unrelated recommendations; verify titles before downloading.
- **Varying media hosts** — each video lives on a different `<model>.pornhex.com/volN/` host; take the host exactly from the page, do not guess.
- **recaptcha on the page** is for posting/comments only; browsing and downloading need no interaction.
