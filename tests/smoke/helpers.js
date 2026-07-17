// @ts-check
const path = require('path');
const { pathToFileURL } = require('url');

// file:// URL to the app under test — the app is a single self-contained file.
const APP_URL = pathToFileURL(
  path.join(__dirname, '..', '..', 'urunan.html')
).href;

/**
 * Load the app fresh (clean localStorage) and complete the one-time user setup
 * so tests start on the trip-list screen as a logged-in user.
 */
async function setupUser(page, { name = 'Alice', email = 'alice@example.com' } = {}) {
  await page.goto(APP_URL);
  await page.evaluate(() => localStorage.clear());
  await page.reload();

  await page.getByPlaceholder('Your name').fill(name);
  await page.getByPlaceholder('your@email.com').fill(email);
  await page.getByRole('button', { name: /Get Started/ }).click();

  // We should now be on the trips screen.
  await page.getByRole('button', { name: /Create New Trip/ }).waitFor();
  return { name, email };
}

/**
 * Create a trip with the given title and participant emails (besides the
 * current user, who is added automatically).
 */
async function createTrip(page, { title, participants = [] } = {}) {
  await page.getByRole('button', { name: /Create New Trip/ }).click();
  await page.getByPlaceholder(/Trip name/).fill(title);
  for (const email of participants) {
    await page.getByPlaceholder('friend@email.com').fill(email);
    await page.getByRole('button', { name: 'Add', exact: true }).click();
  }
  await page.getByRole('button', { name: 'Save Trip' }).click();
  await tripCard(page, title).waitFor();
}

/**
 * The trip-list card whose name is exactly `title` (exact match so a title
 * like "Trip" doesn't collide with static UI text such as "Your Trips").
 */
function tripCard(page, title) {
  return page
    .locator('.trip-card')
    .filter({ has: page.getByText(title, { exact: true }) });
}

/**
 * Open a trip from the trip list by its title.
 */
async function openTrip(page, title) {
  await tripCard(page, title).locator('.trip-card-body').click();
  await page.getByRole('button', { name: /Back/ }).waitFor();
}

/**
 * Add a transaction. `splits` (optional) is a map of email -> amount for a
 * custom split; when omitted the default even split is used.
 */
async function addTransaction(page, { payerName, title, cost, splits = null }) {
  await page.getByRole('button', { name: /Add Transaction/ }).click();
  const form = page.locator('.card-form form');
  await form.locator('select').selectOption({ label: payerName });
  await form.getByPlaceholder('What was it for?').fill(title);
  await form.getByPlaceholder('0.00').first().fill(String(cost));

  if (splits) {
    const rows = form.locator('.split-row');
    const n = await rows.count();
    for (let i = 0; i < n; i++) {
      const label = (await rows.nth(i).locator('.split-name').innerText()).trim();
      if (splits[label] != null) {
        await rows.nth(i).locator('input').fill(String(splits[label]));
      }
    }
  }
  await form.getByRole('button', { name: 'Add Transaction' }).click();
}

module.exports = { APP_URL, setupUser, createTrip, tripCard, openTrip, addTransaction };
