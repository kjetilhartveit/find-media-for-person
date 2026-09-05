---
name: find-media-from-brazzers
description: Use when scraping media from Brazzers profiles and video pages.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Scraping image thumbnails from Brazzers profile pages
- Extracting poster images from video pages
- Collecting media from Brazzers pornstar profiles

# Find media from Brazzers

Brazzers is accessible via standard HTTP scraping tools (curl, cloudscraper).

## URL Patterns

- **Profile**: `brazzers.com/pornstar/{id}/{name}`
- **Video**: `brazzers.com/video/{id}/{title}`
- **Search**: `brazzers.com/search?query={query}` (unreliable - see Pitfalls)
- **Actor full video list**: `brazzers.com/videos/models/{actorId}/{slug}/` (default = newest first) and `brazzers.com/videos/models/{actorId}/{slug}/sortby/rating/`. The "View all" links under *Latest Videos* / *Top Rated Videos* on a profile point here.
- **Pagination**: `?page=2` works, but SSR seems clamped at 2 pages (24 vids/page) per sort order - higher pages just repeat. To get a more complete catalog, union the default and `sortby/rating` listings (plus the ~24 cards on the profile page) and dedupe; some older scenes only appear in one of the two sorts.

## Download Method — curl with regex extraction

```bash
# Fetch profile page
curl -sL -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36" \
  "https://www.brazzers.com/pornstar/22939/halle-hayes" | \
  grep -oP '(https://[^\s"<>]+\.(?:jpg|jpeg|png|webp)[^\s"<>]*)' | \
  grep -v 'placeholder\|logo\|icon\|favicon\|banner' | \
  sort -u > brazzers_urls.txt

# Download images
while IFS= read -r url; do
  curl -sL -A "Mozilla/5.0" -o "$filename" "$url"
done < brazzers_urls.txt
```

## Extracting Poster Images

Poster images are at: `https://media-public*.project1content.com/`
Pattern: `https://media-public-fl.project1content.com/m=XXXX/poster/poster_01.jpg`
The path segments encode the image: `//m=XXXX/ddd/82a/015/bb3/.../poster/poster_01.jpg`

```bash
# Specific poster extraction
curl -sL -A "Mozilla/5.0" \
  "https://www.brazzers.com/pornstar/22939/halle-hayes" | \
  grep -oP 'https://media-public[-\w]*\.project1content\.com[^\s"<>]*poster[^\s"<>]*' | \
  sort -u
```

## Recommendations

1. Use `curl` with a proper `User-Agent` header - no Cloudflare protection
2. Cloudscraper works but is not needed - site responds to standard requests
3. Get the actor's complete scene catalog from `/videos/models/{actorId}/{slug}/?page=N`, not just the profile page (profile shows ~24 cards mixed with *recommended* videos of other performers)
4. Verify a scene actually features the performer: the HTML `<title data-rh="true">` lists the full cast ("Title With Performer A, Performer B" or "Page Not Found | Brazzers")
5. Visit individual video pages to parse metadata - they embed everything server-side (no API needed)

## Video page metadata (best source)

- **VideoObject JSON-LD** (`<script type="application/ld+json">`) per video page contains: `name`, `description` (full scene synopsis), `thumbnailUrl` (poster), `uploadDate`. Best per-scene metadata on the site.
- **Scene tags** are SSR'd as links `/videos/tags/{id}/{slug}/` on the video page. Tag sets differ per scene and can be used to e.g. find `Facial` (tag id 66), `Cumshot` tagged scenes. Note: in multi-performer scenes the tag describes the scene, not necessarily the target performer.
- The first `<img src=".../poster/poster_01.jpg">` on a video page is the scene's own poster; the rest are related/cast videos.
- **Two poster hash variants**: `m=eaSaaTbWx/.../poster/poster_01.jpg` (main video posters, **1280x720 landscape, ~100-150KB** - highest quality obtainable) and `m=eyzaevFb/.../poster/poster_01.jpg` (gallery thumbnails, ~40-60KB). The `m=` transform hashes are signed - you cannot add `?width=` or swap them for larger renditions.
- **Profile images** from `image-service-ht.project1content.com` with `model/profile_001.jpg` — the `width=600` parameter can be bumped up (e.g. `width=1200` → 1200x1599 portrait). Usually only `profile_001` exists.
- **Search may not find all performers/videos** — site search (`/search?query=`) returns fuzzy results mixed with popular videos; it may not even list the performer's profile. Use Google: `site:brazzers.com "{performer name}"` to find profiles.
- **Detecting "performer does not exist on Brazzers"**: if a performer has no Brazzers content, site search still returns a full page (title `Page Not Found | Brazzers` in `<title data-rh="true">`) but it contains only generic popular videos/profiles — zero `/video/…` or `/pornstar/…` links and zero `<title>` cast mentions matching the query. Grepping the page HTML for the performer's name only hits the SSR `prev`-query navigation payload, not real results. Cross-check with a web search for `site:brazzers.com "{name}"` / `"{name}" brazzers`. If both are empty, the performer is not in the Brazzers catalog — stop and move to other sources instead of downloading anything.

## Pitfalls

- **"Page Not Found" string appears in the embedded JSON of every page** (SSR fallback template) - do not use it to detect 404s; check `<title data-rh="true">` instead.
- **Profile page is mostly a shell** - the actor's bio/tags/videos are SSR'd, but there is no separate "photos" section; free images = profile photo + one poster per scene.
- **Video/trailer streams require login** - no public m3u8/mp4 in the page HTML; `canDownloadGallery`/`canViewGallery` flags are for premium only.
- **Poster URLs may be encoded** - the path segments are URL-encoded hash prefixes
- **Content may be behind paywall** - Some galleries are only available to premium users
- **Images may be watermarked** - Check if full-size images include branding
- **Rate limits** - Heavy scraping may trigger temporary IP blocks
- **No authentication needed** for page scraping but videos require login
