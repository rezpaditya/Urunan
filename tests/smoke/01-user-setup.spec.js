// @ts-check
// Mandatory feature: one-time user setup + local persistence.
const { test, expect } = require('@playwright/test');
const { APP_URL, setupUser } = require('./helpers');

test('new user completes setup and lands on the trips screen', async ({ page }) => {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });

  await expect(page.locator('.topbar-name')).toContainText('Alice');
  await expect(page.locator('.topbar-email')).toHaveText('alice@example.com');
  await expect(page.getByRole('button', { name: /Create New Trip/ })).toBeVisible();
});

test('the logged-in user survives a page reload (localStorage persistence)', async ({ page }) => {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });

  await page.reload();

  // No setup form on reload — the saved user is restored straight to trips.
  await expect(page.getByPlaceholder('Your name')).toHaveCount(0);
  await expect(page.locator('.topbar-name')).toContainText('Alice');
});

test('email is stored lowercased and normalized', async ({ page }) => {
  await setupUser(page, { name: 'Alice', email: '  Alice@Example.COM  ' });

  const stored = await page.evaluate(() =>
    JSON.parse(localStorage.getItem('urunan_user'))
  );
  expect(stored.email).toBe('alice@example.com');
  expect(stored.name).toBe('Alice');
});
