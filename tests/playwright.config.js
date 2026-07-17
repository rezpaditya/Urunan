// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Smoke tests for urunan.html — the whole app is a single self-contained file
 * loaded over file://, exactly how the README says it runs. No server needed.
 */
module.exports = defineConfig({
  testDir: './smoke',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? [['list'], ['html', { open: 'never' }]] : 'list',
  use: {
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
