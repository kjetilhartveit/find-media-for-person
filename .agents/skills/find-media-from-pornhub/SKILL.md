---
name: find-media-from-pornhub
description: Use when downloading media from Pornhub profiles, galleries, albums, or searching for specific pornstar content.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Downloading image galleries from Pornhub profiles
- Searching for specific pornstar content
- Scraping PornHub albums/galleries

# Find media from Pornhub

PornHub profile, gallery, album, and video page URLs.

## URL Patterns

- **Profile**: `pornhub.com/pornstar/{name}` or `pornhub.com/pornstar/{name}/videos`
- **Album**: `pornhub.com/album/{id}`
- **Photo gallery**: `pornhub.com/album/viewphotos?albumId={id}`
- **Single video**: `pornhub.com/view_video.php?viewkey={phXXXXX}`
- **Search**: `pornhub.com/video/search?search={query}`

## Primary method — gallery-dl (for images)

Extractors: `PornhubPhotosExtractor`, `PornhubGalleryExtractor`

## Alternative method — yt-dlp (for videos)

```bash
# Single video (requires browser impersonation)
yt-dlp -o "%(title)s.%(ext)s" -f "best" "https://www.pornhub.com/view_video.php?viewkey=ph632a2ba4c7c09"

# Profile pages
yt-dlp -o "%(title)s.%(ext)s" "https://www.pornhub.com/pornstar/halle-hayes"
```

**Requires**: playwright browser impersonation (`impersonate:browser=chrome`) for video downloads to work.

## Cloudscraper method — extracting image URLs

```bash
# Get profile page
curl -sL -H "User-Agent: Mozilla/5.0" \
  "https://www.pornhub.com/model/halle-hayes/photos" | \
  grep -oP 'https://ei\.phncdn\.com/[^"'"'"']+\.(jpg|png)[^"'"'"']*'
```

## Recommendations

1. Use gallery-dl for album/gallery images - reliable and straightforward
2. yt-dlp for videos needs browser impersonation - may not work in headless environments
3. Cloudscraper/curl works for profile pages but CDN URLs may expire or be blocked without proper cookies
4. Video URLs require session cookies from the main PornHar site - download in sequence after profile fetch
5. Images in galleries are typically high-res (1080p+)
6. Gallery images can be downloaded without authentication

## Pitfalls

- **Video downloads fail** - PornHub CDN (phncdn.com) returns HTTP 470/403 without proper session cookies. yt-dlp tries impersonation but fails if no browser is available.
- **Pagination** - Profile pages show limited thumbnails. Use direct gallery URLs for full albums.
- **URL format** - Gallery URLs use albumId parameter: `https://www.pornhub.com/album/viewphotos?albumId=XXX`
- **Cloudscraper works but CDN is protected** - Basic page fetching works, but direct CDN links need cookies
- **Video stream URLs** - HLS playlists (m3u8) and segmented MP4s require proper decryption tokens
- **No gallery-dl for videos** - Only supports image galleries, not full videos
