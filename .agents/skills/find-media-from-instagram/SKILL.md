---
name: find-media-from-instagram
description: Use when you need to find and download media from Instagram posts, reels, stories, and profiles using gallery-dl (primary) with yt-dlp as fallback, both requiring cookie authentication.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Downloading posts, reels, or stories from a specific Instagram account
- Scraping all media from an Instagram profile
- Extracting media from a single Instagram post or reel URL
- Need to support carousel posts (multiple images/videos)

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
  -o "user-strategy=web_profile_info" \
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

**Important:** Use `-d <path>` to set the output directory. Do NOT use `-o "directory=..."` or `"directory": [...]` in the config. With `-d <path>`, gallery-dl still creates nested `instagram/username/` folders below the given path (e.g., `-d /tmp/output` → `/tmp/output/instagram/mstrattonx/`). To control the folder structure, use output template options instead:

```bash
# Flat structure with custom filename template
gallery-dl \
  --config /tmp/gallery-dl-config.json \
  --no-mtime \
  --cookies .data/cookies.txt \
  --range 1-250 \
  -d <output-dir> \
  --extractor-args instagram:filename="{username}/{title}{extension}" \
  "https://www.instagram.com/{username}/"
```

Alternative: download to a temp directory and organize manually:
```bash
mkdir -p <output-dir>/temp
gallery-dl --config /tmp/gallery-dl-config.json --no-mtime --cookies .data/cookies.txt --range 1-250 -d <output-dir>/temp "https://www.instagram.com/{username}/"
mv <output-dir>/temp/instagram/<username>/* <output-dir>/
rmdir <output-dir>/temp/instagram/<username> <output-dir>/temp/instagram
```

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

## Tagged Content Tips

- **Fan accounts** often have user-edited content, fan edits, and reposts. Common naming patterns: `<username>theestallion`, `50shadesof<username>`, `theestallionbr`.
- **Media/news accounts** (e.g., `revolt`, `uproxx`, `bet`, `essence`) often post multi-video articles with 8-12+ parts per post.
- **Brand collaborations**: Major brands sometimes tag influencers in their posts, which can yield exclusive or unique content.
- **Indian web series collaborators**: For Indian models/actresses, tagged content from web series production accounts (e.g., Cinema Dosti, Ullu, Kooku) provides valuable behind-the-scenes and BTS content. Check accounts of directors/producers who worked with the target.
- **Repost/reel accounts**: Accounts like `<topic>_reel_<number>` often repost content. They can yield additional angles and versions not on the original profile.
- **Carousels can be very large**: Some tagged media posts have 15+ image/video parts. A single `--range 1-250` pass may be consumed quickly by high-count carousels from accounts like `hhucitnews`, `revolt`, `adumboy`, `theonly.mommymaki`.

## Instagram-Specific Settings

- `sleep-request: [8, 16]` — wait 8–16 seconds between requests. **Do not reduce** — Instagram will 429 or invalidate the cookie.
- `sleep-429: 120` — wait 120 seconds on rate limit response.

## Time Budget — Always Wrap Up

**Never wait hours on an Instagram download.** Instagram rate limits (429s, empty responses, redirect-to-home) can make gallery-dl crawl or stall for a very long time. Enforce a hard time budget:

- Set a bash timeout of **900000ms (15 min) max per gallery-dl invocation**. If a download is that big, split it into multiple smaller `--range` runs.
- **Max two attempts** per profile/URL. If gallery-dl fails, returns 401/429s repeatedly, or downloads almost nothing after two tries, **stop and wrap up**: record what was downloaded (possibly nothing), note the failure reason, and move on to other sources.
- If rate-limit waits (`sleep-429`) accumulate for more than ~10 minutes total in one attempt, abort the attempt early.
- A stalled run (no progress for ~10 min) should be killed (`pkill -f gallery-dl` for the specific run) and treated as a failed attempt — do not restart it a third time.
- Report the outcome (0 files / partial / full) with failure reason so the orchestrator can plan follow-up (e.g., fresh cookies, different IP) instead of silently blocking the whole run.

## Common Account Name Changes

Celebrity and public figure accounts frequently change handles. Search news sources to find the current handle:

- **Name simplification**: e.g., `@meghanmarkle` → removed → `@meghan` (Jan 2025 return)
- **Brand rebranding**: e.g., `@americanrivieraorchard` → `@aseverofficial`
- **Official accounts discontinued**: e.g., `@sussexroyal` (stopped 2020) — still exists but has no new posts
- **Old personal accounts deleted**: Old handles become available and may be re-registered
- **Account deactivated, new account created**: Some creators deactivate old accounts and start fresh with a new handle. Old accounts may remain visible but with no posts. Example: `@melissastratton` was deactivated in 2024, replaced by `@mstrattonx` as the active account. Check both accounts when searching.

When searching for media of a person, verify the current Instagram handle via web search, as the old one may no longer exist or may return NotFoundError.

## Diagnosing "NotFoundError: Requested user could not be found"

When gallery-dl fails with `[instagram][error] NotFoundError: Requested user could not be found`, the problem is NOT always the cookie. This error can be caused by the **default user-resolution strategy** failing even for fully valid accounts, so first rule that out:

- The default `user-strategy` is `search,web` — the `topsearch` endpoint frequently returns `{"message":"Server Error"}`, and the HTML-page strategy (`web`) hits the login wall, so both fail and gallery-dl (wrongly) concludes the user doesn't exist. Fix: pass `-o "user-strategy=web_profile_info"`, which uses `/api/v1/users/web_profile_info/?username=...` — the same endpoint as the curl control check. If the control check succeeds but gallery-dl says NotFoundError, this is almost always the cause.

