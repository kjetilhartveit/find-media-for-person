---
name: find-media-from-tiktok
description: Use when you need to find and download media from TikTok profiles, posts, and videos using gallery-dl or yt-dlp.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Downloading videos from a specific TikTok profile
- Scraping all media from a TikTok user account
- Extracting media from a single TikTok video URL
- Finding content via TikTok search/embed URLs

# TikTok source URLs

- **Profile**: `https://www.tiktok.com/@{username}`
- **Posts filter**: `https://www.tiktok.com/@{username}/posts`
- **Single video**: `https://www.tiktok.com/@{username}/video/{id}`
- **Video short link**: `https://vm.tiktok.com/{short_id}`
- **Likes (requires auth)**: `https://www.tiktok.com/@{username}/liked`

# Recommendations on how to download

**Primary method: yt-dlp** — reliable for full profile downloads. Use `--download-archive` with an archive file in `/tmp/` (no spaces in path) to track already-downloaded videos and resume across sessions. Requires multiple batch calls for large accounts (583+ videos needs ~6+ batch runs).

**gallery-dl** — extracts avatar successfully but less reliable for full profile video downloads on very large accounts. Use for single avatar image extraction.

## Recommended yt-dlp workflow

1. **Check profile first** to see how many videos:
   ```bash
   yt-dlp --simulate "https://www.tiktok.com/@{username}" 2>&1 | grep -c "Playlist"
   ```

2. **Archive file** (in `/tmp/` without spaces):
   ```bash
   echo "" > /tmp/tiktok_archive.txt
   ```

3. **Download in batches** (each batch needs ~15 min timeout):
   ```bash
   # First: extract existing IDs from already-downloaded files
   for f in /path/to/tiktok/*.mp4; do basename "$f" .mp4; done > /tmp/tiktok_archive.txt

   # Run yt-dlp (each call downloads ~80-150 videos)
   yt-dlp -S "res:1080,ext" \
     --download-archive /tmp/tiktok_archive.txt \
     --output "/path/to/tiktok/%(id)s.%(ext)s" \
     --sleep-interval 5 \
     --max-sleep-interval 12 \
     "https://www.tiktok.com/@{username}"
   ```

4. **Clean up**: Remove `.m4a` and `.mp3` files (from carousel posts that contain audio). Keep only `.mp4` and `.jpg` files.

5. **Repeat** until `yt-dlp` reports "Finished downloading playlist".

**Output filename**: Use `%(id)s.%(ext)s` to avoid filesystem issues with space-containing titles. For gallery-dl avatar files, IDs are used without spaces.

# Pitfalls

- **item_list API returns 0 items**. The TikTok `creator/item_list` API (used by gallery-dl's `TiktokPostsExtractor`) frequently returns 0 items, even for accounts with published videos. Videos are discovered via HTML page parsing instead, yielding fewer but still valid results.
- **Small/inactive accounts** may have very few or no videos. Check profile stats (followers, likes, videoCount) before investing time. A signature of "Ikke i bruk" (Not in use) indicates an abandoned account.
- **Accounts with 0 posted videos**. Some verified/celebrity accounts exist on TikTok but have no public videos posted (0 in videoCount). The account exists and is public, but the user has never posted content. Use `yt-dlp --simulate` to quickly check: if it returns "This account does not have any videos posted", stop before wasting time. The account @tyla is an example — only 238 followers, 0 videos, not verified.
- **Alternative usernames** may not exist (e.g., @username vs @username). Try variations if needed.
- **Private/unavailable accounts**: Some accounts may be private or have embedding disabled (`[tiktok:user] This user's account is either private or has embedding disabled`). These won't be accessible — stop before wasting time. Example: @thereallaylajenner (different from @thelaylajenner) returned this error.
- **TikTok search via gallery-dl is not supported** — no extractor for TikTok's search/discover. Use `yt-dlp --simulate` on a profile URL to preview what would be downloaded.
- **Long downloads need long timeouts**. Profile downloads can take 10+ minutes even for large accounts. Set bash timeout to at least `900000`ms (15 min).
- **Videos are 9:16 portrait** (typically 540x960 or 720x1280). Low resolution is normal for TikTok.
- **Region settings don't help**. Setting `"region": "NO"` in config does not change API behavior.
- **Avatar images**: The avatar is extracted separately from the profile page. It's usually a high-quality (1080x1080) profile picture.
- **No cookie required**. TikTok is generally public without authentication. Private accounts won't be accessible through gallery-dl API.
- **yt-dlp impersonation warning** — yt-dlp may show `[TikTok] The extractor is attempting impersonation` warnings but downloads still work. No action needed unless blocked.
- **yt-dlp download-archive** — use `--download-archive download_archive.txt` to prevent re-downloading already saved videos (useful for resuming interrupted downloads). Note: if the archive file path contains spaces, yt-dlp may fail — keep the archive file in a path without spaces (e.g., in `/tmp/`).
- **yt-dlp output format with spaces** — when output path or title contains special characters, use `--output "%(id)s_%(title)s.%(ext)s"` (ID-prefix naming) to avoid filesystem issues. Avoid `%(fulltitle)s` which may create unescaped path separators.