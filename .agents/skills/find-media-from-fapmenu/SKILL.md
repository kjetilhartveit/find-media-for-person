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
- Names with common first names may match the wrong person (e.g., `sofie/` matches "Sofie Ivars" not "Sofie Eikeland"). Always verify the profile name and aliases listed on the page to ensure it's the correct person.

## Image URL Patterns

- Full-size: `/models/{1st_char}/{2nd_char}/{slug}/1/full/{slug}_nude_XXXX.webp`
  - Example: `/models/m/e/megan-thee-stallion-3/1/full/megan-thee-stallion-3_nude_0001.webp`
  - The 1st/2nd chars are first/second chars of the slug (e.g., m/e for megan-thee-stallion-3)
- Thumbnail: `/models/{1st_char}/{2nd_char}/{slug}/1/300px/{slug}_nude_XXXX_300px.webp`
  - To get full-size URL from thumbnail: replace `300px` → `full` and remove `_300px` from filename

## Search

- Search endpoint: POST to `https://fapmenu.com/search` with body `searchVal={name}`
- Search form uses field name `searchVal`
- Results contain profile links like `/slug/`
- Search is client-side rendered; use curl POST, not GET

## Primary download method — Manual scraping of paginated profile

1. **Fetch the profile page**: `curl -sL "https://fapmenu.com/{slug}/page/{page}/" > page.html`
2. **Extract image URLs** from the page HTML:
   - Look for `src="/models/{...}/{slug}/1/300px/{slug}_nude_XXXX_300px.webp"` in `<img>` tags
   - Each page typically has ~25 images
   - Remove leading `src="` and trailing `"` and the `/300px/{slug}_nude_\d+_300px` → `/full/{slug}_nude_\d+` pattern to convert to full-size paths
   - Prepend `https://fapmenu.com` to create full URLs
3. **Pagination**: Check which pages exist by iterating page numbers. Each page usually has 25 images. Stop when a page has no images.
  - Note: The avatar image (often showing up as `nude_0001` or near the start) may appear on every page — deduplicate when collecting across pages.
4. **Download images**: Fetch `https://fapmenu.com/{image_path}` and save as `.webp`. Files are typically WEBP format.
5. **Rate limiting**: Sleep 0.3–0.5s between requests. Respect the site's anti-bot measures.

## Quality

- Images are typically high-resolution (original leaks)
- Format is WEBP (modern, good compression with quality)
- File sizes range from ~50KB to ~500KB+ per image
- Videos may be present but are less common than images

## Pitfalls

- Multiple alias slugs may exist for the same person — search is the best way to find all profiles
- The primary slug without a number (e.g., `megan-thee-stallion/`) may return 404 and won't work
- Profile may return 200 with no media items — this means the profile either doesn't exist for that person or is private
- Some sequential IDs may not exist (gaps) — handle gracefully
- WEBP format requires conversion for some viewers — consider converting to JPG if needed
- Rate limiting is important; aggressive scraping may trigger Cloudflare/bot protection