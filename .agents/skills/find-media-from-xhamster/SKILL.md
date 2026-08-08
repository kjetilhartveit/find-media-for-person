---
name: find-media-from-xhamster
description: Use when downloading media from XHamster profiles and content.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Downloading videos from XHamster user profiles
- Extracting galleries from XHamster
- Scraping pornstar pages on XHamster

# Find media from XHamster

XHamster is a **SPA (Single Page Application)** - most content is rendered client-side via JavaScript. This makes it one of the most difficult adult sites to scrape automatically.

## URL Patterns

- **Profile**: `xhamster.com/pornstars/{name}`
- **Gallery**: `xhamster.com/photos/gallery/{id}`
- **User galleries**: `xhamster.com/users/{handle}/photos`
- **User videos**: `xhamster.com/users/{handle}/videos`
- **Single video**: `xhamster.com/video/{id}`

## Primary method — Browser automation (REQUIRED)

XHamster requires a **real browser with JavaScript execution** because:

- Profile content (videos, thumbnails, metadata) is loaded via XHR/fetch calls
- gallery-dl returns 404 or "No results" for most URLs
- yt-dlp returns "Unsupported URL" for pornstars pages
- Cloudscraper returns stripped HTML without the actual content

```bash
# Using playwright (Python)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://xhamster.com/pornstars/halle-hayes")
    # Wait for content to load
    page.wait_for_selector('.video-list-item')
    # Extract video URLs, download, etc.
```

## Methods That Fail (Known Issues)

- **yt-dlp**: Returns "Unsupported URL" for `/pornstars/` pages. `/users/` path returns 0 videos.
- **Cloudscraper**: Page loads (200 OK, 25KB) but content is minimal - JavaScript-rendered video list is not in the response.
- **curl**: Returns empty or incomplete HTML without the JavaScript-rendered content.

## Recommendations

1. **Use browser automation** - playwright or selenium are essentially required
2. **Wait for API calls to complete** - Content is loaded via XHR after page load
3. **Check network tab** - Use DevTools to find the actual API endpoints that load video data
4. **XHamster has anti-bot protection** - May require realistic browser fingerprints
5. **Pagination** - Profiles show limited content per page; handle pagination carefully

## Technical Tips

- The profile at `xhamster.com/pornstars/halle-hayes` shows: 66 videos, 42.6M views, 26.6K subscribers for Halle Hayes
- Content is loaded via fetch/XHR calls to internal APIs
- Search the page source for `/api/` or `/fetch/` endpoints
- Video thumbnails are typically at `https://ic-vt-nss.xhcdn.com/` or `https://static-ah.xhcdn.com/`
- Actual video streams may be served from CDN with different domains

## Pitfalls

- **SPA architecture** is the main challenge - standard HTTP clients get minimal HTML
- **No working extractor** currently in gallery-dl for pornstars pages
- **yt-dlp XHamsterUser extractor** returns 0 videos for Halle Hayes profile
- **Rate limits** - Browser automation can hit rate limits on the API
- **Anti-bot** - May require realistic browser fingerprints and timing
