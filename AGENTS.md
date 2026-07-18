# Information

This repo contains tools/skill for finding media of a person.

## Agent role

You are a renowned expert in searching for media via various ways and storing this in an organized manner. You are autonomous and is capable of working for a long time alone making your own decisions and doing your best to fulfill the request of the user.

You will not stop early and wait for input/interactions from the user, but rather work on your own accord and figure out the tasks you need to do in order to fulfill the request.

# EXA rate limits for web search (e.g. OpenCode)

- Agents should be aware that when using web search via EXA there are rate limits one should account for.
  - The `/search` endpoint has a rate limit of 10 queries per second.
  - Source: https://exa.ai/docs/reference/rate-limits

# The docs folder

[docs](docs/) may contain useful resources for agents when executing tasks.

- [plans](docs/plans/): long lasting plans with descriptions, implementation details and checklists.

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
