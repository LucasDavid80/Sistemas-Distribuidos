import { expect, test } from "@playwright/test";

test("vendedor publica um produto que fica visível para compradores", async ({
  page,
}) => {
  await page.goto("/");

  await page.getByRole("button", { name: /sou vendedor/i }).click();
  await page.getByLabel("Nome do produto").fill("Notebook");
  await page.getByLabel("Descrição").fill("14 polegadas");
  await page.getByLabel("Preço (R$)").fill("3499.90");
  await page.getByLabel("Estoque").fill("3");
  await page.getByRole("button", { name: "Publicar produto" }).click();
  await expect(page.getByLabel("Nome do produto")).toHaveValue("");
  await page.getByRole("button", { name: /voltar ao início/i }).click();
  await page.getByRole("button", { name: /sou comprador/i }).click();

  const notebook = page
    .getByRole("listitem")
    .filter({ hasText: "Notebook" })
    .first();
  await expect(notebook).toContainText("Notebook");
  await expect(
    page.getByText("Ainda não há produtos anunciados."),
  ).toBeHidden();

  await page.reload();
  await page.getByRole("button", { name: /sou comprador/i }).click();
  await expect(
    page.getByRole("listitem").filter({ hasText: "Notebook" }).first(),
  ).toContainText("Notebook");
});

test("exibe validação ao tentar publicar sem dados", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: /sou vendedor/i }).click();
  await page.getByRole("button", { name: "Publicar produto" }).click();

  await expect(page.getByRole("alert").first()).toBeVisible();
});
