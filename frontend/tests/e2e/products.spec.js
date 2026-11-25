import { expect, test } from "@playwright/test";

test("fluxo completo: cadastra tarefa, altera status, valida persistencia e exclui", async ({
  page,
}) => {
  await page.goto("/");

  // 1. Cadastra nova tarefa
  await page.getByLabel(/título da tarefa/i).fill("Apresentar Projeto C216");
  await page
    .getByLabel(/descrição detalhada/i)
    .fill("Gravar vídeo demonstrativo do sistema");
  await page.getByRole("button", { name: "Cadastrar Tarefa" }).click();

  // 2. Confirma que a tarefa aparece na listagem
  const taskCard = page
    .getByRole("listitem")
    .filter({ hasText: "Apresentar Projeto C216" })
    .first();
  await expect(taskCard).toBeVisible();
  await expect(taskCard).toContainText("Apresentar Projeto C216");
  await expect(taskCard).toContainText("Pendente");

  // 3. Atualiza o status para Em Progresso
  await taskCard.getByRole("button", { name: "Iniciar" }).click();
  await expect(taskCard).toContainText("Em Progresso");

  // 4. Testa a persistência no banco recarregando a página
  await page.reload();
  const reloadedTask = page
    .getByRole("listitem")
    .filter({ hasText: "Apresentar Projeto C216" })
    .first();
  await expect(reloadedTask).toBeVisible();
  await expect(reloadedTask).toContainText("Em Progresso");

  // 5. Exclui a tarefa com confirmação
  page.on("dialog", (dialog) => dialog.accept());
  await reloadedTask.getByRole("button", { name: "Excluir" }).click();
  await expect(page.getByText("Apresentar Projeto C216")).toBeHidden();
});

test("exibe validacao ao tentar cadastrar tarefa com campos vazios", async ({
  page,
}) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Cadastrar Tarefa" }).click();

  await expect(page.getByRole("alert").first()).toBeVisible();
  await expect(page.getByRole("alert").first()).toContainText("obrigatório");
});
