# agent.md — .github

GitHub configuration for the repository.

## Contents

- `workflows/` — GitHub Actions workflows. Currently just the GitHub Pages
  publisher for `urunan.html`.

## Notes

- The only active automation here publishes the app to GitHub Pages. See
  `workflows/agent.md` for details.
- Keep automation minimal — the app has no build step, so CI stays lightweight.
