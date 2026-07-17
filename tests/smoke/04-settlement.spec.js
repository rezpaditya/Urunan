// @ts-check
// Mandatory features: automatic debt settlement summary ("who pays whom")
// and settling a trip to lock further changes.
const { test, expect } = require('@playwright/test');
const { setupUser, createTrip, openTrip, addTransaction } = require('./helpers');

test('debt summary shows the minimal "who owes whom"', async ({ page }) => {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });
  await createTrip(page, { title: 'Trip', participants: ['bob@example.com'] });
  await openTrip(page, 'Trip');

  // Alice pays €10 split evenly → Bob owes Alice €5.
  await addTransaction(page, { payerName: 'Alice', title: 'Dinner', cost: 10 });

  await expect(page.locator('.summary-paid')).toContainText('€10.00');
  const debt = page.locator('.debt-line');
  await expect(debt).toContainText('Bob owes you');
  await expect(debt).toContainText('€5.00');
});

test('debt summary nets out to a minimal set across three people', async ({ page }) => {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });
  await createTrip(page, {
    title: 'Trip',
    participants: ['bob@example.com', 'carol@example.com'],
  });
  await openTrip(page, 'Trip');

  // Alice pays €30 split evenly three ways → Bob and Carol each owe €10.
  await addTransaction(page, { payerName: 'Alice', title: 'Hotel', cost: 30 });

  const lines = page.locator('.debt-line');
  await expect(lines).toHaveCount(2);
  await expect(lines.filter({ hasText: 'Bob owes you' })).toContainText('€10.00');
  await expect(lines.filter({ hasText: 'Carol owes you' })).toContainText('€10.00');
});

test('a fully balanced trip reports "all settled up"', async ({ page }) => {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });
  await createTrip(page, { title: 'Trip', participants: ['bob@example.com'] });
  await openTrip(page, 'Trip');

  // Each pays their own €5 share of their own €5 expense → nobody owes anyone.
  await addTransaction(page, {
    payerName: 'Alice', title: 'Alice lunch', cost: 5, splits: { Alice: 5, Bob: 0 },
  });
  await addTransaction(page, {
    payerName: 'Bob', title: 'Bob lunch', cost: 5, splits: { Alice: 0, Bob: 5 },
  });

  await expect(page.locator('.debt-line')).toContainText('All settled up');
});

test('settling a trip marks it Settled and blocks new transactions', async ({ page }) => {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });
  await createTrip(page, { title: 'Trip', participants: ['bob@example.com'] });
  await openTrip(page, 'Trip');
  await addTransaction(page, { payerName: 'Alice', title: 'Dinner', cost: 10 });

  page.on('dialog', (d) => d.accept()); // accept the settle confirmation
  await page.getByRole('button', { name: /Settle Trip/ }).click();

  await expect(page.locator('.badge-settled')).toBeVisible();
  // The add-transaction toggle and per-transaction edit/delete actions disappear.
  await expect(page.getByRole('button', { name: /Add Transaction/ })).toHaveCount(0);
  await expect(page.locator('.tx-actions')).toHaveCount(0);
});
