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
- **Model profile**: `pornhub.com/model/{name}` - may have additional galleries/albums not shown on pornstar page
- **Photos page (own albums)**: `pornhub.com/pornstar/{name}/photos` (title "{Name} Porn Pics & Nude Photos") - has a **"{Name}'s Photo Albums"** section with "Showing 1-N of N albums" counter; "See All" URL: `pornhub.com/pornstar/{name}/photos/public`
- **GIFs page**: `pornhub.com/pornstar/{name}/gifs` - "GIFs From {Name} Videos" section, paginated
- **Album**: `pornhub.com/album/{id}`
- **Photo gallery**: `pornhub.com/album/viewphotos?albumId={id}`
- **Single video**: `pornhub.com/view_video.php?viewkey={phXXXXX}`
- **Search**: `pornhub.com/video/search?searchterm={query}` (newer format; older `view_video.php?searchkey=` still works but may return unrelated results)
- **Playlists**: `pornhub.com/pornstar/{name}/videos?o=mr&page=N` - pagination for model pages
- **Video search with most viewed**: `pornhub.com/video/search?search=melissa+stratton&o=mv` - most viewed first

## Primary method — gallery-dl (for images)

Extractors: `PornhubPhotosExtractor`, `PornhubGalleryExtractor`

Works reliably on album URLs (verified):

```bash
# List URLs only
gallery-dl --get-urls "https://www.pornhub.com/album/{id}"

# Download (custom filename; {extension} does NOT include the leading dot)
gallery-dl --directory "$DST/albums/{id} {title}" \
  -o 'filename="{num:03d}.{extension}"' "https://www.pornhub.com/album/{id}"
```

Note: the option is `-o 'filename=...'` (there is no `--filename-fmt` flag).

## Alternative method — yt-dlp (for videos)

```bash
# Single video with Chrome impersonation (install curl_cffi first)
yt-dlp -f "best[height<=720]" --impersonate "Chrome-131:Android-14" \
  --no-playlist -o "%(title)s.%(ext)s" \
  "https://www.pornhub.com/view_video.php?viewkey=ph632a2ba4c7c09"

# Profile pages (may return 410 for retired models)
yt-dlp -f "best[height<=720]" --impersonate "Chrome-131:Android-14" \
  "https://www.pornhub.com/pornstar/halle-hayes"
```

**Note on viewkey format**: The `data-video-vkey` HTML attribute contains raw hex (e.g., `6a72006dce335`). When using yt-dlp URL directly from this value, use it as-is (no `ph` prefix). Some search result links may include a `ph` prefix in the href — always strip it. Example of working URL: `view_video.php?viewkey=6a72006dce335` (not `ph6a72006dce335`).

**Prerequisite**: Install `curl_cffi` for `--impersonate` to work (`pip install curl_cffi`).
Verify available targets: `yt-dlp --list-impersonate-targets`.

**Search URL format**: Use `pornhub.com/video/search?search={query}` - the modern `/visual/search` endpoint may return 404.

### Fallback: Extract HLS URLs from HTML and download

When yt-dlp fails but the video page returns HTML, extract the HLS URL directly:

```bash
# 1. Get the video page HTML (use raw hex for viewkey, NO 'ph' prefix)
curl -sL "https://www.pornhub.com/view_video.php?viewkey=XXXXXXXX" \
  -H "User-Agent: Mozilla/5.0" > page.html

# 2. Extract the default quality HLS URL (use Python to unescape JSON)
python3 -c "
import re, json
page = open('page.html').read()
m = re.search(r'defaultQuality[^}]*\"videoUrl\":\"([^\"]+)\"', page)
if m:
    url = m.group(1)
    url = json.loads('\"' + url + '\"')
    print(url)
"

# 3. Download with yt-dlp using the extracted HLS URL
yt-dlp --referer "https://www.pornhub.com/" \
  --user-agent "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
  -o "video.%(ext)s" "https://hv-h.phncdn.com/hls/videos/.../master.m3u8?..."
```

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
7. Use `pornstar/{name}/videos` with pagination (=page=N) to enumerate all tagged videos for a pornstar
8. Each profile page shows 47 videos (mix of recommended/premium + tagged videos)

## HTML scraping - extracting video URLs from pornstar profile pages

When you need to extract video URLs from a pornstar profile page (for paginated scraping):

