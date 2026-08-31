---
name: find-media-from-xasiat
description: Use when you need to find and download media from Xasiat (xasiat.com), an aggregator of leaked adult content, particularly Asian models.
---

# When to use this skill

- Downloading leaked videos from Xasiat (xasiat.com) featuring specific models/pornstars
- Searching for content by model name on Xasiat
- Scraping Xasiat album pages (images) using gallery-dl
- Downloading video files using curl_cffi directly

# Find media from Xasiat (xasiat.com)

Xasiat is an aggregator of leaked adult content, particularly Asian models (Thai, Chinese, Japanese, Korean). Content is organized by model and album. **Non-Asian adult performers (pornstars) may also appear** if they are known in the industry. Search results for non-adult Western celebrities typically return empty results.

## URL Patterns

- **Model search**: `https://www.xasiat.com/search/QUERY/` (use model name variations)
- **Video page**: `https://www.xasiat.com/videos/VIDEO_ID/TITLE/`
- **Album page**: `https://www.xasiat.com/albums/ALBUM_ID/TITLE/`
- **Tags**: `https://www.xasiat.com/tags/TAG_NAME/`
- **Categories**: `https://www.xasiat.com/categories/CATEGORY/`

**Note**: Model profile pages (`/albums/models/MODEL/`) return 403/404 and are not usable.

## Model page discovery

Model profiles at `/albums/models/MODEL/` return 403/404. Use search instead. Search results are rendered in async blocks with section headings. Video URLs follow the pattern `/videos/NUMBER/TITLE/`.

Videos on the search page may include both the target model's content AND related/recommended videos. **Verify each video** by checking the title and description for the model's name. Videos without the model's name in the title/description may be from a different model entirely.

## Extractors

### gallery-dl

- **XasiatSearchExtractor**: `https://www.xasiat.com/search/QUERY/`
  - Uses the async block endpoint at `?mode=async&function=get_block&block_id=list_albums_albums_list_search_result`.
  - **May return 403/404** for certain queries (e.g., Western models like "Amia Miley"). The HTML search page renders correctly but the async API fails.
  - **Fallback**: When gallery-dl fails, scrape the HTML search page directly with `curl` and grep for `/videos/` and `/albums/` links.
  - Note: Returns ALL content matching the query - filter results for the target model.
- **XasiatAlbumExtractor**: `https://www.xasiat.com/albums/ALBUM_ID/TITLE/`
  - Downloads album images. Works with `i-acctoken` authentication.
- **Model profiles are NOT supported**: The `/albums/models/MODEL/` URL pattern returns 403/404. Model profiles do not exist on Xasiat.

### yt-dlp (does NOT work for video downloads)

yt-dlp falls back to the generic extractor and fails due to the KVS player engine version mismatch. The player engine on Xasiat uses an untested major version which prevents format extraction. **Do not use yt-dlp for Xasiat video downloads**.

### gallery-dl does NOT support individual video URLs

The `XasiatSearchExtractor` and `XasiatAlbumExtractor` work for search results and albums (downloading images). However, individual video URLs like `/videos/12345/` are not supported by gallery-dl.

### Scraping search pages when gallery-dl fails

When gallery-dl's search extractor returns 403/404, the HTML search page may still contain results. Use `curl` + grep:

```bash
# Get all video links from search page
curl -s "https://www.xasiat.com/search/QUERY/" | grep -oP 'href="https://www\.xasiat\.com/videos/\d+/[^"]+"' | sort -u

# Get all album links from search page  
curl -s "https://www.xasiat.com/search/QUERY/" | grep -oP 'href="https://www\.xasiat\.com/albums/\d+/[^"]+"' | sort -u
```

Then verify each match by checking the video/album title contains the model name. Check the video page via its HTML title tag to confirm it features the target model.

## Searching and verification

When searching, filter results by checking:
1. Video/album title contains the exact model name
2. Description matches (avoids misidentified models)

Search for name variations (e.g., hyphenated vs underscored). Always verify by checking titles before downloading.

## Important caveats

- **Non-Asian/adult-model searches may return results**: While Xasiat primarily covers Asian performers, adult performers (pornstars) of any ethnicity may appear. Western adult models/pornstars (e.g., Maya Bijou) CAN have content if they are known in the industry.
- **Name-based false positives**: Searching for a celebrity name (e.g. "Tyla") may return no results, while searching a variant (e.g. "Tyla chanteuse" = "Tyla singer" in French) may return videos of an adult performer who looks like or resembles the celebrity — NOT the actual celebrity. Always verify content by checking titles, descriptions, and video previews.
- **Search results contain many false positives**: Search queries often return content from multiple models with similar names. Always filter by exact model name matches.
- **Both videos and albums may return empty**: The async endpoints return `There is no data in this list.` when no content matches, for both video and album searches.
- **Model profile pages return 403/404**: The `/albums/models/MODEL/` format does not work for model profiles. They return 403 (Forbidden) or 404. Only search URLs and individual video/album pages are accessible.
- **Some adult performers simply have no content on Xasiat**: E.g., "Megan Vale" returned 404 for async endpoint with no content. Always try the search first before assuming the model is absent.

## Thumbnails and preview

Video previews are available at:
`https://www.xasiat.com/get_file/CATEGORY/HASH/DIRECTORY/VIDEO_ID/VIDEO_ID_preview.mp4/`

Example: `https://www.xasiat.com/get_file/10/376a31b278f571abb79944f5dc25f089/14000/14444/14444_preview.mp4/`

## Downloading videos

Direct download URLs require browser fingerprinting (Cloudflare protection). Use `curl_cffi` in Python:

```python
from curl_cffi import requests as cffi_requests
import re
import os

s = cffi_requests.Session(impersonate='chrome')
resp = s.get('https://www.xasiat.com/videos/VIDEO_ID/TITLE/')

# Extract video URL from flashvars (best quality)
alt_match = re.search(r'video_alt_url:\s*["\x27]([^"\x27\r\n]+)["\x27]', resp.text)
# Or SD quality:
sd_match = re.search(r'video_url:\s*["\x27]([^"\x27\r\n]+)["\x27]', resp.text)

vurl = alt_match.group(1) if alt_match else sd_match.group(1)

# Support resume for interrupted downloads
out_path = 'output.mp4'
current_size = os.path.getsize(out_path) if os.path.exists(out_path) else 0

headers = {}
if current_size > 0:
    headers['Range'] = f'bytes={current_size}-'
    mode = 'ab'
else:
    mode = 'wb'

vresp = s.get(vurl, stream=True, timeout=600, headers=headers)
if vresp.status_code == 206:
    print("Resumed download")
elif vresp.status_code == 200:
    current_size = 0  # Fresh download

with open(out_path, mode) as f:
    for chunk in vresp.iter_content(chunk_size=65536):
        f.write(chunk)
```

The video download URL has the format:
`https://www.xasiat.com/get_file/CATEGORY/HASH/60000/VIDEO_ID/VIDEO_ID_source.mp4/?v-acctoken=TOKEN`

Or SD:
`https://www.xasiat.com/get_file/CATEGORY/HASH/60000/VIDEO_ID/VIDEO_ID.mp4/?v-acctoken=TOKEN`

## Tags commonly associated with Asian models

Teen, Thai, Chinese, Japanese, Hardcore, Creampie, Anal, Blowjob, POV, Homemade, Babes, Big Tits, Asian, Brunette, Girlfriend, Solo, Small Tits, Sl
