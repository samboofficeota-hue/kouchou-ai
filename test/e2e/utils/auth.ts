import type { Page } from "@playwright/test";

/**
 * Basic認証のヘッダーを設定する
 */
export async function setupBasicAuth(page: Page): Promise<void> {
  const username = process.env.BASIC_AUTH_USERNAME || "test_user";
  const password = process.env.BASIC_AUTH_PASSWORD || "test_password";

  await page.setExtraHTTPHeaders({
    Authorization: `Basic ${Buffer.from(`${username}:${password}`).toString("base64")}`,
  });
}
