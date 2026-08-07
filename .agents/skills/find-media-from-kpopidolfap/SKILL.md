---
name: find-media-from-kpopidolfap
description: Use when you need to find K-pop idol media from KpopIdolFap, a niche aggregator with tag-based browsing.
---

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Looking for images of a K-pop idol on KpopIdolFap
- Using tag pages (`/post/tag/<name>/`) to discover posts about a person

# Find media from KpopIdolFap

Find images from KpopIdolFap (https://kpopidolfap.com), a WordPress-based aggregator of K-pop idol content.

## URL Patterns

- Site: `https://kpopidolfap.com`
- Tag page: `https://kpopidolfap.com/post/tag/<tag>/` (e.g. `/post/tag/jessi/`) — lists all posts tagged with that name
- Search: `https://kpopidolfap.com/search/?q=<query>` — returned 404 in testing; prefer tag pages instead
- Individual post: `https://kpopidolfap.com/post/<id>/`
- Images: `https://kpopidolfap.com/wp-content/uploads/<YEAR>/<MONTH>/<filename>.jpg`

## Recommendations on how to download

1. Use a tag page (`/post/tag/<name>/`) to discover all posts about a person. Try name variations (stage name, real name, handle).
2. Parse the tag page for post links matching `/post/\d+/`.
3. Fetch each post page to extract image URLs from the HTML — look for `wp-content/uploads` paths in `<img src>` and `<a href>` attributes.
4. Posts have `prev`/`next` navigation links for browsing adjacent content.
5. Rate limiting: sleep 0.3–0.5s between requests.
6. Use a user-agent header.

## Quality

- Small number of posts per idol (typically 2–5).
- Images ~70–130KB each. Low file count but usable quality.

## Pitfalls

- **Content may be faked.** Posts are often categorized under "Korean Idol Fakes" — content can be AI-generated or photoshopped, not real leaks.
- **Search endpoint returns 404.** Rely on tag pages (`/post/tag/<name>/`) to find content.
- **Low volume.** Small post counts per person — not a primary source.
- **WordPress parsing.** Extract image URLs from the post HTML body, filtering for paths containing the person's name to avoid unrelated images.
- **Resized duplicates.** Posts may include multiple sizes of the same image (e.g. `-211x300.jpg`, `-720x1024.jpg`). Keep only the largest/original.
