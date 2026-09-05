---
name: find-media-from-modelsearcher
description: Use when searching for OnlyFans creator profiles on ModelSearcher.com, a directory/aggregator of OnlyFans creators across categories.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Searching for OnlyFans creator profiles on ModelSearcher.com
- Finding aggregated OnlyFans subscription links for various creators

# ModelSearcher.com

## Main URL

- https://modelsearcher.com
- Hub/Blog: https://modelsearcher.com/hub/

## How it works

ModelSearcher is a directory/aggregator of OnlyFans creators across categories (fitness, Asian, MILF, etc.). It does NOT host original media - it links to OnlyFans subscription pages and provides profile info and teaser images.

## URLs and Structure

- **Search**: https://modelsearcher.com/?s=QUERY (uses site search)
- **Posts**: https://modelsearcher.com/post?s=QUERY
- **Profile**: https://modelsearcher.com/profile/USERNAME
- **Categories**: https://modelsearcher.com/onlyfans/CATEGORY
  - Examples: /onlyfans/fitness, /onlyfans/asian, /onlyfans/milf, etc.
- **Hub**: https://modelsearcher.com/hub/ (blog/content about OnlyFans)
- **Free trials**: https://modelsearcher.com/onlyfans/free-trials
- **Locations**: https://modelsearcher.com/locations

## Important Notes

### Cloudflare Protection

- Cloudflare JavaScript challenge blocks all automated access to `modelsearcher.com` HTML pages. Both `curl` and `webfetch` return 403 errors. Cloudflare proxies/reader services (e.g. r.jina.ai) also get blocked.
- **Only the HTML pages are blocked.** The image/CDN hosts are NOT protected and can be downloaded directly with `curl` (plain User-Agent suffices):
  - `api.modelsearcher.com` (feed photos/thumbs, logos, misc images)
  - `public.onlyfans.com` (creator avatars/headers stored on OnlyFans public CDN)
  - `ctimages.servefilesonly.com` (thumbnail resizer, mostly for other/related models)
- **Best workaround: the Wayback Machine.** Profile pages are server-side-rendered (Next.js RSC), so a `web.archive.org` snapshot contains the full page HTML AND the embedded structured post data - no browser session needed:
  - Check for snapshots: `curl "http://archive.org/wayback/available?url=modelsearcher.com/profile/USERNAME"` or the CDX API: `curl "http://web.archive.org/cdx/search/cdx?url=modelsearcher.com/profile/USERNAME*&fl=timestamp,original,statuscode"`
  - Fetch the snapshot: `curl -sL "http://web.archive.org/web/<timestamp>/https://modelsearcher.com/profile/USERNAME"`
  - Extract media URLs from the snapshot HTML, then download the images directly from the CDN hosts (not via web.archive.org) for best quality/speed.

### Profile Page Contents (from archived snapshots)

- The page header shows profile stats: display name, @handle, followers, post/photo/video counts, subscription price, location, attributes and bio.
- The profile's embedded feed (a `self.__next_f.push` RSC chunk in the HTML) contains a limited set of recent posts (~13) with structured JSON: slug, caption (`text`), `createdAt`, `type` (photo/video), and file entries (name, width, height). The header post counts can be much larger (e.g. 103) - those extra posts are NOT in the payload.
- `?tab=photo` / `?tab=video` tabs are client-side rendered, so archived snapshots of tab URLs usually don't contain the extra media.
- Media URL patterns:
  - Feed photos: `https://api.modelsearcher.com/feeds/photo-<timestamp>-<username>.jpg` (full size), `feeds/thumb-<timestamp>-<username>.jpg` (thumb)
  - Avatar/header: `https://public.onlyfans.com/files/<hash>/avatar.jpg` (and `/header.jpg`); `thumbs.onlyfans.com` versions are downscaled
  - Beware of one site-wide "top monthly models" video (m3u8 on `videos.fansmetrics.com`) embedded in every profile page - it is unrelated to the profile; verify before downloading.
- The feed posts can be stale - both a 2024 and a 2025 archive snapshot of the same profile showed the same 13 posts from mid-2024.

### Search Behavior

The search with `?s=QUERY` parameter does not always return relevant results - the site often shows general OnlyFans profiles regardless of query. The internal search may not work well for specific names.

### Checking whether a person is listed at all

To confirm absence without a browser, do a bulk Wayback CDX scan for any archived page whose URL contains the person's name:

- `curl -s "http://web.archive.org/cdx/search/cdx?url=modelsearcher.com*&filter=original:.*NAME.*&fl=timestamp,original,statuscode&limit=20"`
- An empty result means no snapshot of any page for that name exists - a strong (not absolute) signal the person is not listed. Note: CDX name filters only catch name-based slugs; a profile slug that is just a handle variant would only surface if handle variants were also archived.
- The sitemap (`https://modelsearcher.com/sitemap.xml`) is also Cloudflare-blocked (403) - no value in trying it.

### gallery-dl Support

gallery-dl does NOT support modelsearcher as an extractor. Must use web scraping tools.

### Notable Findings - Persons Not Listed

- **Megan Vale (adult actress)**: ModelSearcher search for "Megan Vale" returns no profile. The site primarily tracks OnlyFans content creators and may not have mainstream/legacy adult film stars who are not active OnlyFans creators.
- **Amia Miley**: Despite having an OnlyFans account (@amiamiley), she does NOT have a profile on ModelSearcher. The site does not index all OnlyFans creators - it seems to only list selected/promoted creators.
- Thai adult performers/pornstars (like Joon Mali) often NOT listed - focus on OnlyFans content creators, not mainstream adult film stars

### Notable Findings - Persons With Profiles

- **Lela Star** (adult actress, OnlyFans @getlela): listed at `/profile/getlela`. High-profile creators with active OnlyFans often ARE listed, so try the profile URL directly (plus the Wayback Machine) even for well-known performers.

## Tips

- Not all models have profiles here - it's OnlyFans-specific and selective
- The site primarily links to paid OnlyFans subscriptions
- Images on the site are teaser/thumbnail images from OnlyFans
- Use web search engines to find ModelSearcher profiles rather than direct scraping

## Pitfalls

- Do NOT rely on this source for original high-quality media - it only shows OnlyFans teasers
- Cloudflare blocks all automated access to HTML pages (curl, webfetch, reader proxies) - use Wayback Machine snapshots to get page data; image CDN hosts stay open for direct downloads
- Search functionality may not return accurate results for specific names
- The site is focused on adult/OnlyFans content - may not have mainstream influencers
- ModelSearcher is NOT a comprehensive directory of all OnlyFans creators or adult performers