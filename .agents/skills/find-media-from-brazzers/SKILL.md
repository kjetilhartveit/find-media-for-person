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
- **Search**: `brazzers.com/search?query={query}`

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
3. Extract poster images from video cards on profile pages
4. For full-size images/videos, visit individual video pages and parse their HTML
5. Poster thumbnails are typically 1080x1920 (vertical format)

## Tips

- **Two poster hash variants**: `m=eaSaaTbWx/.../poster/poster_01.jpg` (main video posters, ~150KB) and `m=eyzaevFb/.../poster/poster_01.jpg` (gallery thumbnails, ~40-60KB). Different pages may use different hash prefixes for their posters.
- **Profile images** from `image-service-ht.project1content.com` with `model/profile_001.jpg` — may have query parameters like `width=600&aspectRatio=3x4&imageVersion=...` that can be modified (e.g., `width=1200`).
- **Video page posters include cross-references** — poster URLs from other performers appear on a video page. Filter to the performer's hash prefix(es) to get only relevant posters.
- **Search may not find all performers** — some profiles exist but aren't returned by site search. Use Google: `site:brazzers.com "{performer name}"` to find profiles.

## Pitfalls

- **Video downloads** - full videos require parsing video page HTML for stream URLs
- **Poster URLs may be encoded** - the path segments are URL-encoded hash prefixes
- **Content may be behind paywall** - Some galleries are only available to premium users
- **Images may be watermarked** - Check if full-size images include branding
- **Rate limits** - Heavy scraping may trigger temporary IP blocks
- **No authentication needed** for page scraping but videos require login
