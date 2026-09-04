---
name: find-media-from-aznude
description: Use when you need to find and download media from AZNude, a celebrity nude content aggregator with hosted images and embedded videos.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for media of a specific celebrity/person on AZNude
- AZNude has dedicated pages per celebrity

# Find media from AZNude

Download media from AZNude (https://www.aznude.com), a celebrity nude content site with dedicated pages per celebrity.

## URL Patterns

- Site: `https://www.aznude.com`
- Celebrity page: `https://www.aznude.com/view/celeb/{initial}/{slug}.html` — first letter + lowercase slug
- Story pages: `https://www.aznude.com/view/story/{initial}/{slug}{story-description}.html`
- Images from CDN: `cdn2.aznude.com/{slug}/{category}/{filename}.jpg`
- User uploads (full-size via user-uploads): `user-uploads.aznude.com/data/azncdn/{hash}/{name}.jpg`
- User uploads (full-size via cdn2): `cdn2.aznude.com/{hash}/{hash}.jpg` — 32-char hex hash, both URL segments identical
- Full-size CDN images (from celeb page): `cdn1.aznude.com/{slug}/{category}/{filename}.jpg` — referenced via `href` attribute
- Video thumbnails: `cdn2.aznude.com/antibandit/{slug}/{category}/thumb3_{name}.jpg`

## Recommendations on how to download

- **Slug variations** — try lowercase concatenated words (e.g., `megantheestallion`) and hyphenated (e.g., `megan-thee-stallion`). For Indian models whose display name is "X Bhabhi", try variations like `xname`, `x-name`, `xname-sarkar`, `x-name-sarkar`. For adult performers who go by stage names, also try their real name format (e.g., `layla-fenner` for "Layla Jenner").
- **Page existence** — Not all celebs have a page on AZNude. Many popular performers (especially newer adult film actresses) may not have dedicated pages. If the celeb page 404s, search will also return 0 results. Not all celebrities are on AZNude.
- **Search limitations** — The search results are rendered client-side via JavaScript. The search page shows skeleton loaders initially — actual content loads via JS. `curl`/`grep` only works for pages loaded server-side (celeb/story/movie pages directly). Search queries will return 0 results for performers not indexed by AZNude.
- **Stories** — celeb pages have story links in the HTML. Extract story URLs with: `curl | grep -oE 'href="/view/story/[a-z]/[a-z0-9-]*\.html"'`. Then fetch each story URL to get its images from `user-uploads.aznude.com/data/azncdn/`.
- **Story pages contain the full image set** — the celeb page only shows a subset of each story's images (e.g. 45 photos on the celeb page, but a single story page carried 120+ hash-based stills). To get maximum content, fetch and extract images from ALL story pages linked from the celeb page, then dedupe by URL.
- **Videos** — video m3u8 URLs are server-rendered in celeb/story HTML. Extract with `grep -oE 'https://cdn2\.aznude\.com/hls/[^"]+\.m3u8'`. Pattern: `https://cdn2.aznude.com/hls/{videoId}-{quality}/{videoId}-{quality}.m3u8` (videoId is a 32-char hex; `-hd` is high quality, also referenced by the embed id `{videoId}-hd.html`). Download the m3u8 directly with `yt-dlp` — no auth needed. Videos can be full scene rips (30+ min, ~1.5–2GB) or short clips.
- **Direct mp4 clips** — some short clips (movie scenes, ~1–2 min) are also served as direct mp4s: `https://cdn1.aznude.com/{slug}/{category}/{name}-hi.mp4` (480p) and `-lo.mp4` (360p). The recommender JSON `cdn.aznude.com/recommender/{videoId}-hi-chromecast-v5.json` lists playable sources; its playlist may also contain "more like this" entries for _other_ celebs — only take entries whose URL path contains the target celeb's slug.
- **Movie pages** — celeb pages list linked movie pages with additional images. Extract movie URLs with `grep -oP 'href="/view/movie/[a-z0-9-]+\.html'`. Movie pages use `largeCelebPage-4.jpg` and `gigantic-4.jpg` for their images, not the patterns used on celeb pages.
- **Extract media URLs** using `curl | grep`:
  - Download full-size images from `user-uploads.aznude.com/data/azncdn/` paths (not `data/thumbs/`).
  - Download full-size images from `cdn2.aznude.com/{hash}/{hash}.jpg` (32-char hex, both segments same).
  - Download full-size CDN images from `cdn1.aznude.com/{slug}/` (referenced via `href` in celeb page).
  - Download `cdn2.aznude.com/{slug}/` category images (not `/antibandit/` thumbnails).
  - Filter out `/images/categories/` (category icons), `/sparkthumbs/`, and biopic images of unrelated celebs.
- **No auth required.** Rate limit: sleep 0.3–0.5s between requests.
- Some celeb pages may have 404 if no content exists — try slug variations.

## Quality

- Images: CDN images (~30KB–150KB), hash-based uploads (~15–30KB), user-uploads via azncdn (~150KB–300KB+). CDN images may be lower compression but still reasonable quality. Hash-based uploads on cdn2 may be compressed versions.
- Content: mix of leaked photos, bikini/swimwear, scene stills from movies/TV, red carpet, and social media.
- Moderate value per celeb. Content may be sourced from other aggregators (reposted).
- Some celeb pages have no stories or movies — only a handful of images from collections. Check the `categories` section to gauge content volume.

## Pitfalls

- **Slug format** — the slug may not follow simple hyphenation rules. Try both `slug` and `slug-name` variations. For Indian models with "Bhabhi" nicknames, try concatenated first name + last name without spaces.
- **Many URL patterns** — images come from multiple CDN paths. Must filter carefully.
- **Thumbnails** use different paths (`/thumbs/`, `/antibandit/`) — don't confuse with full-size.
- **Biopic images** on the page may include thumbnails for _other_ celebs (sidebar/related). Download only images whose URL path contains the target celeb's slug.
- **Movies vs celeb pages** — movie pages use `-largeCelebPage-4.jpg` and `-gigantic-4.jpg` image patterns, not the `/slug/` path pattern. The grep for `largeCelebPage` images must exclude `boxpic/` (movie cover) and `vtt/` (subtitles) from the URL paths.
- **Stories loaded via JS** — story links on the celeb page are rendered client-side. Use curl/grep to discover story URLs, then process each individually.
- **Search is JS-rendered** — direct `curl` requests to `/search.html?q=...` won't return actual search results. A celeb page may not exist even for well-known performers; verify by trying direct URL access first.