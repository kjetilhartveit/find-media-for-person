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

## Alternative download method - yt-dlp

`yt-dlp` also supports Twitter URLs as a quick single-post fallback with no auth.

### Prerequisites

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

## Pitfalls

- **Handle may not match display name.** Content creators use different names/handles on X/Twitter vs. display names shown on aggregator sites. Search for aliases found on other platforms. Try variations with underscores, periods, and different capitalizations.
- **API access tiers matter.** Free tier has very limited rate limits. Media lookup counts against read quota. Check X developer docs for current limits.
- **Video URLs are temporary.** The `variants[].url` values are signed URLs that expire. Download immediately; do not store URLs for later.
- **Raw JSON uses snake_case.** The raw API returns `media_key`, `preview_image_url`, `bit_rate`. The `@xdevplatform/xdk` SDK transforms to camelCase.
- **Articles have separate media.** X Articles use `coverMedia` and `mediaEntities` — separate from regular `attachments.media_keys`.
- **Thread fetching is expensive.** Uses separate (lower) rate-limited search API. Only fetch threads when explicitly needed.
