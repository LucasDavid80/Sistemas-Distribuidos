import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, expect, it, vi } from "vitest";
import { TaskForm } from "../../src/components/TaskForm";

beforeEach(() => {
  vi.clearAllMocks();
});

it("exibe erros de validação ao submeter formulário vazio", async () => {
  const user = userEvent.setup();
  const onSave = vi.fn();
  render(
    <TaskForm onSave={onSave} editingTask={null} onCancelEdit={vi.fn()} />,
  );

  await user.click(screen.getByRole("button", { name: "Cadastrar Tarefa" }));

  expect(screen.getByRole("alert")).toBeInTheDocument();
  expect(screen.getByText(/obrigatório/i)).toBeInTheDocument();
  expect(onSave).not.toHaveBeenCalled();
});

it("chama onSave com os dados corretos ao submeter formulário válido", async () => {
  const user = userEvent.setup();
  const onSave = vi.fn().mockResolvedValue();
  render(
    <TaskForm onSave={onSave} editingTask={null} onCancelEdit={vi.fn()} />,
  );

  await user.type(screen.getByLabelText(/título da tarefa/i), "Minha Tarefa");
  await user.type(
    screen.getByLabelText(/descrição detalhada/i),
    "Uma descrição",
  );
  await user.click(screen.getByRole("button", { name: "Cadastrar Tarefa" }));

  await waitFor(() => expect(onSave).toHaveBeenCalledOnce());
  expect(onSave).toHaveBeenCalledWith(
    expect.objectContaining({
      titulo: "Minha Tarefa",
      descricao: "Uma descrição",
    }),
    undefined,
  );
});

it("limpa o formulário após salvar com sucesso", async () => {
  const user = userEvent.setup();
  const onSave = vi.fn().mockResolvedValue();
  render(
    <TaskForm onSave={onSave} editingTask={null} onCancelEdit={vi.fn()} />,
  );

  const input = screen.getByLabelText(/título da tarefa/i);
  await user.type(input, "Tarefa para limpar");
  await user.click(screen.getByRole("button", { name: "Cadastrar Tarefa" }));

  await waitFor(() => expect(input).toHaveValue(""));
});

it("exibe erro de submit quando onSave lança exceção", async () => {
  const user = userEvent.setup();
  const onSave = vi.fn().mockRejectedValue(new Error("Falha na API"));
  render(
    <TaskForm onSave={onSave} editingTask={null} onCancelEdit={vi.fn()} />,
  );

  await user.type(
    screen.getByLabelText(/título da tarefa/i),
    "Tarefa com erro",
  );
  await user.click(screen.getByRole("button", { name: "Cadastrar Tarefa" }));

  expect(await screen.findByText("Falha na API")).toBeInTheDocument();
});

it("preenche os campos quando editingTask é fornecido", () => {
  const editingTask = {
    id: 42,
    titulo: "Tarefa Existente",
    descricao: "Desc existente",
    prioridade: "ALTA",
    status: "EM_PROGRESSO",
    categoria: "Backend",
  };
  render(
    <TaskForm
      onSave={vi.fn()}
      editingTask={editingTask}
      onCancelEdit={vi.fn()}
    />,
  );

  expect(screen.getByLabelText(/título da tarefa/i)).toHaveValue(
    "Tarefa Existente",
  );
  expect(screen.getByLabelText(/descrição detalhada/i)).toHaveValue(
    "Desc existente",
  );
  expect(
    screen.getByRole("button", { name: "Atualizar Tarefa" }),
  ).toBeInTheDocument();
  expect(
    screen.getByRole("button", { name: "Cancelar Edição" }),
  ).toBeInTheDocument();
});

it("chama onCancelEdit ao clicar em Cancelar Edição", async () => {
  const user = userEvent.setup();
  const onCancelEdit = vi.fn();
  const editingTask = {
    id: 1,
    titulo: "Tarefa",
    descricao: "",
    prioridade: "MEDIA",
    status: "PENDENTE",
    categoria: "Geral",
  };
  render(
    <TaskForm
      onSave={vi.fn()}
      editingTask={editingTask}
      onCancelEdit={onCancelEdit}
    />,
  );

  await user.click(screen.getByRole("button", { name: "Cancelar Edição" }));
  expect(onCancelEdit).toHaveBeenCalledOnce();
});

it("chama onSave com id ao editar tarefa existente", async () => {
  const user = userEvent.setup();
  const onSave = vi.fn().mockResolvedValue();
  const editingTask = {
    id: 7,
    titulo: "Título Antigo",
    descricao: "",
    prioridade: "BAIXA",
    status: "PENDENTE",
    categoria: "Geral",
  };
  render(
    <TaskForm
      onSave={onSave}
      editingTask={editingTask}
      onCancelEdit={vi.fn()}
    />,
  );

  const input = screen.getByLabelText(/título da tarefa/i);
  await user.clear(input);
  await user.type(input, "Título Atualizado");
  await user.click(screen.getByRole("button", { name: "Atualizar Tarefa" }));

  await waitFor(() => expect(onSave).toHaveBeenCalledOnce());
  expect(onSave).toHaveBeenCalledWith(
    expect.objectContaining({ titulo: "Título Atualizado" }),
    7,
  );
});
