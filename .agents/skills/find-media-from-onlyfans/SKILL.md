# Skill: find-media-from-onlyfans

# Before using this skill

Make sure to read the `shared-find-media-guidelines` skill before using this skill.

# When to use this skill

- Verifying whether a person has an OnlyFans account
- Trying to download free/public preview content from an OnlyFans profile

# OnlyFans.com

## Main URL / profile URL pattern

- https://onlyfans.com
- Profile: https://onlyfans.com/USERNAME

## What works without an account

Very little. Recommendations:

- **Direct curl of a profile page is useless for existence checks.** `curl` on `onlyfans.com/<handle>` (any handle, existing or not) returns the same generic ~17KB 404-style page with `og:title=OnlyFans` and no profile-specific meta tags. Do not conclude from a single curl whether a profile exists - test multiple plausible handles and treat all identical responses as "uninformative", then fall back to the methods below.
- **Determine existence indirectly:**
  - Web search for `"PERSON NAME" onlyfans` and check the Linktree/other bios for an onlyfans.com link.
  - Check aggregators that mirror OF profiles (e.g. ModelSearcher - see `find-media-from-modelsearcher`), including their Wayback snapshots.
  - Wayback CDX for an archived OF profile: `curl -s "http://web.archive.org/cdx/search/cdx?url=onlyfans.com/HANDLE*&fl=timestamp,original,statuscode&limit=10"`.
- **Free preview content** (free posts, free-with-subscription teasers that show publicly) is embedded in the profile page HTML (`og:image` and the free-posts carousel), which requires a real browser session to render - plain HTTP fetches are not reliably sufficient. If a profile is confirmed to exist, a headless-browser scrape or a Wayback snapshot of the profile is the realistic path.
- Most content is paywalled - there is nothing to download for paid profiles without an account.

## Pitfalls

- **Fake/spam "watch her video" pages** built on SEO (e.g. ministrysafe-domain farm templates) use real creator names and social handles to claim leaked/OF content. They do not host the creator's real media. Treat any page that only *asserts* OF existence as junk - verify against 2+ independent sources.
- AI-generated bio sites claim OF careers for mainstream influencers; verify such claims against known biographical facts before believing them (see `shared-find-media-guidelines`).
- Do not attempt login bypasses, scraping of paywalled content, or downloading of private content.
