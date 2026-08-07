---
name: find-media-from-instagram
description: Download media from Instagram posts, reels, stories, and profile using gallery-dl (primary) with yt-dlp as fallback, both requiring cookie authentication.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# Find media from Instagram

Download images and videos from Instagram using `gallery-dl` (see respective skill if exists).

## URL Patterns

- **Profile**: `instagram.com/{username}/` — all posts on a profile
- **Posts**: `instagram.com/p/{shortcode}` — images, carousels, or video posts
- **Reels**: `instagram.com/reel/{shortcode}` — short-form video
- **Stories**: `instagram.com/stories/{username}/{id}` — ephemeral content (24h only, must be active)

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

**Primary method: gallery-dl**. gallery-dl is the preferred tool — it has 18+ Instagram extractors (posts, reels, stories, user profile, tags, etc.) and uses Instagram's internal API. gallery-dl handles carousel posts automatically.

**Fallback: yt-dlp**. If gallery-dl fails, `yt-dlp` can also download individual posts/reels. It does not support profile scraping or stories, only single media URLs.

1. Ensure `.data/cookies.txt` exists with a valid session cookie.

2. Write a temporary config file (e.g., `/tmp/gallery-dl-config.json`):

```json
{
  "extractor": {
    "sleep-request": [8, 16],
    "sleep-429": 120,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..."
  }
}
```

3. Always use `--range 1-250` to limit downloads (see pitfall about carousels). Run with appropriate timeout (profile downloads can take 10+ minutes):

```bash
# Create output directory first
mkdir -p <output-dir>/instagram

# Profile — download recent posts, reels, and highlights
gallery-dl \
  --config /tmp/gallery-dl-config.json \
  --no-mtime \
  --cookies .data/cookies.txt \
  --range 1-250 \
  -d <output-dir>/instagram \
  -o "include=posts,reels,highlights" \
  "${timeout: 900000}" \
  "https://www.instagram.com/{username}/"

# Single post
gallery-dl \
  --config /tmp/gallery-dl-config.json \
  --no-mtime \
  --cookies .data/cookies.txt \
  -d <output-dir> \
  "https://www.instagram.com/p/ABC123/"

# Specific reel
gallery-dl \
  --config /tmp/gallery-dl-config.json \
  --no-mtime \
  --cookies .data/cookies.txt \
  -d <output-dir> \
  "https://www.instagram.com/reel/ABC123/"
```

**Important:** Use `-d <path>` to set the output directory. Do NOT use `-o "directory=..."` or `"directory": [...]` in the config — gallery-dl creates nested folders per site/user by default, and `-d` is the reliable way to override this. If you need a subfolder per source, create it first (`mkdir -p <output-dir>/instagram`) and point `-d` there.

4. Verify results:

```bash
find <output-dir>/instagram -type f | wc -l
du -sh <output-dir>/instagram
```

5. Clean up the temporary config file.

`gallery-dl` uses Instagram's internal API — not HTML scraping. It handles carousel posts (multiple images/videos) automatically.

## Include Options

Use `-o "include=..."` to control what content types are downloaded from a profile:

- `posts` (default) — regular feed posts only
- `reels` — short-form video clips
- `highlights` — story highlights (permanent saved stories)
- `tagged` — posts where the user is tagged
- `photos` — photo posts only (excludes video-only posts)
- `stories` — active 24h stories
- `all` — everything available

```bash
-o "include=posts,reels,highlights"
-o "include=all"
```

## Instagram-Specific Settings

- `sleep-request: [8, 16]` — wait 8–16 seconds between requests. **Do not reduce** — Instagram will 429 or invalidate the cookie.
- `sleep-429: 120` — wait 120 seconds on rate limit response.

## Pitfalls

- **Rate limits are aggressive.** Do not reduce `sleep-request`. Instagram will 429 or soft-ban IPs making rapid requests.
- **Do not scrape HTML.** Instagram changes their frontend constantly. `gallery-dl` uses internal API and is actively maintained.
- **Stories are ephemeral.** Only fetchable while active (24h). Must be authenticated to view them.
- **Private accounts** require the session cookie to belong to an account that follows the target profile.
- **Output classification by extension.** Images: `.jpg`, `.png`, `.webp`, `.gif`. Videos: `.mp4`, `.webm`, `.mkv`, `.avi`, `.mov`.
- **Long downloads need long timeouts.** A full profile download can take 10+ minutes. Set bash timeout to at least `900000`ms (15 min).
- **`--range` counts individual media, not posts.** A carousel with 3–10 images counts each image separately. `--range 1-1000` on a profile with many carousels can yield 2000–2500+ files. Use `--range 1-250` for a reasonable number of posts. Avoid exceeding 2–3 GB total.
- **`-o "directory=..."` bug.** Setting `-o "directory=[instagram]"` splits each character of "instagram" into a separate nested folder (`[/i/n/s/t/a/g/r/a/m/]`). Always use `-d <path>` to set the output directory instead.
