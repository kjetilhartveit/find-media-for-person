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

## Recommendations on how to download

1. Extract tweet ID from URL (regex: `/status/(\d+)`)

2. Call X API v2:

```
GET https://api.x.com/2/tweets/{id}
Authorization: Bearer $X_API_BEARER_TOKEN
```

Query params:

```
expansions=author_id,attachments.media_keys
media.fields=url,variants,type,preview_image_url,width,height,alt_text
tweet.fields=attachments,entities,note_tweet,created_at,lang
```

Full request payload:

```json
{
  "expansions": ["author_id", "attachments.media_keys", "referenced_tweets.id"],
  "media.fields": [
    "alt_text",
    "height",
    "media_key",
    "preview_image_url",
    "type",
    "url",
    "variants",
    "width"
  ],
  "tweet.fields": [
    "article",
    "attachments",
    "author_id",
    "conversation_id",
    "created_at",
    "entities",
    "in_reply_to_user_id",
    "lang",
    "note_tweet",
    "referenced_tweets"
  ]
}
```

3. Parse response:

   - **Photos** (`type: "photo"`): direct URL in `includes.media[].url`
   - **Videos** (`type: "video"`): multiple `variants[]` with different bitrates — filter to `video/mp4`, sort by `bitRate` descending, pick highest
   - **GIFs** (`type: "animated_gif"`): same variants structure as video

4. Download each media URL to the output directory.

### Video quality selection

```js
const mp4s = variants.filter((v) => v.contentType === "video/mp4" && v.url);
mp4s.sort((a, b) => (b.bitRate ?? 0) - (a.bitRate ?? 0));
return mp4s[0]?.url;
```

## Caching

Cache API responses as JSON files keyed by tweet ID (e.g., `.data/x-api-cache/{tweetId}.json`) to avoid redundant calls.

## Pitfalls

- **API access tiers matter.** Free tier has very limited rate limits. Media lookup counts against read quota. Check X developer docs for current limits.
- **Video URLs are temporary.** The `variants[].url` values are signed URLs that expire. Download immediately; do not store URLs for later.
- **Raw JSON uses snake_case.** The raw API returns `media_key`, `preview_image_url`, `bit_rate`. The `@xdevplatform/xdk` SDK transforms to camelCase.
- **Articles have separate media.** X Articles use `coverMedia` and `mediaEntities` — separate from regular `attachments.media_keys`.
- **Thread fetching is expensive.** Uses separate (lower) rate-limited search API. Only fetch threads when explicitly needed.
