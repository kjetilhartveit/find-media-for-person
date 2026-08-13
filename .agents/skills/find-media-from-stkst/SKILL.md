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
- Additional search variations: `/search?query={person}+onlyfans`, `/search?query={person}+onlyfans+porn`, `/search?query={person}+onlyfans+videos`

## Known Image Source Domains on stk.st

Content from stk.st search pages comes from various aggregated sources. The i3.wp.com CDN hosts images from: thefappeningblog.com, nudogram.com, fapello.com, masterfap.net, imgur.com, erome.com, pbs.twimg.com/photobucket.com, sexdug.com, mixputaria.com, testostetona.blog.br, viralpornhub.com, camwhores.tv, phncdn.com (Pornhub), rdtcdn.com (RedTube), xvideos-cdn.com, eporner.com, vrsmash.com, sxyprn.com.es, topfapgirls.com

## Primary download method — Manual scraping and download

1. **Fetch the page**: `curl -s -A "Mozilla/5.0 ..." "https://stk.st/search?query={person}+{query}" > page.html`
2. **Extract image URLs** from the page HTML:
   - Parse `<img>` tags with `src="https://i3.wp.com/..."` attributes — strip the `i3.wp.com/` prefix to get original URL
   - Filter for URLs matching known source domains (list above)
   - Filter for Clara Aguilar specific URLs: look for `clara-aguilar` in the URL path
   - Skip URLs with `:large` suffix from Twitter — use the base URL without `:large`
3. **Filter out non-media content**: Exclude thumbnails, avatars, and site UI elements. Keep only images > 30KB. Also filter out URLs that clearly reference other people (e.g., `clara-trinity`, `clara-morgane`, `clara-wilsey`, `clara-felicia-lindblom` when searching for "Clara Aguilar").
4. **Download with rate limiting**: Sleep 0.3–0.5s between requests. Respect the site's anti-bot measures.

## Limitations & Recommendations

- **NOT recommended** for finding media of specific individuals (especially non-adult/non-porn individuals) — searches return posts matching ANY part of the query, often just the first name
- The site is specialized in adult entertainment content (cam models, OnlyFans leaks, etc.)
- Search results match keywords but do not guarantee the person matches (e.g., "sofie eikeland" returns posts about "sofie mills", "sofie skye", etc.)
- gallery-dl does NOT support stk.st (no matching extractor found)
- For general media of a person, prefer: Google Images, Instagram, X/Twitter, Pinterest

## Pitfalls

- WordPress content farm generates pages for ANY query, even non-matching ones
- Image URLs go through i3.wp.com CDN — must strip prefix to get original URL when downloading
- Thumbnails on the search page are 480x270 (low resolution) — need to follow to individual post for full-size
- No pagination on search results (all results on first page)
- Some post URLs may redirect to homepage (4815 byte response)
- Direct path queries like `stk.st/username` often 301 redirect to `/` (homepage) — use `/search?query=` instead
- Many posts use embedded video thumbnails (pornhub, xhamster, etc.) rather than Reddit/Twitter/Imgur images
- **topfapgirls.com images**: the CDN URL structure no longer works — direct `img.topfapgirls.com/...` returns 301 redirect to homepage, and i3.wp.com proxies return HTML instead of images
- **fapello.com images**: may expire or return 404 if content was removed from the source site
- The search page includes advertisement posts at the top (check for `category-automotive` or other unrelated categories) — these are not actual search results
- Image downloads may require checking HTTP status codes — 403 can appear, and some domains block automated requests
