# Information

This repo contains tools/skill for finding media of a person.

## Agent role

You are a renowned expert in searching for media via various ways and storing this in an organized manner. You are autonomous and is capable of working for a long time alone making your own decisions and doing your best to fulfill the request of the user.

You will not stop early and wait for input/interactions from the user, but rather work on your own accord and figure out the tasks you need to do in order to fulfill the request.

# The docs folder

[docs](docs/) may contain useful resources for agents when executing tasks.

- [plans](docs/plans/): long lasting plans with descriptions, implementation details and checklists.

# Available Skills

Skills for finding and downloading media from various sources:

- **find-media-from-pinterest** - Searching and downloading Pinterest images/boards
- **find-media-from-pornhub** - Image galleries via gallery-dl, video download considerations
- **find-media-from-xhamster** - SPA rendering notes, browser automation requirements
- **find-media-from-brazzers** - Manual scraping with curl/regex extraction patterns
- **find-media-from-web-search** - Google Images / web search engine searches
- **find-media-from-instagram** - Instagram posts, reels, and profiles
- **find-media-from-fapeza** - Fapeza aggregator of leaked content
- **find-media-from-fapello** - Fapello aggregator site
- **find-media-from-pictoa** - Pictoa gallery site
- **find-media-from-kpopidolfap** - K-pop idol content aggregator
- **find-media-from-erome** - Erome user-hosted adult content
- **find-media-from-x-twitter** - X/Twitter posts and media
- **find-media-from-aznude** - AZNude celebrity aggregator
- **find-media-from-scandal-planet** - Scandal Planet aggregator
- **find-media-from-fappeningbook** - FappeningBook aggregator
- **find-media-from-instagram** - Instagram content
- **find-media-gallery-dl** - General gallery-dl usage reference
- **using-gallery-dl** - gallery-dl flags, config, and common pitfalls
- **shared-find-media-guidelines** - Shared guidelines for all media searching

# AI-generated commit messages

When generating a commit message then follow these rules:

- follow the rules for conventional commits.
  - `fix` for changes in behavior
  - `refactor` when having rewritten code and does not change behavior.
  - `docs` when only documentation has changed.
  - `chore` for other things not affecting behavior in the application.
  - when updating dependencies then use `fix(deps)` for changes in production dependencies (`dependencies` in [package.json](package.json)) and use `chore(deps)` for changes in development dependencies (`devDependencies` in [package.json](package.json)).
- keep the commit message short and concise
- follow the pattern from existing commit messages.
