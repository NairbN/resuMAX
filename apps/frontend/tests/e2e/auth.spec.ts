import { test, expect } from '@playwright/test';

test.describe('Auth flow (mock mode)', () => {
  test('login redirects to dashboard and shows verification gate', async ({ page }) => {
    await page.goto('/login');

    await page.getByLabel(/email/i).fill('mockuser@example.com');
    await page.getByLabel(/^password$/i).fill('password123');
    await page.getByRole('button', { name: /continue with email/i }).click();

    await page.waitForURL('**/dashboard');
    await expect(page.getByText(/verify your email to enable uploads/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /go to upload/i })).toBeDisabled();
  });

  test('signup enforces matching passwords and reaches dashboard', async ({ page }) => {
    await page.goto('/register');

    await page.getByLabel(/email/i).fill('newuser@example.com');
    await page.getByLabel(/^password$/i).fill('password123');
    await page.getByLabel(/confirm password/i).fill('different');
    await page.getByRole('button', { name: /continue with email/i }).click();
    await expect(page.getByText(/passwords must match/i)).toBeVisible();

    await page.getByLabel(/confirm password/i).fill('password123');
    await page.getByRole('button', { name: /continue with email/i }).click();

    await page.waitForURL('**/dashboard');
    await expect(page.getByRole('button', { name: /go to upload/i })).toBeDisabled();
  });
});
