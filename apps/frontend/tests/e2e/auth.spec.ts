import { test, expect } from '@playwright/test';

test.describe('Auth flow (mock mode)', () => {
  test('login redirects to dashboard and shows verification gate', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: /log in/i }).first().click();

    await page.getByLabel(/email/i).fill('mockuser@example.com');
    await page.getByLabel(/^password$/i).fill('password123');
    await page.getByRole('button', { name: /continue with email/i }).click();

    await page.waitForURL('**/dashboard');
    await expect(page.getByText(/verify your email to enable uploads/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /go to upload/i })).toBeDisabled();
  });

  test('signup enforces matching passwords and reaches dashboard', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('button', { name: /sign up/i }).first().click();

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

  test('invalid login shows inline error', async ({ page }) => {
    await page.route('**/auth/login', (route) =>
      route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ detail: 'Invalid credentials' }),
      }),
    );

    await page.goto('/');
    await page.getByRole('button', { name: /log in/i }).first().click();
    await page.getByLabel(/email/i).fill('fail@example.com');
    await page.getByLabel(/^password$/i).fill('wrongpass');
    await page.getByRole('button', { name: /continue with email/i }).click();

    await expect(page.getByText(/invalid credentials/i)).toBeVisible();
  });

  test('refresh keeps session on dashboard when tokens are valid', async ({ page, context }) => {
    // Stub login success
    await page.route('**/auth/login', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          user: { id: 'u1', email: 'kept@example.com', verified: true },
          needsVerification: false,
        }),
        headers: {
          'set-cookie': [
            'access_token=dummy; Path=/; HttpOnly',
            'refresh_token=dummy; Path=/; HttpOnly',
            'XSRF-TOKEN=dummy; Path=/',
          ],
        },
      }),
    );
    // Stub refresh success
    await page.route('**/auth/refresh', (route) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          user: { id: 'u1', email: 'kept@example.com', verified: true },
          needsVerification: false,
        }),
        headers: {
          'set-cookie': [
            'access_token=new; Path=/; HttpOnly',
            'refresh_token=new; Path=/; HttpOnly',
            'XSRF-TOKEN=dummy; Path=/',
          ],
        },
      }),
    );

    await page.goto('/');
    await page.getByRole('button', { name: /log in/i }).first().click();
    await page.getByLabel(/email/i).fill('kept@example.com');
    await page.getByLabel(/^password$/i).fill('password123');
    await page.getByRole('button', { name: /continue with email/i }).click();
    await page.waitForURL('**/dashboard');
    await expect(page).toHaveURL(/dashboard/);

    // Reload triggers refresh; expect still on dashboard
    await page.reload();
    await page.waitForTimeout(200);
    await expect(page).toHaveURL(/dashboard/);
  });
});