Beyond that, the error also occurs when the **target account** is disabled, banned, deleted, or age-gated by Instagram. To distinguish:

1. Check whether the session cookie still works by querying a control account with the same request:

```bash
curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..." \
  -H "x-ig-app-id: 936619743392459" \
  "https://www.instagram.com/api/v1/users/web_profile_info/?username=nasa" \
  -b .data/cookies.txt
```

   - Control resolves (returns `data.user` with username/followers) + target returns `data.user: null` → the **target account is unavailable** (disabled/deleted/renamed), not an auth problem. Document this and move on.
   - Control also returns `data.user: null` or no JSON → the cookie/session is invalid or the IP is rate-limited; refresh the cookie.

2. Rate-limit the diagnostic queries: a burst of quick `web_profile_info` calls triggers Instagram to return **empty (non-JSON) responses** for a while. Space checks at least ~20–30 s apart and pause a few minutes before retrying.

3. HTML profile pages are NOT useful for this diagnosis — profile pages (and old post URLs of a disabled account) 302-redirect to the homepage in both normal login-wall situations and disabled-account situations. Rely on the API check above.

4. Before concluding, rule out a handle rename:
   - Check the person's own link-in-bio hub (link.me, linktr.ee, beacons, etc.) — it usually links the current profile.
   - Web-search for the person's current handle (SEO bio sites and stats trackers like hafi.pro/socialveins show last known follower data; a stale "active" claim there may just be uncached data).
   - Check handle variants (no suffix, underscores, "official" suffix, period placement). A squatter account with the "expected" handle but few hundred followers is not the real person.

## Pitfalls

- **Handle may not match display name.** Content creators use different names/handles on Instagram vs. display names shown on aggregator sites. Search for aliases found on other platforms. Try variations with underscores, periods, and different capitalizations.
- **Rate limits are aggressive.** Do not reduce `sleep-request`. Instagram will 429 or soft-ban IPs making rapid requests.
- **Immediate repeated 429s mean the session/IP is already throttled.** If every request 429s right after start (0 files persisted) despite conservative sleeps, the cookie/IP is likely in an active throttle window — e.g. from other concurrent/recent Instagram downloads sharing the same cookie or IP, or from bursts of diagnostic `web_profile_info` calls. `sleep-429` is far too short to clear it. A cooldown of several minutes (5–10+) is often needed. With a strict time budget, prefer waiting before a retry over burning all allowed attempts within minutes on guaranteed-429 requests.
- **Do not scrape HTML.** Instagram changes their frontend constantly. `gallery-dl` uses internal API and is actively maintained.
- **Stories are ephemeral.** Only fetchable while active (24h). Must be authenticated to view them.
- **Private accounts** require the session cookie to belong to an account that follows the target profile.
- **Output classification by extension.** Images: `.jpg`, `.png`, `.webp`, `.gif`. Videos: `.mp4`, `.webm`, `.mkv`, `.avi`, `.mov`.
- **Long downloads need long timeouts.** A full profile download can take 10+ minutes. Set bash timeout to at least `900000`ms (15 min).
- **`--range` counts individual media, not posts.** A carousel with 3–10 images counts each image separately. `--range 1-1000` on a profile with many carousels can yield 2000–2500+ files. Use `--range 1-250` for a reasonable number of posts. Avoid exceeding 2–3 GB total.
- **`-o "directory=..."` bug.** Setting `-o "directory=[instagram]"` splits each character of "instagram" into a separate nested folder (`[/i/n/s/t/a/g/r/a/m/]`). Always use `-d <path>` to set the output directory instead.
- **YouTube-dl/ytdl fallback for videos.** When direct Instagram video URLs fail, gallery-dl tries yt-dlp as fallback. If yt-dlp/youtube-dl is not installed, the fallback errors with `[downloader.ytdl][error] Cannot import yt-dlp or youtube-dl` and the video is not downloaded. Install yt-dlp for complete video coverage.
- **`highlights` may return "No results".** Some profiles don't have public story highlights. The output message `No results for .../highlights/` is normal and not an error.
- **Session cookie may expire during long downloads.** Profile downloads can take 10+ minutes, and the session cookie may expire mid-download. Look for `[instagram][error] HTTP redirect to home page` in the output — this indicates the cookie expired. If you see this, refresh the cookie and re-run gallery-dl (it will skip already downloaded files).
- **Tagged posts create subdirectories with other accounts.** Using `-o include=posts` also fetches posts where the user appears (fan accounts, tagged posts, etc.). These are saved in `instagram/<other_account>/` subdirectories. After download, extract the target's files: `mv /output/instagram/<username>/* /output/` and remove empty subdirs. Content from non-target accounts (especially videos needing yt-dlp) may fail or be empty.
- **yt-dlp must be installed for reliable video downloads.** Videos without direct MP4 URLs require yt-dlp. Without it, videos silently fail with `[downloader.ytdl][error] Cannot import yt-dlp or youtube-dl`. Install with `pip install yt-dlp` or equivalent. Verify with `yt-dlp --version`.
- **Adult content creators' accounts are frequently disabled or age-gated.** For adult creators, "Requested user could not be found" is much more common than for mainstream creators, even for very large accounts. See the diagnosis section above; when confirmed unavailable, note exactly what was and was not resolvable and pursue other sources (aggregators, other platforms) instead of retrying the profile.
