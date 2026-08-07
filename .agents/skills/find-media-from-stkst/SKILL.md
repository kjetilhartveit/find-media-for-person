---
name: find-media-from-stkst
description: Use when you need to find and download media from stk.st, a Reddit + X/Twitter image aggregation site with embedded media from multiple platforms.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for aggregated media of a specific person from stk.st (Reddit + X image aggregator)
- Downloading images embedded from Reddit, X/Twitter, Imgur, and other platforms
- Searching stk.st by query to find profile pages matching a person

# Find media from stk.st

Download aggregated media from stk.st (https://stk.st), a site that aggregates images from Reddit (i.redd.it) and X/Twitter media into a single feed.

**`gallery-dl` and `yt-dlp` do NOT have built-in extractors for stk.st.** Use manual scraping with curl/wget and Python requests.

## URL Patterns

- Site: `https://stk.st`
- Profile/Query: `https://stk.st/{query}` — use `+` for spaces, e.g. `https://stk.st/halle+ahyes`
- Reddit image source: `https://i.redd.it/{random_id}.jpg`
- X/Twitter media source: `https://pbs.twimg.com/media/{media_id}:{format}?format={ext}`
- Imgur source: `https://i.imgur.com/{id}.jpg`

## Primary download method — Manual scraping and download

1. **Fetch the profile page**: `curl -s "https://stk.st/{query}" > page.html`
2. **Extract image URLs** from the page HTML:
   - Parse `<img>` tags or `data-`/`src` attributes
   - Filter for URLs matching known domains: `i.redd.it`, `pbs.twimg.com`, `i.imgur.com`, `pbs.twimg.com/media`
   - Also capture Twitter video URLs when present (`.mp4` on pbs.twimg.com)
3. **Filter out non-media content**: Exclude thumbnails, avatars, and site UI elements. Keep only images > 30KB.
4. **Download with rate limiting**: Sleep 0.3–0.5s between requests. Respect the site's anti-bot measures.
5. **Handle infinite scroll**: stk.st may have additional content behind lazy-load/infinite scroll. The initial page fetch will get the visible items; additional pages may exist.

## Quality

- Images vary widely in quality depending on the source platform (Reddit, X, Imgur)
- Reddit images tend to be decent resolution (typically 800px–1920px wide)
- X/Twitter images may be compressed; prefer `.jpg` over `.jpg:small`
- Video content may be available from X/Twitter source (MP4 format)
- File sizes range from ~20KB to ~800KB+

## Pitfalls

- No gallery-dl extractor available — requires custom scraping
- Some image URLs may be expired or removed from source platforms (404s)
- SSL errors may occur on some URLs — handle gracefully and skip
- Query may need URL-encoding adjustments (e.g., spaces as `+` or `%20`)
- Infinite scroll means not all content may be visible in initial page load
- No album structure — images are presented as a single feed