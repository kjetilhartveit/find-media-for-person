---
name: find-media-from-x-twitter
description: Use when you need to find and download media from X/Twitter posts using gallery-dl (primary) with API v2 as fallback, or API v2 as primary if auth unavailable for gallery-dl.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Downloading images or videos from specific X/Twitter posts
- Scraping all media from a user profile (X/Twitter media timeline)
- Searching X/Twitter by query for media
- Extracting media from X/Twitter hashtags or timelines
- Need to fetch X/Twitter articles with embedded media

# Find media from X / Twitter

Download images and videos from X (Twitter) posts, user profiles, and timelines.

## URL Patterns

- **Posts**: `x.com/{user}/status/{id}` or `twitter.com/{user}/status/{id}`
- **Articles**: `x.com/{user}/article/{id}` — long-form X articles with embedded media
- **User profiles**: `x.com/{user}/media` — user's media-only timeline
- **Search**: `x.com/search?q={query}`
- **Hashtags**: `x.com/hashtag/{tag}`

## Primary download method — Download via gallery-dl

`gallery-dl` is the **preferred** method — no API key or bearer token required. Extractors: `TwitterTweetExtractor`, `TwitterUserExtractor`, `TwitterMediaExtractor`, `TwitterTimelineExtractor`, `TwitterHashtagExtractor`, `TwitterSearchExtractor`, `TwitterListExtractor`, and more.

## Fallback download method — X API v2 with bearer token

Use this when `gallery-dl` fails or when tweet metadata is needed. API access tiers matter — free tier has very limited rate limits.

## Alternative download method — yt-dlp

`yt-dlp` also supports Twitter URLs as a quick single-post fallback with no auth.

## Alternative download method — Aggregator sites (fallback when gallery-dl fails)

When `gallery-dl` fails (requires authenticated cookies), aggregator sites can provide media URLs directly.

### Using twpornstars.com

This site aggregates adult content creators' Twitter/X media into browsable pages.

1. **Find the creator's X handle** — search for their verified handle (e.g., @MayaBijouXXX)
2. **Browse their aggregated posts**: `https://www.twpornstars.com/{handle}` or `https://www.twpornstars.com/{handle}?page=N`
3. **Each post page at `/p/{post_id}` contains:**
   - **Redirect URL**: `/out.php?t={encoded_token}` — follows to actual tweet URL
   - **Video URL**: `https://video.twimg.com/ext_tw_video/{media_id}/pu/vid/{codec}/{resolution}/{filename}.mp4?tag=12` — direct from Twitter CDN
   - **Image URLs**: `https://pbs.twimg.com/media/{ID}.jpg:small` — thumbnail (use `:large` or `:med_url` instead of `:small`)
4. **To download:**
   - **Videos**: Follow `/out.php?t=...` redirect → get tweet URL and tweet ID → download video directly from `video.twimg.com/...`
   - **Images**: Extract `pbs.twimg.com/media/...` URL → convert `:small` to `:large` for better quality

### Python pattern for video extraction

```python
# From post page HTML
video_url = re.search(r'source[^>]*src="(https://video\.twimg\.com/[^"]+)"', html)
if video_url:
    full_url = video_url.group(0).replace('src="', '')

# Get tweet ID from redirect
out_match = re.search(r'/out\.php\?t=([a-zA-Z0-9_.=-]+)', html)
tweet_url = urlopen("https://www.twpornstars.com/out.php?t=%s" % out_match.group(1)).url
tweet_id = re.search(r'/status/(\d+)', tweet_url).group(1)

# Download video
video_path = "/path/to/video_%s.mp4" % tweet_id
download(full_url, video_path)
```

### Pitfalls for aggregator sites
- Pages may return HTTP 500 under load — retry with exponential backoff (3-5s between attempts)
- Video URLs in HTML are often already `:large` quality; don't double-convert
- Some post pages may be deleted (HTTP 404) — skip those gracefully
- Image posts may require gallery-dl (which itself needs auth for X/Twitter media)

## Pitfalls

- `X_API_BEARER_TOKEN` environment variable set
- Obtained from the X Developer Portal after creating a project and app

### Authentication

X uses the official API v2 with a bearer token (standard API key, no cookies or browser sessions). Store as env var `X_API_BEARER_TOKEN`.

### Video quality selection

```js
const mp4s = variants.filter((v) => v.contentType === "video/mp4" && v.url);
mp4s.sort((a, b) => (b.bitRate ?? 0) - (a.bitRate ?? 0));
return mp4s[0]?.url;
```

## Caching

Cache API responses as JSON files keyed by tweet ID (e.g., `.data/x-api-cache/{tweetId}.json`) to avoid redundant calls.

## Troubleshooting suspended handles

- **Adult content creators are frequently suspended.** If a known handle returns `NotFoundError: User is suspended`, try alternative handle variations. If all attempts fail, use X/Twitter **search** (`x.com/search?q=...`) as a reliable fallback — it finds media from all sources without requiring a specific profile URL.
- **Verify handles before bulk downloads.** When suggested URLs don't work, test a single URL first before running large batch downloads.
- **Searched results cross all sources.** Search finds tweets from multiple authors mentioning the person, not just the person's own tweets. Expect some non-author content mixed in.

## Pitfalls

- **gallery-dl needs auth cookies for X/Twitter timelines.** Without configured browser cookies, `gallery-dl` will return `AuthRequired` error for user timelines and search results. Use aggregator sites or direct tweet URLs as fallback.
- **Handle may not match display name.** Content creators use different names/handles on X/Twitter vs. display names shown on aggregator sites. Search for aliases found on other platforms. Try variations with underscores, periods, and different capitalizations.
- **API access tiers matter.** Free tier has very limited rate limits. Media lookup counts against read quota. Check X developer docs for current limits.
- **Video URLs are temporary.** The `variants[].url` values are signed URLs that expire. Download immediately; do not store URLs for later.
- **Raw JSON uses snake_case.** The raw API returns `media_key`, `preview_image_url`, `bit_rate`. The `@xdevplatform/xdk` SDK transforms to camelCase.
- **Articles have separate media.** X Articles use `coverMedia` and `mediaEntities` — separate from regular `attachments.media_keys`.
- **Thread fetching is expensive.** Uses separate (lower) rate-limited search API. Only fetch threads when explicitly needed.