```bash
# 1. Download profile page
curl -sL "https://www.pornhub.com/pornstar/{name}/videos" \
  -H "User-Agent: Mozilla/5.0" > profile.html

# 2. Extract all video data attributes with Python
python3 -c "
import re, sys
html = sys.stdin.read()

# Video items are in <li class='pcVideoListItem...> blocks
blocks = re.findall(r'<li[^>]*class=\"pcVideoListItem[^\"]*\"[^>]*>.*?</li>', html, re.DOTALL)

for block in blocks:
    vkey = re.search(r'data-video-vkey=\"([0-9a-f]+)\"', block)
    vkey = vkey.group(1) if vkey else None
    
    # Title extraction
    title_m = re.search(r'title=\"([^\"]+)\" class=\"thumbnailTitle', block)
    if not title_m:
        title_m = re.search(r'alt=\"([^\"]+)\"', block)
    title = re.sub(r'<[^>]+>', '', title_m.group(1) if title_m else 'N/A')
    # Clean HTML entities
    title = title.replace('&#39;', \"'\").replace('&amp;', '&').replace('&quot;', '\"')
    
    # Duration
    dur = re.search(r'>(\d+:\d+)<', block)
    
    # URL link
    link = re.search(r'href=\"/view_video\.php\?viewkey=([a-f0-9]+)', block)
    
    if vkey and title:
        print(f'{vkey}|{title}|{dur.group(1) if dur else ""}|view_video.php?viewkey={link.group(1) if link else ""}')
" < profile.html
```

Note: Video keys in `data-video-vkey` attribute are pure hex strings WITHOUT the "ph" prefix (unlike viewkey URL parameters which sometimes include "ph" prefix). Also extract from `href="/view_video.php?viewkey=VALUE"` which also lacks the "ph" prefix for some videos. Filter by title containing the performer's name to distinguish tagged videos from recommended/premium content.

## Video download with yt-dlp + cookies (recommended fallback)

When yt-dlp impersonation fails or is unavailable, use cookie-based downloads:

```bash
# 1. Get cookies first (from homepage or video page)
curl -sLb cookies.txt -c cookies.txt "https://www.pornhub.com/" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" -o /dev/null

# 2. Download video with cookies
yt-dlp --cookies cookies.txt \
  -f "bestvideo[height<=480]+bestaudio/best[height<=480]" \
  --no-playlist \
  -o "%(title)s.%(ext)s" \
  "https://www.pornhub.com/view_video.php?viewkey=XXXXXXXX"
```

**This method was verified working reliably in headless/remote environments.** It avoids the need for `curl_cffi` browser impersonation. Speed for 480p is typically 2-3MB/s. Videos average 100-400MB at 480p quality.

## Pitfalls

