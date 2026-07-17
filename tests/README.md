# Smoke tests

End-to-end smoke tests for [`urunan.html`](../urunan.html). They drive the app
exactly the way it ships — a single self-contained file loaded over a `file://`
URL, no server, no build step — using [Playwright](https://playwright.dev) and
Chromium. One spec covers each mandatory feature; each test is a thin
happy-path check that the feature is wired up and works, not an exhaustive
unit suite.

| Spec                       | Mandatory feature it smoke-tests                                        |
| -------------------------- | ----------------------------------------------------------------------- |
| `01-user-setup.spec.js`    | One-time user setup and `localStorage` persistence across reloads.      |
| `02-trips.spec.js`         | Creating a trip with multiple participants.                             |
| `03-transactions.spec.js`  | Transactions with even-by-default and custom splits, validated totals.  |
| `04-settlement.spec.js`    | The "who owes whom" debt summary and settling a trip (locks it).        |
| `05-share-link.spec.js`    | Sharing a trip via a link and merging on import without duplicates.     |

Optional live device sync is intentionally **not** covered: it is off by
default, requires a running relay, and isn't a mandatory feature.

## Running

```bash
cd tests
npm install          # installs @playwright/test
npx playwright install chromium   # first run only, to fetch the browser
npm test
```

The tests open `urunan.html` directly from disk, so no local server is needed.
