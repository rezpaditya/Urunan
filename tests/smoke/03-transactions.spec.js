// @ts-check
// Mandatory feature: transactions with payment splits — even by default,
// adjustable per person, validated against the total.
const { test, expect } = require('@playwright/test');
const { setupUser, createTrip, openTrip, addTransaction } = require('./helpers');

async function twoPersonTrip(page) {
  await setupUser(page, { name: 'Alice', email: 'alice@example.com' });
  await createTrip(page, { title: 'Trip', participants: ['bob@example.com'] });
  await openTrip(page, 'Trip');
}

test('adding a transaction defaults to an even split', async ({ page }) => {
  await twoPersonTrip(page);

  // Open the form and enter a cost; the even split should prefill each row.
  await page.getByRole('button', { name: /Add Transaction/ }).click();
  const form = page.locator('.card-form form');
  await form.locator('select').selectOption({ label: 'Alice' });
  await form.getByPlaceholder('What was it for?').fill('Dinner');
  await form.getByPlaceholder('0.00').first().fill('10');

  const splitInputs = form.locator('.split-row input');
  await expect(splitInputs).toHaveCount(2);
  await expect(splitInputs.nth(0)).toHaveValue('5');
  await expect(splitInputs.nth(1)).toHaveValue('5');

  await form.getByRole('button', { name: 'Add Transaction' }).click();

  const tx = page.locator('.tx-card', { hasText: 'Dinner' });
  await expect(tx.locator('.tx-amount')).toHaveText('€10.00');
  await expect(tx.locator('.tx-payer')).toContainText('Paid by Alice');
  await expect(tx.locator('.tx-split')).toHaveText([/Alice: €5\.00/, /Bob: €5\.00/]);
});

test('a custom (uneven) split is saved as entered', async ({ page }) => {
  await twoPersonTrip(page);

  await addTransaction(page, {
    payerName: 'Alice',
    title: 'Taxi',
    cost: 10,
    splits: { Alice: 2, Bob: 8 },
  });

  const tx = page.locator('.tx-card', { hasText: 'Taxi' });
  await expect(tx.locator('.tx-split')).toHaveText([/Alice: €2\.00/, /Bob: €8\.00/]);
});

test('an under-allocated split is rejected (validated against the total)', async ({ page }) => {
  await twoPersonTrip(page);

  await page.getByRole('button', { name: /Add Transaction/ }).click();
  const form = page.locator('.card-form form');
  await form.locator('select').selectOption({ label: 'Alice' });
  await form.getByPlaceholder('What was it for?').fill('Broken split');
  await form.getByPlaceholder('0.00').first().fill('10');

  // Under-allocate: only €4 of €10 assigned.
  const splitInputs = form.locator('.split-row input');
  await splitInputs.nth(0).fill('2');
  await splitInputs.nth(1).fill('2');

  await expect(form.locator('.field-error')).toContainText('left to allocate');
  const submit = form.getByRole('button', { name: 'Add Transaction' });
  await expect(submit).toBeDisabled();
});

test('an over-allocated split is rejected', async ({ page }) => {
  await twoPersonTrip(page);

  await page.getByRole('button', { name: /Add Transaction/ }).click();
  const form = page.locator('.card-form form');
  await form.locator('select').selectOption({ label: 'Alice' });
  await form.getByPlaceholder('What was it for?').fill('Too much');
  await form.getByPlaceholder('0.00').first().fill('10');

  const splitInputs = form.locator('.split-row input');
  await splitInputs.nth(0).fill('9');
  await splitInputs.nth(1).fill('9');

  await expect(form.locator('.field-error')).toContainText('Over-allocated');
  await expect(form.getByRole('button', { name: 'Add Transaction' })).toBeDisabled();
});

test('"Split evenly" restores an even split after manual edits', async ({ page }) => {
  await twoPersonTrip(page);

  await page.getByRole('button', { name: /Add Transaction/ }).click();
  const form = page.locator('.card-form form');
  await form.locator('select').selectOption({ label: 'Alice' });
  await form.getByPlaceholder('What was it for?').fill('Groceries');
  await form.getByPlaceholder('0.00').first().fill('10');

  const splitInputs = form.locator('.split-row input');
  await splitInputs.nth(0).fill('9');
  await splitInputs.nth(1).fill('1');

  await form.getByRole('button', { name: /Split evenly/ }).click();
  await expect(splitInputs.nth(0)).toHaveValue('5');
  await expect(splitInputs.nth(1)).toHaveValue('5');
});