- **Video downloads fail** - PornHub CDN (phncdn.com) returns HTTP 470/403 without proper session cookies. yt-dlp tries impersonation but fails if no browser is available.
- **Pagination** - Profile pages show limited thumbnails. Use direct gallery URLs for full albums.
- **URL format** - Gallery URLs use albumId parameter: `https://www.pornhub.com/album/viewphotos?albumId=XXX`
- **Cloudscraper works but CDN is protected** - Basic page fetching works, but direct CDN links need cookies
- **Video stream URLs** - HLS playlists (m3u8) and segmented MP4s require proper decryption tokens
- **No gallery-dl for videos** - Only supports image galleries, not full videos
- **Retired pornstar profiles return 410 Gone** - For retired models, `pornstar/{name}/videos` and `model/{name}/videos` return 410. The main profile page (`pornstar/{name}`) may still show thumbnails and links.
- **YouTube-dlp may fail while curl works** - curl may return 200 on video pages where yt-dlp returns 410 (different UA/SNI behavior). Extract HLS URLs from HTML and pipe to yt-dlp directly.
- **Albums survive profile removal** - Even when a pornstar's profile is gone, their photo albums remain accessible via `pornhub.com/album/{id}`
- **gallery-dl doesn't support video search** - Only image galleries. Use `pornhub.com/video/search?searchterm={query}` with curl for video discovery.
- **Search results may include unrelated content** - When searching for a name (e.g., "joon mali"), results can include videos with matching words in titles (e.g., "Mali Ubon", "Little Maly", "my tiny dyke friends") that are NOT the target model. Always verify video content before downloading.
- **Model/performer video pages return 410 Gone** - For many models, both `/model/{name}/videos` and `/pornstar/{name}/videos` return 410. The main profile page may also be gone. Some individual videos with direct links may still work temporarily. Video keys that include `&pkey=` parameters are often expired. Check the video URL first (`--simulate`) before attempting to download.
- **Gallery-dl for HLS URLs**: The reliable pattern to extract and decode HLS URLs from video page HTML: extract `"videoUrl"` JSON values, then `url.replace('\\/', '/')` followed by `.encode().decode('unicode_escape', errors='replace')`. This handles escaped JSON string encoding properly. Then pass the decoded URL to yt-dlp with `--referer https://www.pornhub.com/`.
- **Non-existent profiles (301 redirect)** - Profile URLs for non-pornstars (celebrities, mainstream figures, people with no Pornhub account) return HTTP 301 redirect to `/pornstars`. This includes both `/pornstar/{name}` and `/model/{name}` URLs. No profile content exists - the redirect returns the generic pornstars listing page. gallery-dl will resolve to `/photos` but get 404 on the photo API.
- **Celebrity name searches return parody content** - Searching for celebrity names (e.g., "megan thee stallion", "meg thee stallion") on video search typically returns parody/imitation porn videos made by adult performers impersonating or referencing the celebrity. The profile/avatar page for such profiles doesn't have real albums - generic albums found on search/result pages are typically unrelated (they appear on generic pages and are random user albums).
- **Video search with `&o=mv`** (most viewed) helps surface the most popular videos first, but verification is essential - search results often contain content about performers with similar names (e.g., "Mini Stallion", "YumTheeBoss") that are NOT the target person.
- **Empty model profiles (HTTP 200, no content)** - Some model profiles return HTTP 200 with a page title but contain NO actual uploaded content. gallery-dl returns "No results" because the photo AJAX endpoint returns empty (0 bytes). These profiles show only recommended/premium upsell content on their video and photos pages. The profile URL exists (not redirected) but no videos or galleries exist. This can happen for mainstream figures who haven't uploaded adult content. Verify by checking the AJAX endpoint response size and looking for actual video/album links on the page.
- **Pornstar profiles show recommended videos, not own content** - Even when a pornstar profile page (e.g., `/pornstar/megan-vale`) returns 200, the videos shown on the page may be generic "recommended" videos from other pornstars, not the target pornstar's actual content. Video thumbnails use phncdn.com URLs that are video thumbnails, not album photos. gallery-dl's `PornhubPhotosExtractor` returns "No results" when the AJAX endpoint is empty. Check video titles on the profile page to confirm they mention the target pornstar.
- **Mainstream celebrities have no Pornhub presence** - Mainstream public figures (singers, actors, athletes) typically have NO adult content on Pornhub. Non-existent profiles may return HTTP 200 (empty model profile page) or HTTP 301 redirect to `/pornstars`. If no pornstar/model profile exists, no parody videos featuring the person will be found in search either. Search results for celebrity names on Pornhub typically return parody/imitation content where adult performers impersonate the celebrity, not actual content of the person. For celebrities without adult presence, it's efficient to check the model profile first (HTTP status + gallery-dl `--get-urls`) before spending time on video search.
- **Virtual influencers/influencers return 200 with generic page title** - Profiles for virtual influencers or social media influencers without adult presence on Pornhub may return HTTP 200 with the generic pornhub page title "Top Pornstars and Models In Full-Length Free Sex Videos" rather than a redirect or 410. The page contains no profile-specific content. This is a distinct from the 301 redirect for non-existent profiles. Check the page title or profile banner area to distinguish.
- **"Bhabhi" is a character/genre in Indian adult films** - In Indian/Desi adult content, "Bhabhi" (sister-in-law) is a common character archetype/persona, similar to "Lust Stories" on OTT platforms. Content tagged "Rekha Bhabhi" refers to a character/series format, not necessarily the real person (Rekha Mona Sarkar). When searching for a model known for "X Bhabhi" content, expect results about characters in that genre, not verified content of the actual person. The model may have official OTT series (Ullu, Kooku, etc.) but not official Pornhub content.
- **Indian adult content uses title mix of Hindi/English** - Video titles often mix Hindi and English words (e.g., "Thukaee", "Malkin", "Devar", "Chotuu", "Bhabhi", "Naukar"). Search with these terms may yield more relevant results than English-only queries.
- **Search with visual endpoint returns 404** - The modern URL `pornhub.com/visual/search?search={query}` returns HTTP 404. Use the older format `pornhub.com/video/search?search={query}` instead.
- **Keyword-based action searches return generic content** - Searching for a specific performer with action keywords (e.g., "arya fae facial") typically returns generic/high-view videos matching the action keyword (e.g., "facial") but NOT featuring the target performer. The search index prioritizes view count over exact performer matching. Such searches should only be used for discovery, not as a reliable way to find specific type of content starring a particular performer. Verify each result by checking the title for the performer's name.
- **gallery-dl photos/gifs endpoints return 404** - `PornhubPhotosExtractor` and `PornhubGifsExtractor` return "No results" for URLs like `pornstar/{name}/photos` and `pornstar/{name}/gifs` even when the profile exists. The AJAX endpoints these extractors use return 404. Use HTML scraping or yt-dlp instead for profile-level content.
- **Profile page albums are recommended, not the pornstar's own albums** - Albums linked from a pornstar profile page are typically user-submitted or recommended albums, NOT albums created by or featuring the pornstar. Always verify album content (check gallery-dl output or album page title) before downloading. These can include random user content (e.g., "Pemela Anderson", "LilWasian69").
- **Profile image CDN versions** - Profile images from phncdn.com have multiple size options: `thumb_`, `bigger_`, `original_`. For retired models, only `thumb_` is available; `bigger_` and `original_` return 410 Gone. The thumb version is typically 234x234px.
- **Search queries with aliases find relevant content** - When a pornstar uses multiple aliases (e.g., "Amber Hardin" also known as "Veronica", "Alanova"), search queries combining the main name with aliases (e.g., "Amber Hardin Veronica") can find videos even when no dedicated pornstar profile exists for the alias.
- **GIF searches return other models with similar names** - GIF search for names like "Amber" returns content of other models (e.g., "Britney Amber", "Amber Jayne"). Filter results by checking titles for the exact performer name and alias.
- **Some search result videos are premium-only** - Videos appearing in search results may require premium to view. These return HTTP errors when checking via yt-dlp's `--dump-json` flag. Extract the page HTML and check for "Upgrade now" text to detect premium content.
- **pornstar/{name}/videos pagination** - Profile video pages are paginated with 47 videos per page. Page 1 mixes recommended/premium videos first, then shows "Tagged Videos" section. Pages 2+ show older tagged videos. Use `?page=N` to paginate. Check the page title to verify if a profile exists (should be "{Name} Porn Videos" not "Top Pornstars").
- **pornstar/profile video search with `?o=mv|tr|lg`** - Sorting options: `o=mr` (most recent, default), `o=mv` (most viewed), `o=tr` (top rated), `o=lg` (longest). These change order but same videos appear.
- **yt-dlp "already downloaded" detection fails** - When verifying if a video file exists before downloading, yt-dlp reports "already downloaded" even though the file exists. This happens because the sanitized filename in the skip-check doesn't match yt-dlp's output filename (e.g., different special character handling). Don't rely on yt-dlp's skip detection; use your own file existence check instead.
- **Video download speeds vary widely** - Pornhub HLS playlists have 150+ fragments at ~200KB each. Download speed ranges from 350KB/s to 7MB/s. At 720p, videos average 100-400MB. 10+ minute videos can be 60-150MB, while 30+ minute videos can be 300-700MB+.
- **Album ownership verified via album page title** - Album page titles read `"{Album Title} - {Owner}'s Albums"`. This is the fast, reliable way to confirm an album belongs to the target before downloading (sidebar/"Recent Albums" links from pornstar profile pages are mostly recommended albums from random users).
- **/model/{name} and /model/{name}/photos 301-redirect to the pornstar main page** - When a model page does not exist for an account, `/model/{name}` and `/model/{name}/photos` redirect (HTTP 200 after follow) to `/pornstar/{name}` (the main profile page), NOT to `/pornstars` (which is the no-profile redirect). Use `pornstar/{name}/photos` for the real photo-albums listing.
- **"{Name}'s Uploaded Videos" section = premium/PPV uploads** - Profile pages have a "{Name}'s Uploaded Videos" section whose items carry `data-entrycode="VidPg-premVid"` (premium PPV content). The "See All" link (`/pornstar/{name}/videos/upload`) renders a generic premium recommendation feed when fetched without a logged-in session - it is NOT a reliable list of her uploads headlessly. Counters like "Showing 1-40 of N" on that page refer to that feed.
- **Video page og:image = direct static 640x360 thumbnail** - `view_video.php?viewkey={vkey}` pages contain `og:image` meta with a direct thumbnail URL (ei/pix phncdn.com). Works without cookies and also for premium videos. Best way to batch-download video thumbnails (name files by vkey + title). Some og:images point at .mp4 preview paths yet serve static JPEGs - check file type and fix extensions.
- **/user/{username} and /user/{id} return 404 for pornstar accounts** - The account's user profile page is not reachable via `/user/{slug}` or numeric user id for verified pornstar accounts; do not rely on it to enumerate an account's albums.
- **Albums can be geo-blocked** - Album pages may return HTTP 200 with `<title></title>` and H1 "This content is unavailable in your country." Treat as skipped (not failed).
- **Pornstar profile pages have no banner image** - Profile pages only carry the avatar (e.g. `pics/users/{...}/avatar{ts}/(...)200x200.jpg`, actually ~150x150px). No larger original exists (other sizes 401). The best "profile images" of active models are her own photo albums.
