// @ts-check
// Mandatory feature: trips with multiple participants.
const { test, expect } = require('@playwright/test');
const { setupUser, createTrip, openTrip } = require('./helpers');

test('create a trip with multiple participants', async ({ page }) => {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });

  await createTrip(page, {
    title: 'Bali 2025',
    participants: ['bob@example.com', 'carol@example.com'],
  });

  // The trip appears on the list with the correct participant count
  // (creator + 2 invited = 3).
  const card = page.locator('.trip-card', { hasText: 'Bali 2025' });
  await expect(card).toBeVisible();
  await expect(card.locator('.trip-card-meta')).toContainText('👥 3');
});

test('opening a trip shows every participant by name', async ({ page }) => {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });
  await createTrip(page, {
    title: 'Bali 2025',
    participants: ['bob@example.com', 'carol@example.com'],
  });

  await openTrip(page, 'Bali 2025');

  const chips = page.locator('.participant-chip');
  await expect(chips).toHaveCount(3);
  await expect(chips.filter({ hasText: 'Alice' })).toHaveCount(1);
  await expect(chips.filter({ hasText: 'Bob' })).toHaveCount(1);
  await expect(chips.filter({ hasText: 'Carol' })).toHaveCount(1);
});

test('created trips persist across a reload', async ({ page }) => {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });
  await createTrip(page, { title: 'Weekend Trip', participants: ['bob@example.com'] });

  await page.reload();

  await expect(page.locator('.trip-card', { hasText: 'Weekend Trip' })).toBeVisible();
});
