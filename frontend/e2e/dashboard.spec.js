import { test, expect } from "@playwright/test"

test.describe("Saturn dashboard", () => {

  test("loads and reaches ready state", async ({ page }) => {
    await page.goto("/")
    await expect(page).toHaveTitle(/./)
    await expect(page.locator("body")).not.toContainText("Cannot GET")
  })

  test("displays a trading signal", async ({ page }) => {
    await page.goto("/")
    const badge = page.locator(".signal-badge")
    await expect(badge).toBeVisible({ timeout: 20000 })
    await expect(badge).not.toHaveClass(/signal-badge--empty/)
    await expect(badge.locator(".signal-badge__label")).toHaveText(/BUY|SELL|HOLD/)
  })

  test("displays sentiment headlines", async ({ page }) => {
    await page.goto("/")
    const feed = page.locator(".feed-list")
    await expect(feed).toBeVisible({ timeout: 20000 })
    await expect(feed).not.toHaveClass(/feed-list--state/)
    await expect(feed.locator(".feed-item").first()).toBeVisible()
  })

  test("renders the price chart", async ({ page }) => {
    await page.goto("/")
    const chart = page.locator(".price-chart")
    await expect(chart).toBeVisible({ timeout: 20000 })
    await expect(chart).not.toHaveClass(/price-chart--empty/)
  })

  test("AI explain panel streams a response", async ({ page }) => {
    await page.goto("/")

    const askBtn = page.locator(".ai-panel__btn")
    await expect(askBtn).toBeEnabled({ timeout: 20000 })
    await expect(askBtn).toHaveText("✦ Ask Saturn AI")

    await askBtn.click()

    await expect(askBtn).toHaveText("⏹ Stop Analysis")
    await expect(page.locator(".ai-panel__output")).toBeVisible({ timeout: 30000 })

    await expect(askBtn).toHaveText("✦ Ask Saturn AI", { timeout: 60000 })
  })

})