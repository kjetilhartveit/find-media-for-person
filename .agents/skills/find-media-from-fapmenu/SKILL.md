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
- Profile: `https://fapmenu.com/{slug}/` — try the person's name first (e.g. `halle-hayes/`)
- Aliases: Some profiles exist under multiple slugs — if one returns empty, try alternatives (e.g. `hallehayes1`, `hallehayesvip`, `the_real_halle_hayes`). These aliases may be referenced on the profile or via their social media bio links.
- Names with common first names may match the wrong person (e.g. `sofie/` matches "Sofie Ivars" not "Sofie Eikeland"). Always verify the profile name and aliases listed on the page to ensure it's the correct person.
- Item URLs: `https://fapmenu.com/media/{id}` — sequentially numbered items
- Image source: WEBP format, URLs follow `/media/{id}` pattern

## Primary download method — Manual scraping of paginated profile

1. **Fetch the profile page**: `curl -s "https://fapmenu.com/{slug}/" > page.html`
2. **Extract item URLs** from the page HTML:
   - Look for links or image sources referencing `/media/` followed by numeric IDs
   - IDs are sequential (e.g., 1, 2, 3...) — scrape all IDs listed on the page
   - Page 1 typically has ~25 items, with pagination providing subsequent pages
3. **Pagination**: If pagination exists, scrape each page to collect all media IDs. FapMenu profiles may have 100+ items across multiple pages.
4. **Download images**: For each media ID, fetch `https://fapmenu.com/media/{id}` and extract the actual image URL or download directly. Files are typically in WEBP format.
5. **Rate limiting**: Sleep 0.3–0.5s between requests. Respect the site's anti-bot measures.

## Fallback — Direct ID scanning

If scraping page URLs fails, scan sequential IDs:

1. Start at ID 1 and increment
2. For each ID, try fetching `https://fapmenu.com/media/{id}`
3. Stop when you get consistent 404s (end of content)
4. Note: Some IDs may be missing (gaps in sequence) — skip these gracefully

## Quality

- Images are typically high-resolution (original leaks)
- Format is WEBP (modern, good compression with quality)
- File sizes range from ~50KB to ~500KB+ per image
- Videos may be present but are less common than images

## Pitfalls

- Multiple alias slugs may exist for the same person — try all if the primary slug yields no results
- Profile may return 200 with no media items — this means the profile either doesn't exist for that person or is private
- Some sequential IDs may not exist (gaps) — handle gracefully
- WEBP format requires conversion for some viewers — consider converting to JPG if needed
- Rate limiting is important; aggressive scraping may trigger Cloudflare/bot protection
