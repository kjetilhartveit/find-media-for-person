---
name: find-media-from-tnaflix
description: Use when you need to find and download media from TNAFlix (tnaflix.com), a free porn tube site with pornstar profile pages and direct MP4 video formats.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for older/webcam-era videos of a person on TNAFlix
- Downloading videos from a pornstar's TNAFlix profile
- Finding facial-cum content (videos are categorized, e.g. under `facial-porn/`)

# Find media from TNAFlix

TNAFlix (https://www.tnaflix.com) is a free porn tube site. Profile pages are server-side rendered; video files are plain MP4 downloads per quality.

## URL Patterns

- Profile: `https://www.tnaflix.com/profile/{slug}` — **singular** `profile`. The `profiles/` variant and `pornstar/` 404. Slugs sometimes carry a numeric suffix (e.g. `andrea-rincon-4245`). Discover the exact slug via Google (`site:tnaflix.com "{name}"`) or from profile links inside video pages.
- Profile pagination: `https://www.tnaflix.com/profile/{slug}?page=N` (server-rendered, ~35 videos per page)
- Video: `https://www.tnaflix.com/{category}/{slug}/video{id}` — e.g. `https://www.tnaflix.com/facial-porn/{slug}/video{id}`
- Search: `https://www.tnaflix.com/search?what={query}`

## Anti-bot / headers

Bare `curl` may get a "soft 404" (HTTP 200 with a 404 page that lists language variants) even when the page exists. A cookie jar plus full browser headers fix it:

```bash
curl -s --compressed -L -c cj.txt -b cj.txt \
  -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9" \
  -H "Accept-Language: en-US,en;q=0.9" \
  -H "Referer: https://www.tnaflix.com/" \
  "https://www.tnaflix.com/profile/{slug}"
```

## Parsing profile pages

- `<h1>` = performer name; a `Videos (N)` line gives the total video count.
- Video links: regex `href="([a-z-]+/[a-zA-Z0-9._~/-]*/video\d+)"` over the HTML, dedupe by `video{id}`.
- The category path segment encodes the content type — useful for value-prioritizing, e.g. `facial-porn/`, `blowjob-videos/`, `anal-porn/`, `babe-videos/`.

## Downloading with yt-dlp

`yt-dlp` supports TNAFlix directly (plain MP4, HTTP). `gallery-dl` does NOT support TNAFlix.

```bash
yt-dlp -f "480p/720p/best" --user-agent "Mozilla/5.0 ..." "https://www.tnaflix.com/{category}/{slug}/video{id}"
```

Available formats: 144p / 240p / 360p / 480p / 720p / 1080p MP4.

## Pitfalls

- **Profile/video tags are auto-generated and noisy.** Profiles mix in videos whose real star is a different performer sharing a similar name (e.g. "Selena Love", "Virginee Spice", "Selena Gomez" uploads tagged "Selena Spice"). Always require the target person's name/alias in the TITLE before downloading; check the cast list on the video page when unsure.
- **Bandwidth can be very low** (observed ~120 KB/s bursts, up to a few MB/s). A batch of 20-30 videos can take an hour — run large batches detached (`setsid nohup ... &`) and poll a log file.
- Profile counts (`Videos (N)`) can exceed what the listed pages expose; if pagination stops before N, the remainder may be JS-loaded or missing.
