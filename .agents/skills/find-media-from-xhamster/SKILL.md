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

XHamster is an SPA, but much useful data is embedded in the initial HTML as escaped JSON. Standard HTTP requests (requests/urllib) can extract significant data without browser automation.

## URL Patterns

- **Profile**: `xhamster.com/pornstars/{name}`
- **Search**: `xhamster.com/search/{name}`
- **Gallery**: `xhamster.com/photos/gallery/{id}`
- **User galleries**: `xhamster.com/users/{handle}/photos`
- **User videos**: `xhamster.com/users/{handle}/videos`
- **Single video**: `xhamster.com/videos/{slug}-{id}`
- **Shorts**: `xhamster.com/shorts/{slug}-{id}`

## Method 1 — Embed JSON from profile page (best for video lists)

Request `https://xhamster.com/pornstars/{name}` with a normal User-Agent. The response HTML is large (~300KB) and contains:

- `<title>` and `<meta name="description">` page info
- Profile avatar in CSS: `landing-info__logo-image` with `background-image: url('...')`
- `videoListProps` — contains `pageInfo.videoCount` and `videoThumbProps` array with all videos listed on that page
  - Each item has: `id`, `title`, `pageURL`, `views`, `thumbURL`, `imageURL`, `imageURLWithPrefix`, `trailerURL`, `contentRating`, `dateCreatedObj`, `imageWidth`, `imageHeight`
  - Note: Profile page may list fewer videos than `pageInfo.videoCount` — only the first page of videos appears here
- `momentsListComponent` — contains `videoThumbProps` (short videos/clips)

To extract: parse the HTML for `"videoThumbProps"`, find the opening `[`, count brackets to find end of array, then `.decode('unicode_escape')` on the raw JSON string (all slashes are escaped) and `json.loads()`. For profiles, there are 2 arrays — the first is usually short videos (moments), the second is the main video list. Filter items by checking if the person's name appears in `title` or `pageURL`.

Thumbnail URLs are at `https://ic-vt-nss.xhcdn.com/` with quality suffixes like `s(w:1280,h:720),webp` and paths like `/005/748/041/v2/2560x1440.268.webp`. These directly downloaded thumbnails return 403 Hotlink Forbidden — use individual video page og:image instead, or fetch with a Referer header.

## YouTube-dl download (videos)

Videos are served via HLS (m3u8). Use:
```bash
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -o "output.mp4" "https://xhamster.com/videos/{slug}-{id}"
```

Best quality is 1080p MP4. Videos average 170-200MB but some reach 600-800MB+. yt-dlp automatically applies `FixupM3u8` to fix MPEG-TS in MP4 containers. Each download takes roughly 2-5 minutes at typical bandwidth.

## Technical Tips

- Use User-Agent: `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36`
- Video thumbnails: `https://ic-vt-nss.xhcdn.com/` (with proper Referer)
- Photo images: `https://ic-ph-nss.xhcdn.com/`
- Avatar/profile images: `https://ic-tt-nss.xhcdn.com/`
- Short video trailers: `https://thumb-v*.xhcdn.com/`
- JSON in HTML uses `\/` not `/` — must `.decode('unicode_escape')` before `json.loads()`
- The `imageURL` field often has higher resolution than `thumbURL`
- Profile pornstar pages often link to user channels (e.g., "Thai Swinger") that host the same content under a different uploader

## Method 2 — Search page (broader discovery)

Request `https://xhamster.com/search/{name}` with normal User-Agent. Contains:

- `videoThumbProps` array in embedded JSON (~47 videos per page, paginated)
- Separate smaller array for "Related/Relevant Short videos"
- Direct HTML links to videos and galleries in the results grid

Search results are paginated (up to 22+ pages for popular stars). Each page returns ~47 videos. Compare video IDs against the profile list to find extras not covered by the profile page. Search results may include videos where the model is featured but not the main pornstar page title.

## Method 3 — Individual video pages (best thumbnails)

Request `https://xhamster.com/videos/{slug}-{id}` for each video. The `og:image` meta tag contains a high-quality thumbnail (1280x720 or 2560x1440 webp). Extract with:

```python
og_match = re.search(r'<meta[^>]*property=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html)
thumb_url = urllib.parse.unquote(og_match.group(1)) if og_match else None
```

The og:image URL points to ic-vt-nss.xhcdn.com and returns the best available quality thumbnail.

## Method 4 — Photo galleries

Request `https://xhamster.com/photos/gallery/{id}`. Images are served from `https://ic-ph-nss.xhcdn.com/` with URLs like:
```
https://ic-ph-nss.xhcdn.com/a/{hash}/webp/000/517/456/852_1000.
```

Filter out 32x32 tiny thumbnails. Look for URLs containing `1000`, `852`, `1280` which indicate full-size photos.

Methods 1-4 work with plain `requests` — no browser automation needed for thumbnails and metadata. Use browser automation only for downloading full videos.

## Methods That Fail

- **gallery-dl**: No `pornstars` extractor. Has `XhamsterGalleryExtractor` and `XhamsterUserExtractor` only. Does not support `/videos/` pages for this purpose.
- **yt-dlp**: Returns "Unsupported URL" for `/pornstars/` and `/users/` pages (returns 0 videos). Only works for `/videos/{slug}-{id}` pages via the `XHamster` extractor.

## Pitfalls

- **JSON escaping**: Embedded JSON in HTML has all `/` escaped as `\/` — must unescape before parsing
- **Limited video list on profile**: The `videoListProps` array on the main profile page only includes the first page of videos (typically ~46 of 50+ total). Search page discovery finds additional videos not in the profile list
- **Thumbnail hotlink protection**: Thumbnail URLs from profile JSON (`imageURL`, `thumbURL`) return 403 when fetched directly without proper Referer headers. Extract high-quality thumbnails from individual video pages via `og:image` meta tag, or download them along with videos
- **Pagination**: Search results have many pages (e.g., 22+ pages). Use video IDs for deduplication across pages
- **Placeholder thumbnails**: Some pages return xhamster's generic placeholder image as og:image — verify the thumbnail URL contains the person's name