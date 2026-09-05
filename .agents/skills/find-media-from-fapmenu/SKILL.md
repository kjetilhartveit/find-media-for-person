---
name: find-media-from-fapmenu
description: Use when you need to find and download media from FapMenu, a large aggregator of leaked content (pics/videos) with paginated galleries.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for media of a specific person on FapMenu
- Downloading paginated galleries from FapMenu
- Searching FapMenu by name to find profile pages

# Find media from FapMenu

Download images and videos from FapMenu (https://fapmenu.com), a large aggregator hosting leaked content with paginated galleries.

## URL Patterns

- Site: `https://fapmenu.com`
- Profile: `https://fapmenu.com/{slug}/` — try the person's name first (e.g., `halle-hayes/`)
- Suffix aliases: When multiple profiles exist, slugs use a numeric suffix (e.g., `megan-thee-stallion-3/`, `megan-thee-stallion-4/`). Try searching for the person first.
- Aliases: Some profiles exist under multiple slugs — if one returns empty, try alternatives (e.g., `hallehayes1`, `hallehayesvip`, `the_real_halle_hayes`). These aliases may be referenced on the profile or via their social media bio links.
- Slug hyphenation varies by site: FapMenu may require hyphens (`layla-jenner-4`) while Fapello/Fapeza may require no-hyphen (`laylajenner`). Always try the most common slug format first, then fall back to search if 404.
- **Suffix aliases are common:** When multiple profiles exist, slugs use a numeric suffix (e.g., `layla-jenner-4`). The base slug without a number often returns 404. Try the search endpoint to find the correct profile slug.
- Names with common first names may match the wrong person (e.g., `sofie/` matches "Sofie Ivars" not "Sofie Eikeland"). Always verify the profile name and aliases listed on the page to ensure it's the correct person.
- **Identity verification signals**: the profile bio + meta description list the person's aliases (often their social handles), the bio text may state a post count that matches the gallery size, and the page may contain direct links to their social platforms (e.g. Instagram/OnlyFans) — cross-check those handles against the target person.
- **Alias co-occurrence**: Media page alt text may list multiple names (e.g., "Megan Vale / Lupe Burnett nude photo #0004"). This suggests content may include multiple models on the same gallery page — verify each image to ensure it's the target person.

## Image URL Patterns

- Full-size: `/models/{1st_char}/{2nd_char}/{slug}/{model_num}/full/{slug}_nude_XXXX.webp`
  - Example: `/models/m/e/megan-thee-stallion-3/2/full/megan-thee-stallion-3_nude_0001.webp`
  - The 1st/2nd chars are first/second chars of the slug (e.g., m/e for megan-thee-stallion-3)
  - **Multiple model numbers can exist** on a profile (e.g., model 1 = avatar, model 2+ = galleries)
- Thumbnail: `/models/{1st_char}/{2nd_char}/{slug}/{model_num}/300px/{slug}_nude_XXXX_300px.webp`
  - To get full-size URL from thumbnail: replace `/300px/` with `/full/` and remove the `_300px` from filename
  - Note: `_300px` appears in BOTH the path segment AND the filename (e.g., `_300px_300px.webp` → `.webp`)

## Search

- Search endpoint: POST to `https://fapmenu.com/search` with body `searchVal={name}`
- Search form uses field name `searchVal`
- Results contain profile links like `/slug/`
- Search is client-side rendered; use curl POST, not GET
- **Search endpoint reliability**: The search endpoint does not always return results even when content exists on the profile. Direct profile URL is more reliable — try the slug first, then fall back to search.
- One person often has **multiple alias profiles**, each with its own separate image numbering and non-overlapping galleries. Run every known alias/handle (real name, social handle, past professional aliases) through the search endpoint and collect ALL profile links (`href="/slug"`) from the result pages — profiles are frequently discoverable only via search, not via guessing slugs.
- Search POSTs can occasionally hang even when a direct page fetch is fast — always use a per-request timeout (e.g. `curl -m 25`) when polling the search endpoint.

## Primary download method — Manual scraping of paginated profile (Python script recommended)

A Python script is recommended for reliable multi-model, multi-page scraping. Use `curl` + `grep`/`sed` as an alternative for simple cases.

1. **Fetch the profile page**: `curl -sL "https://fapmenu.com/{slug}/page/{page}/"`
2. **Extract image URLs** from the page HTML:
    - Match pattern: `/models/{1st}/{2nd}/{slug}/{model_num}/300px/{slug}_nude_XXXX_300px.webp`
    - Use regex to capture the model number and image number: `/models/[a-z]+/[a-z]+/{slug}/(\d+)/300px/{slug}_nude_(\d+)_300px\.webp`
    - Convert to full-size: replace `/300px/` → `/full/` and strip `_300px` from filename
    - Full-size URL pattern: `https://fapmenu.com/models/{1st}/{2nd}/{slug}/{model_num}/full/{slug}_nude_XXXX.webp`
    - Each page typically has ~24–30 images
3. **Pagination**: Iterate page numbers. Each page usually has 24–25 images. Stop when a page has no images.
   - Pagination hrefs have **no trailing slash**: `href="/slug/page/2"`. Both `.../page/N/` and `.../page/N` work (redirect), but when detecting the next-page link in HTML, match the no-slash form (`/slug/page/{N+1}`) — checking for a trailing slash makes you stop prematurely.
   - **Final page detection**: the last page's HTML contains no link to `/slug/page/{N+1}` at all.
   - Skip model number 1 (avatar) which appears on every page as a duplicate — **however, some small profiles have their actual content in model 1** (e.g., Megan Vale has 4 images in model 1). Check if model 1 images are unique to the profile and not avatars.
   - Deduplicate across pages since the same image numbers may appear in different model folders
4. **Download images**: Use wget/curl to fetch each URL. Save as `.webp`. Files are typically WEBP format.
5. **Rate limiting**: Sleep 0.3–0.5s between requests. Respecting that, modest parallelism (e.g. 3 workers with ~0.15s per-worker delay) downloaded 894 images without bot protection kicking in (~2 min).

## Quality

- Images are typically high-resolution (original leaks)
- Format is WEBP (modern, good compression with quality)
- File sizes range from ~50KB to ~500KB+ per image
- Videos may be present but are less common than images
- **No videos have been found on FapMenu profiles** (confirmed on large profiles with 700+ images).

## Pitfalls

- Multiple alias slugs may exist for the same person — search is the best way to find all profiles
- The primary slug without a number (e.g., `megan-thee-stallion/`) may return 404 and won't work
- Profile may return 200 with no media items — this means the profile either doesn't exist for that person or is private
- **Small profiles may have no pagination** — page 2 returns 404, meaning the entire gallery fits on one page. Check if pagination exists.
- Some sequential IDs may not exist (gaps) — handle gracefully
- **Content items have individual media URLs** at `/{slug}/media/{NNNN}` — these can be used for direct access to individual items but don't affect download logic.
- **Large profiles may have 700+ images** across 30+ pages (e.g., `layla-jenner-4` with 746 consecutive IDs: 1-746, 32 pages). IDs are typically sequential with no gaps, 24 images per page.
- When collecting IDs, deduplicate across pages by checking for cycling (same ID set as previous page means stop).
- Pages 1 and 2 can display the **same** ID set even though a `/page/2` link exists — dedupe by image ID, never by page count.
- The same person's content is sometimes re-uploaded under different alias slugs (different filenames, sometimes different photos). If merging profiles, compare SHA-256 of downloaded files to detect actual duplicates, and treat different-numbered files as potentially unique content.
- Same/real-name profiles can belong to a DIFFERENT person (e.g. a slug equal to the target's real name or alias, with a large unrelated gallery under a modern social handle). Before downloading, cross-check social links and alias co-occurrence alt text; verify alias profiles via the meta description / alt text listing the person's known alias set.
- WEBP format requires conversion for some viewers — consider converting to JPG if needed
- Rate limiting is important; aggressive scraping may trigger Cloudflare/bot protection