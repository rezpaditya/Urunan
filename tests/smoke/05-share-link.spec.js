// @ts-check
// Mandatory feature: share a trip between devices with a link (no server) —
// the trip data travels in the URL fragment and merges on import without
// duplicating anything on repeat imports.
const { test, expect } = require('@playwright/test');
const { APP_URL, setupUser, createTrip, openTrip, addTransaction } = require('./helpers');

// Build a share link on device A (Alice), then return it.
async function makeShareLink(page) {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });
  await createTrip(page, { title: 'Shared Trip', participants: ['bob@example.com'] });
  await openTrip(page, 'Shared Trip');
  await addTransaction(page, { payerName: 'Alice', title: 'Dinner', cost: 10 });

  await page.getByRole('button', { name: /Share/ }).click();
  // Reveal the one-time link/QR export (device sync is the default primary UI).
  await page.getByRole('button', { name: /One-time link/ }).click();
  const shareInput = page.locator('.modal input[readonly]');
  const url = await shareInput.inputValue();
  expect(url).toContain('#trip=');
  return url;
}

test('a shared link carries a trip that imports on another device', async ({ page }) => {
  const shareUrl = await makeShareLink(page);

  // Simulate a second device: Bob, fresh storage, opens the link.
  await setupUser(page, { name: 'Bob', email: 'bob@example.com' });
  page.on('dialog', (d) => d.accept()); // the "imported ✓" alert
  await page.goto(shareUrl);

  await expect(page.locator('.trip-card', { hasText: 'Shared Trip' })).toBeVisible();
  await page.locator('.trip-card', { hasText: 'Shared Trip' }).click();
  await expect(page.locator('.tx-card', { hasText: 'Dinner' })).toBeVisible();
  await expect(page.locator('.tx-amount')).toHaveText('€10.00');
});

test('re-importing the same link does not duplicate data', async ({ page }) => {
  const shareUrl = await makeShareLink(page);

  await setupUser(page, { name: 'Bob', email: 'bob@example.com' });
  page.on('dialog', (d) => d.accept());

  await page.goto(shareUrl);
  await expect(page.locator('.trip-card', { hasText: 'Shared Trip' })).toBeVisible();

  // Import the very same link a second time.
  await page.goto(shareUrl);

  // Still exactly one trip card and, inside it, one transaction.
  await expect(page.locator('.trip-card', { hasText: 'Shared Trip' })).toHaveCount(1);
  await page.locator('.trip-card', { hasText: 'Shared Trip' }).click();
  await expect(page.locator('.tx-card')).toHaveCount(1);
});
