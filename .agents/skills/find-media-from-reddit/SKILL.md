---
name: find-media-from-reddit
description: Use when searching for or downloading media of a person from Reddit (post search, i.redd.it media) via gallery-dl, reddit JSON, or web-search discovery.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Searching Reddit for images/posts of a person (by name, handle, or alias)
- Downloading images/videos from reddit posts (i.redd.it)
- Looking for fan subs, r/pics, or leak posts about a person

# Find media from Reddit

## Known access restrictions (as of 2026)

- **Reddit blocks unauthenticated datacenter IPs.** `gallery-dl` on a search URL returns the HTML block page ("You've been blocked by network security"), and `https://www.reddit.com/search.json?…` / per-post `.json` return HTTP 403 even with a browser user-agent.
- **old.reddit.com search now requires login** (302 → `/login/?reason=lor2`).

Recommendations:

1. **Prefer authenticated access.** If a reddit session/cookies are available in the cookies file, pass them to `gallery-dl --cookies` (reddit extractor supports user accounts). Without auth, direct scraping from a server IP is effectively blocked.
2. **Web-search discovery instead of in-site search.** Search `"{person name}" site:reddit.com` (and with known aliases). Web engines index reddit posts, and a found post URL can be resolved through a mirror/proxy to extract `i.redd.it` media URLs.
3. **Direct media URLs don't need reddit API access.** `i.redd.it/<file>.<ext>` (and `.jpg?auto=webp`) media URLs are served directly; once you know them (from search results, embeds, or mirrors) download them with curl/gallery-dl.
4. If blocked, stop that source after 2 attempts per the time budget and report it — do not keep retrying reddit endpoints.

## URL patterns

- Search: `https://www.reddit.com/search/?q={query}&sort=relevance`
- JSON (needs auth from blocked IPs): `https://www.reddit.com/search.json?q={query}&limit=25`
- Media: `https://i.redd.it/{hash}.{ext}` — append `?auto=webp&f=auto&q=low` variants only if you want lower quality (omit for full size).
