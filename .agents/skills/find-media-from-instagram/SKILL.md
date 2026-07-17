---
name: find-media-from-instagram
description: Download media from Instagram posts, reels, and stories using gallery-dl with cookie authentication.
---

# Find media from Instagram

Download images and videos from Instagram using `gallery-dl` with cookie-based authentication.

## URL Patterns

- **Posts**: `instagram.com/p/{shortcode}` — images, carousels, or video posts
- **Reels**: `instagram.com/reel/{shortcode}` — short-form video
- **Stories**: `instagram.com/stories/{username}/{id}` — ephemeral content (24h only, must be active)

## Prerequisites

- `gallery-dl` installed (`pip install gallery-dl` or `pipx install gallery-dl`)
- Valid Instagram session cookie in `.data/cookies.txt` (Netscape format)
- Python installation

## Authentication

Instagram has no public API. Authentication uses a logged-in user's `sessionid` cookie stored in a Netscape-format `cookies.txt` file.

### Getting the session cookie

1. Log into Instagram in a browser
2. Open DevTools → Application → Cookies → `.instagram.com`
3. Find the `sessionid` cookie
4. Copy its value and expiry date

### cookies.txt format

```
# Netscape HTTP Cookie File
# domain  includeSubdomains  path  secure  expiry  name  value
.instagram.com	TRUE	/	TRUE	1810569780	sessionid	<your_sessionid_value>
```

Convert expiry from ISO date: `Math.round(new Date("2027-05-17T00:00:00Z").getTime() / 1000)`

Session cookies typically last about a year but can be invalidated earlier by password changes or suspicious activity.

## Recommendations on how to download

1. Ensure `.data/cookies.txt` exists with a valid session cookie.

2. Write a temporary config file (e.g., `/tmp/gallery-dl-config.json`):

```json
{
  "extractor": {
    "base-directory": "<output-dir>",
    "directory": [],
    "sleep-request": [8, 16],
    "sleep-429": 120,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..."
  }
}
```

3. Run:

```bash
gallery-dl \
  --config /tmp/gallery-dl-config.json \
  --no-mtime \
  --cookies .data/cookies.txt \
  "https://www.instagram.com/p/ABC123/"
```

4. Scan the output directory for new `.jpg`/`.png`/`.webp`/`.mp4` etc.

5. Clean up the temporary config file.

`gallery-dl` uses Instagram's internal API — not HTML scraping. It handles carousel posts (multiple images/videos) automatically.

## Config Settings

- `sleep-request: [8, 16]` — wait 8–16 seconds (random) between requests. **Do not reduce** — Instagram will 429 or invalidate the cookie.
- `sleep-429: 120` — wait 120 seconds on rate limit response.
- `directory: []` — download directly into base directory, no subdirectory nesting.
- `--no-mtime` — don't set file modification time to the post's publish date.

## Pitfalls

- **Rate limits are aggressive.** Do not reduce `sleep-request`. Instagram will 429 or soft-ban IPs making rapid requests.
- **Do not scrape HTML.** Instagram changes their frontend constantly. `gallery-dl` uses internal API and is actively maintained.
- **Stories are ephemeral.** Only fetchable while active (24h). Must be authenticated to view them.
- **Private accounts** require the session cookie to belong to an account that follows the target profile.
- **Keep gallery-dl updated.** `pip install -U gallery-dl` — fixes for Instagram API changes usually ship within days.
- **Output classification by extension.** Images: `.jpg`, `.png`, `.webp`, `.gif`. Videos: `.mp4`, `.webm`, `.mkv`, `.avi`, `.mov`.
