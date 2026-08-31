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

- Cloudflare JavaScript challenge blocks ALL automated access. Both `curl` and `webfetch` return 403 errors.
- Workaround: Search for ModelSearcher pages via general web search engines (Google/Bing), then access them through a real browser session if media is needed.

### Search Behavior

The search with `?s=QUERY` parameter does not always return relevant results - the site often shows general OnlyFans profiles regardless of query. The internal search may not work well for specific names.

### gallery-dl Support

gallery-dl does NOT support modelsearcher as an extractor. Must use web scraping tools.

### Notable Findings - Persons Not Listed

- **Megan Vale (adult actress)**: ModelSearcher search for "Megan Vale" returns no profile. The site primarily tracks OnlyFans content creators and may not have mainstream/legacy adult film stars who are not active OnlyFans creators.
- **Amia Miley**: Despite having an OnlyFans account (@amiamiley), she does NOT have a profile on ModelSearcher. The site does not index all OnlyFans creators - it seems to only list selected/promoted creators.
- Thai adult performers/pornstars (like Joon Mali) often NOT listed - focus on OnlyFans content creators, not mainstream adult film stars

## Tips

- Not all models have profiles here - it's OnlyFans-specific and selective
- The site primarily links to paid OnlyFans subscriptions
- Images on the site are teaser/thumbnail images from OnlyFans
- Use web search engines to find ModelSearcher profiles rather than direct scraping

## Pitfalls

- Do NOT rely on this source for original high-quality media - it only shows OnlyFans teasers
- Cloudflare blocks all automated access (curl, webfetch, etc.)
- Search functionality may not return accurate results for specific names
- The site is focused on adult/OnlyFans content - may not have mainstream influencers
- ModelSearcher is NOT a comprehensive directory of all OnlyFans creators or adult performers