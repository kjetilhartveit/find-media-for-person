---
name: shared-find-media-guidelines
description: Use when searching for or finding media from any source, and need general guidelines for content, quality, and technical best practices.
---

# When to use this skill

- Before searching for or downloading media from any source
- You need guidelines for content selection, quality, and scraping best practices
- You need to know when and how to update or create new source-specific skills

# Shared Find Media Guidelines

## Soft instructions on how to search for and download media from a source

In general a search for media from a source should include the following. But note you are not limited to these steps and can add or change them as you see fit:

1. Prepare the search:
   - which source(s) do I need to search?
   - which skills do I need to use?
   - get a rough idea of how to perform the search
   - create a TODO-list with steps to follow
2. Find media from the sources and download the media.
3. If new insight about the search has been found, then we should update (or create new) relevant skill(s) with the new findings. We want to update the skill(s) with insight about how to more efficiently search for media and we can also fix out-dated/inaccurate information in the skill(s).
   - See section below.
4. Output the results:

   - a summary of how the search (and persistence) of media went.
   - list which media files were persisted, which ones failed and which ones were skipped.
   - mention next steps for further research/media searches of the person/model.
   - tips on improving the search and/or persistance of media - was something cumbersome to do or did something fail?

## Content / Media Guidelines

- We are particularly interested in explicit/adult material for our archive (including pornographic content). Nude/revealing clothing, sexual positions are great. The main point is that they are attractive images of the person we are looking for.
- The most interesting material would be **facials / cum on face** of the person we are looking for.
  - If we find these then we should make note of the source and highlight it in future searches.
  - When we do web searches we should always remember to search for "facials" and "cum on face" in addition to the person's name.
- We don't want cum tributes by men NOR trannies.
- Note: the content does not have to be leaked or "secret". It can be public/open images like from Instagram etc
- Note 2: there might be irrelevant pictures/videos/media on the websites we are exploring/searching. We should make an effort to only download content/media of the person we are looking for.

## Technical Guidelines for finding and storing media

- Fetch both pictures and videos.
  - Sometimes thumbnails or lower quality versions of media (particularly for pictures) are used in galleries etc. We should make an effort in fetching the highest quality of media whenever possible.
  - Sometimes videos are served in other ways than direct download links (e.g. m3u8 playlists), in which cases we might have to use alternative ways to download the video (e.g. using the `yt-dlp` tool).
- Prefer to avoid duplicates, but if in doubt then fetch the media.
- We should avoid naming collisions of media files. If a file with the same name already exists in the folder then add a suffix like ` (1)`, ` (2)` etc.
- Scraping best practices: When scraping we should make sure not to spam their webservers with a huge number of simultaneous requests. We should limit to 1-3 scraping requests/downloads at the same time and also add a short delay between the requests.

## Tools

- You may use `yt-dlp` to download videos from YouTube or other supported platforms.
- You may use `gallery-dl` to download media from many websites. See skill `using-gallery-dl` for guidance.
  - To verify that `gallery-dl` supports the target source, use the command `gallery-dl --list-extractors` with `grep`.
- You may use web searches and/or web scraping to find media of the person.
- Sometimes your internal tooling might fail or error (e.g. parsing errors). Don't panic! Read the error and consider ways to get around it or fix the error. Be creative, sometimes we can retry or change the way we used the tool to get around it. We should try to avoid skipping the step because of the error.

### Web Search Guidelines

When doing web searches (either via the main orchestrator or subagents):

- We should prefer to use the browser tool if available, because websites might have a "confirm your age" pop-up etc. We need to click through these in order to fetch the actual content.
- Only make a maximum of 10 web searches per agent to avoid context exhaustion. Prefer to return quickly with a few results and encourage further searches rather than making too many large searches in one go.
- Web search engines return article URLs, not image URLs. The actual images are embedded in the HTML of those articles. Extract image URLs efficiently without downloading full pages of HTML bloat.

## Update/create skills when gaining new insight or updated information when doing searches or downloading media

- Update the skill whenever you learn new findings or knowledge about finding or downloading media in a source. We should also update the skill if it has out-dated information.
- Note that individual experiences from searches might not apply to future searches, so we should not make strong assumptions based on single searches.
- If no skill exists for a source you used then create a new one.
  - Note for skill creation: skills should follow the naming convention `find-media-from-<source-name>` (e.g. `find-media-from-instagram`).
  - A skill should include the main website URL, example URLs, and useful information about how to search for and find media from the source.
- Keep skills concise — treat them as supplementary information and not strict guidelines. Use language like "Recommendations" rather than "How to".
- When we create or make changes to skill(s) following a search then we should commit the changes and push them to the repository.
