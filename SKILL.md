---
name: find-and-store-media-for-person
description: Gather media for a celebrity/person for local storage to disk.
---

# Find and store media of a person to disk

The purpose of this skill is to gather media of a celebrity/person and store them to disk.

## Output

- Stored media of the person to disk.
- A single markdown file named `SUMMARY.md` in the folder named after the person which gives a short summary of the person and the result of the search (and persistence) of media. It can also mention next steps for further research or add additional comments.

## Destination directory for stored media

- The media should be stored at the destination of the environment variable `MEDIA_DIR` in `.env`. If the environment variable is not set or if we don't have access to the directory, then we should store the media in a new folder in the root directory of the project.
- Each "find and store media" attempt should store the media in a subfolder in the media folder mentioned above. The subfolder should be named after the person's name (e.g. `Caroline Nitter`, `Taylor Bow` and so on).
- When we retrieve media from the sources, we should store the results for each source in yet another subfolder in the subfolder for that person's name. E.g. (`google searches`, `fapeza`, `pictoa` and so on).

## Guidelines for finding and storing media

- Fetch both pictures and videos.
  - Sometimes thumbnails or lower quality versions of media (particularly for pictures) are used in galleries etc. We should make an effort in fetching the highest quality of media whenever possible.
  - Sometimes videos are served in other ways than direct download links (e.g. m3u8 playlists), in which cases we might have to use alternative ways to download the video (e.g. using the `yt-dlp` tool).
- Prefer to avoid duplicates, but if in doubt then fetch the media.
- We should avoid naming collisions of media files. If a file with the same name already exists in the folder then add a suffix like ` (1)`, ` (2)` etc.

## Tools

- You should use web searches and/or web scraping to find media of the person.
- You may use `yt-dlp` to download videos from YouTube or other supported platforms.

## Sources to Search For Media

### Instagram

- Website URL: https://www.instagram.com/
- Example of URL to an Instagram account: https://www.instagram.com/carolinenitter/

### Fapeza

- Website URL: https://www.fapeza.com/
- Example of URL to a model: https://fapeza.com/caroline-nitter/
- Helper Script for Changing Photos to High Quality in the Gallery (in the browser). Use if needed:
  ```javascript
  document.querySelectorAll(".posts-wrapper img").forEach((img) => {
    img.src = img.src.replace(/_400px\.(\w+)$/, ".$1");
  });
  ```

### Pictoa

This website might not have direct URLs for celebs/persons. We might have to do a search with the name and find relevant albums.

- Example of URL to an album: https://www.pictoa.com/albums/caroline-nitter-nude-4088413.html
- Example path of a thumbnail image: https://t1.pictoa.com/media/galleries/282/396/282396602d9948ac637/3926902602d994abc044.jpg
- Example path of a large/high quality image: https://s2.pictoa.com/media/galleries/282/396/282396602d9948ac637/3926902602d994abc044.jpg
- Script for Changing Photos to High Quality in the Gallery (in the browser). Use if needed:
  ```javascript
  $$(".wrapper img").forEach((img) => {
    if (img.src) img.src = img.src.replace("//t1.", "//s2.");
    if (img.dataset.src)
      img.dataset.src = img.dataset.src.replace("//t1.", "//s2.");
  });
  ```

### Reddit

If we would like to retrieve media from this page we might have to do a search.

- Website URL: https://www.reddit.com
- Subreddit for Norwegian beauties: https://www.reddit.com/r/Norwegianbeauties/

### UltraThots

- Website URL: https://ultrathots.com
- Example of URL to a model: https://ultrathots.com/models/caroline-nitter/

### erome

- Website URL: https://www.erome.com
- Example of URL to a model: https://www.erome.com/a/nvhtQ8C8

### fapello

- Website URL: https://fapello.com
- Example of URL to a model: https://fapello.com/caroline-nitter/

### leakedmodels

- Website URL: https://ru.leakedmodels.com
- Example of URL to a model: https://ru.leakedmodels.com/caroline-nitter/

### nudogram

- Website URL: https://ua.nudogram.com
- Example of URL to a model: https://ua.nudogram.com/models/caroline-nitter/

### thefappeningblog

- Website URL: https://thefappeningblog.com
- Example of URL to a model: https://thefappeningblog.com/gallery/caroline-nitter/

### fappeningbook

- Website URL: https://fappeningbook.com
- Example of URL to a model: https://fappeningbook.com/caroline-nitter-nude/

### pornhex

- Website URL: https://no.pornhex.com
- Example of URL to a model: https://no.pornhex.com/video/crole-nitter-suckg-ridg-dick

### OnlyFans

- Website URL: https://onlyfans.com
- Example of URL to a model: https://onlyfans.com/notsoordinarycc

### modelsearcher

- Website URL: https://modelsearcher.com
- Example of URL to model: https://modelsearcher.com/profile/notsoordinarycc?tab=post
- Example of URL to a model's photos: https://modelsearcher.com/profile/notsoordinarycc?tab=photo
- Example of URL to a model's videos: https://modelsearcher.com/profile/notsoordinarycc?tab=video

### TikTok

- Website URL: https://www.tiktok.com
- Example of URL to a TikTok account: https://www.tiktok.com/@carolinenitter

### linktree

Models might have linktree's which links to other platforms where they might have media.

- Website URL: https://linktr.ee
- Example of URL to a linktree for a model: https://linktr.ee/carolinenitter
