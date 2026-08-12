---
name: find-media-from-stkst
description: Use when you need to find and download media from stk.st. A content farm that specializes in viral adult entertainment content.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Searching stk.st for media of a specific person by query
- The site generates pages for search queries by matching keywords against its own database
- Best suited for finding adult content posts tagged with a person's name

# Find media from stk.st

## Current State (2024-2026)

stk.st is a WordPress content farm that specializes in viral adult entertainment content. It generates pages for any search query but results are limited to posts in its own database. It does NOT scrape or aggregate Reddit, Twitter/X, or Imgur content for specific individuals.

## URL Patterns

- Site: `https://stk.st`
- Profile/Query: `https://stk.st/{query}` — use `+` for spaces, e.g. `https://stk.st/halle+ahyes`
- Search endpoint: `https://stk.st/search?query={query}` — generates blog search results
- Images are served via WordPress Jetpack CDN: `https://i3.wp.com/origin-domain/path` (strip `i3.wp.com/` prefix to get original URL)

## Primary download method — Manual scraping and download

1. **Fetch the page**: `curl -s "https://stk.st/{query}" > page.html`
2. **Extract image URLs** from the page HTML:
   - Parse `<img>` tags with `src="https://i3.wp.com/..."` attributes — strip the `i3.wp.com/` prefix to get original URL
   - Filter for URLs matching known domains: `i.redd.it`, `pbs.twimg.com`, `imgur.com`
   - Note: Most content is the site's own adult blog content, not scraped Reddit/Twitter
3. **Filter out non-media content**: Exclude thumbnails, avatars, and site UI elements. Keep only images > 30KB.
4. **Download with rate limiting**: Sleep 0.3–0.5s between requests. Respect the site's anti-bot measures.

## Limitations & Recommendations

- **NOT recommended** for finding media of specific individuals (especially non-adult/non-porn individuals) — searches return posts matching ANY part of the query, often just the first name
- The site is specialized in adult entertainment content (cam models, OnlyFans leaks, etc.)
- Search results match keywords but do not guarantee the person matches (e.g., "sofie eikeland" returns posts about "sofie mills", "sofie skye", etc.)
- No Reddit/Twitter/X scraping or aggregation for specific individuals — posts only contain the site's own embedded media
- For general media of a person, prefer: Google Images, Instagram, X/Twitter, Pinterest

## Pitfalls

- WordPress content farm generates pages for ANY query, even non-matching ones
- Image URLs go through i3.wp.com CDN — must strip prefix to get original URL
- Thumbnails on the search page are 480x270 (low resolution) — need to follow to individual post for full-size
- No pagination on search results (all results on first page)
- Some post URLs may redirect to homepage (4815 byte response)
- Direct path queries like `stk.st/username` often 301 redirect to `/` (homepage) — use `/search?query=` instead
- Many posts use embedded video thumbnails (pornhub, xhamster, etc.) rather than Reddit/Twitter/Imgur images
