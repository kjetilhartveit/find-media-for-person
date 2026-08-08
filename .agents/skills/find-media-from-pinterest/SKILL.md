---
name: find-media-from-pinterest
description: Use when downloading media from Pinterest pins, boards, profiles, or search results. Gallery-dl is the primary method and works well for bulk downloading.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Searching for images of a specific person by name
- Downloading images from a Pinterest profile or board
- Extracting pins from Pinterest search results
- Bulk downloading from Pinterest

## URL Patterns

- **Profile**: `pinterest.com/{username}/`
- **Board**: `pinterest.com/{username}/{board-name}/`
- **Pin**: `pinterest.com/pin/{id}/`
- **Search**: `pinterest.com/search/pins/?q={query}`

## Primary download method — gallery-dl

```bash
# Search by name (most useful)
gallery-dl -d "./search-results" "https://www.pinterest.com/search/pins/?q=Halle+Hayes+nude"

# Specific profile
gallery-dl -d "./profile" "https://www.pinterest.com/username/"

# Specific board
gallery-dl -d "./board" "https://www.pinterest.com/username/board-name/"

# Single pin
gallery-dl -d "./pin" "https://www.pinterest.com/pin/12345/"
```

Extractors: `PinterestSearchExtractor`, `PinterestUserExtractor`, `PinterestBoardExtractor`, `PinterestPinExtractor`

## Recommendations

1. **Pinterest search is effective for discovering content** - Use queries like `{name} nude`, `{name} onlyfans`, `{name} photos`
2. **Search returns many pins** - Pinterest searches return a large number of results. Gallery-dl downloads ~200-300+ images per search query.
3. **Many pins are reposted content** - Pinterest contains lots of reposted/curated content from other sources (Instagram, OnlyFans, other adult sites).
4. **No authentication needed** - Gallery-dl works without cookies for public search/browsing.
5. **Good for bulk image collection** - Most effective source for large volumes of images.

## Pitfalls

- **Repost-heavy content** - Much of Pinterest is not original content. Pins link back to the original source (often Instagram, OnlyFans, or other sites).
- **No video downloads** - Pinterest video pins are often just GIFs or thumbnails. Actual video content is limited.
- **Bot detection** - Pinterest may block heavy scraping. Rate limiting helps avoid detection.
- **Image quality varies** - Quality depends on the original pin source. Some pins are compressed by Pinterest.
- **Pin expiration** - Pins may delete or become private over time. Download promptly.
- **No gallery-dl for videos** - Pinterest video support is limited in gallery-dl.
- **Account needed for full access** - Some content requires Pinterest login but search works well without auth.