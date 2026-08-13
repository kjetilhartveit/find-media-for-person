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

stk.st is a WordPress content farm that specializes in viral adult entertainment content. It generates pages for any search query by matching keywords against its own database. It does NOT scrape or aggregate Reddit, Twitter/X, or Imgur content for most individuals — the "images" come from specific adult-content hosts.

## Example URLs by Person

- **Not all person queries return relevant content:** Searches for non-adult celebrities (e.g., "megan thee stallion") typically return no matches or completely unrelated results. stk.st focuses on adult content creators, cam models, and OnlyFans leak aggregators.

## URL Patterns

- Site: `https://stk.st`
- Profile/Query: `https://stk.st/{query}` — use `+` for spaces, e.g. `https://stk.st/halle+ahyes`
- Search endpoint: `https://stk.st/search?query={query}` — generates blog search results
- Images are served via WordPress Jetpack CDN: `https://i3.wp.com/origin-domain/path` (strip `i3.wp.com/` prefix to get original URL)
- Additional search variations: `/search?query={person}+onlyfans`, `/search?query={person}+onlyfans+porn`, `/search?query={person}+onlyfans+videos`

## Known Image Source Domains on stk.st

Content from stk.st pages comes from various aggregated sources. **Important**: stk.st does NOT aggregate Reddit, X/Twitter, or Imgur content for most individuals — images come directly from adult-content hosting sites. Images go through WordPress Jetpack CDN: `https://i3.wp.com/origin-domain/path` (strip `i3.wp.com/` prefix to get original URL).

Common image domains: thefappeningblog.com, nudogram.com, fapello.com, masterfap.net, erome.com, sexdug.com, mixputaria.com, virulpornhub.com, camwhores.tv, phncdn.com (Pornhub), rdtcdn.com (RedTube), xvideos-cdn.com, xnxx-cdn.com, eporner.com, vrsmash.com, sxyprn.com.es, babes.plus, vip.sexhd.pics / sexhd.pics, cdn5-images.motherlessmedia.com, www.xxxporn.pics, tiny-asians.com, wallpaperheaven.com

## Primary download method — Manual scraping and download

1. **Fetch the page**: `curl -s --tls-max 1.2 -A "Mozilla/5.0 ..." "https://stk.st/{query}" > page.html`
   - Use `--tls-max 1.2` flag to bypass Cloudflare challenges on some pages
   - Use `-k` flag if HTTPS verification fails
2. **Extract image URLs** from the page HTML (focus on `entry-content` area of individual post pages):
   - Find `<img>` tags with `class="...wp-image-\d+..."` — these are the article's actual images
   - Strip `https://i3.wp.com/` prefix to get original URL
   - Filter out video thumbnails (xvideos-cdn, xnxx-cdn, phncdn, pornwhite, wankoz)
   - Skip URLs that reference other people (check alt text and URL path for the person's name)
   - The lightbox links pattern: `href="original-url"` next to `src="https://i3.wp.com/..."`
3. **Download with rate limiting**: Sleep 0.3–0.5s between requests. Some domains may block automated requests or have SSL/DNS issues.

## Limitations & Recommendations

- **NOT recommended** for finding media of specific individuals (especially non-adult/non-porn individuals) — searches return posts matching ANY part of the query, often just the first name
- The site is specialized in adult entertainment content (cam models, OnlyFans leaks, etc.)
- Search results match keywords but do not guarantee the person matches (e.g., "sofie eikeland" returns posts about "sofie mills", "sofie skye", etc.)
- gallery-dl does NOT support stk.st (no matching extractor found)
- For general media of a person, prefer: Google Images, Instagram, X/Twitter, Pinterest
- stk.st **does NOT** actually aggregate Reddit or X/Twitter content — images are loaded from specific adult content hosts, not social media platforms
- **Use TLS 1.2 (`--tls-max 1.2`)** with curl when fetching stk.st pages — some pages behind Cloudflare challenge pages are more reliably fetched with TLS 1.2
- **Focus on individual post URLs** (e.g., `/joon+mali+naked`) rather than search pages for cleaner, more relevant results

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
- **Network-accessible domains vary**: Some source domains may be unreachable due to DNS failures (e.g., motherlessmedia.com, vip.sexhd.pics) or SSL certificate issues (e.g., babes.plus — Let's Encrypt intermediate not in trust store). Test each domain's accessibility before relying on it.
- **Pages with generic keywords (e.g., "Mali") produce lots of noise**: News, sports, and political content may match the individual's name. Use keyword-specific post paths (e.g., `/joon+mali+naked`) for cleaner results.
- The i3.wp.com proxy sometimes returns 400/403 for certain domains — don't rely on it as a download method, use direct URLs instead.
