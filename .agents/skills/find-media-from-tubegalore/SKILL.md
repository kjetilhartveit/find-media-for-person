# Skill: find-media-from-tubegalore

# When to use this skill

- Use when you need to find and download media from TubeGalore (tubegalore.com).
- TubeGalore is a video aggregation site that aggregates content from many other porn tube sites (Eporner, Pornhub, etc.).
- It wraps content from third-party sources and provides affiliate links to the actual video pages.

# Main website

- URL: https://www.tubegalore.com/
- Search URL: https://www.tubegalore.com/searching/by-form (POST request with `search_query[query]` parameter)
- Pornstar page: https://www.tubegalore.com/pornstar/{name-slug}

# Example URLs

- Search: https://www.tubegalore.com/searching/by-form
- Pornstar: https://www.tubegalore.com/pornstar/layla-jenner

# How to search and download from TubeGalore

## Scraping approach

TubeGalore is protected by Cloudflare. Use `cloudscraper` to bypass the protection:

```python
import cloudscraper
scraper = cloudscraper.create_scraper()
resp = scraper.post("https://www.tubegalore.com/searching/by-form", data={
    "search_query[query]": "PORNSTAR_NAME",
    "search_query[LIMIT]": "3"
}, timeout=30)
```

## Extracting video URLs

TubeGalore uses base64-encoded URLs in `/out/?l=` redirect links. To extract the actual video URLs:

```python
import re
import base64
from urllib.parse import unquote

# Find all /out/?l= links
out_links = re.findall(r'/out/\?l=([^"\']+)', text)

for link in out_links:
    decoded = unquote(link)
    padded = decoded + '=' * (4 - len(decoded) % 4)
    decoded_text = base64.b64decode(padded).decode('utf-8', errors='ignore')
    # Extract URLs from decoded text
    urls = re.findall(r'https?://[^\s"\'<>)\]]+', decoded_text)
```

## Key notes

- Each video card generates multiple affiliate links (~4 per video), so the raw count of URLs is inflated. Actual unique videos = total URLs / ~4.
- Search with LIMIT=3 typically returns ~30 unique videos (120 raw affiliate links).
- The pornstar page (e.g., /pornstar/layla-jenner) returns similar content with pagination.
- Video sources include: Eporner (best quality), Pornhub, xhand.net, babestube, sortporn, and many smaller tube sites.
- After decoding the base64 URLs, cleaning params is required: remove `trx`, `utm_source`, `utm_medium`, `utm_campaign`, `subid`, `aff`, etc.

## Using yt-dlp

Once you have clean video URLs, use yt-dlp to download:

```bash
yt-dlp --no-check-certificates --restrict-filenames -f 'best[height<=720]' \
  --merge-output-format mp4 "VIDEO_URL"
```

Note: Eporner videos tend to be large (300-700MB+) and download slower than expected. Consider limiting resolution with `-f 'best[height<=480]'` for faster downloads.

## Known limitations

- Cloudflare protection requires cloudscraper (standard curl/wget returns 403).
- Some sources (Eporner videos) download very slowly for large files.
- No gallery-dl extractor for TubeGalore.
- Thumbnail images are available in two resolutions: 288x162 and larger versions (800x534) served from ttcache.com CDNs.
- Many affiliate links point to different sites from the same underlying video, causing duplicates.