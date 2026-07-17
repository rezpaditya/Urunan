# agent.md — .github/workflows

GitHub Actions workflows.

## Files

- `github-pages.yml` — Publishes the app to GitHub Pages. On a push to `main`
  that changes `urunan.html` (or manual `workflow_dispatch`), it copies
  `urunan.html` into the `gh-pages` branch as `index.html` and pushes. GitHub
  Pages then serves the site from `gh-pages`, and its built-in "pages build and
  deployment" workflow publishes the push.

## Notes

- Pages deploys **only** from the `gh-pages` branch (enforced by the
  `github-pages` environment), which is why this workflow copies the file
  across rather than deploying directly from `main`.
- Don't hand-edit `gh-pages`; let this workflow keep it in sync.
- The workflow is a no-op commit when the file is unchanged (`git diff
  --cached --quiet` guard), so re-runs are safe.
