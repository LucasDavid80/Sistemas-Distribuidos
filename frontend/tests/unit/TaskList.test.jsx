import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, expect, it, vi } from "vitest";
import { TaskList } from "../../src/components/TaskList";

const defaultFilters = { status: "", prioridade: "", search: "" };

const makeTasks = (overrides = []) =>
  overrides.map((o, i) => ({
    id: i + 1,
    titulo: `Tarefa ${i + 1}`,
    descricao: "",
    prioridade: "MEDIA",
    status: "PENDENTE",
    categoria: "Geral",
    ...o,
  }));

beforeEach(() => vi.clearAllMocks());

it("exibe mensagem quando não há tarefas", () => {
  render(
    <TaskList
      tasks={[]}
      onStatusChange={vi.fn()}
      onEdit={vi.fn()}
      onDelete={vi.fn()}
      filters={defaultFilters}
      onFilterChange={vi.fn()}
    />,
  );
  expect(screen.getByText("Nenhuma tarefa encontrada.")).toBeInTheDocument();
});

it("renderiza lista de tarefas corretamente", () => {
  const tasks = makeTasks([
    { titulo: "Estudar React" },
    { titulo: "Estudar Vitest" },
  ]);
  render(
    <TaskList
      tasks={tasks}
      onStatusChange={vi.fn()}
      onEdit={vi.fn()}
      onDelete={vi.fn()}
      filters={defaultFilters}
      onFilterChange={vi.fn()}
    />,
  );

  expect(screen.getByText("Estudar React")).toBeInTheDocument();
  expect(screen.getByText("Estudar Vitest")).toBeInTheDocument();
});

it("mostra botão Iniciar apenas para tarefas PENDENTE", () => {
  const tasks = makeTasks([
    { titulo: "Pendente", status: "PENDENTE" },
    { titulo: "Em Progresso", status: "EM_PROGRESSO" },
    { titulo: "Concluída", status: "CONCLUIDA" },
  ]);
  render(
    <TaskList
      tasks={tasks}
      onStatusChange={vi.fn()}
      onEdit={vi.fn()}
      onDelete={vi.fn()}
      filters={defaultFilters}
      onFilterChange={vi.fn()}
    />,
  );

  expect(screen.getAllByRole("button", { name: "Iniciar" })).toHaveLength(1);
});

it("não mostra botão Concluir para tarefas já CONCLUIDA", () => {
  const tasks = makeTasks([
    { titulo: "Pendente", status: "PENDENTE" },
    { titulo: "Concluída", status: "CONCLUIDA" },
  ]);
  render(
    <TaskList
      tasks={tasks}
      onStatusChange={vi.fn()}
      onEdit={vi.fn()}
      onDelete={vi.fn()}
      filters={defaultFilters}
      onFilterChange={vi.fn()}
    />,
  );

  // Apenas a tarefa pendente deve ter o botão Concluir
  expect(screen.getAllByRole("button", { name: "Concluir" })).toHaveLength(1);
});

it("chama onStatusChange com status correto ao clicar em Iniciar", async () => {
  const user = userEvent.setup();
  const onStatusChange = vi.fn();
  const tasks = makeTasks([
    { id: 5, titulo: "Minha Tarefa", status: "PENDENTE" },
  ]);

  render(
    <TaskList
      tasks={tasks}
      onStatusChange={onStatusChange}
      onEdit={vi.fn()}
      onDelete={vi.fn()}
      filters={defaultFilters}
      onFilterChange={vi.fn()}
    />,
  );

  await user.click(screen.getByRole("button", { name: "Iniciar" }));
  expect(onStatusChange).toHaveBeenCalledWith(5, "EM_PROGRESSO");
});

it("chama onStatusChange com CONCLUIDA ao clicar em Concluir", async () => {
  const user = userEvent.setup();
  const onStatusChange = vi.fn();
  const tasks = makeTasks([
    { id: 3, titulo: "Em Progresso", status: "EM_PROGRESSO" },
  ]);

  render(
    <TaskList
      tasks={tasks}
      onStatusChange={onStatusChange}
      onEdit={vi.fn()}
      onDelete={vi.fn()}
      filters={defaultFilters}
      onFilterChange={vi.fn()}
    />,
  );

  await user.click(screen.getByRole("button", { name: "Concluir" }));
  expect(onStatusChange).toHaveBeenCalledWith(3, "CONCLUIDA");
});

it("chama onEdit ao clicar em Editar", async () => {
  const user = userEvent.setup();
  const onEdit = vi.fn();
  const task = makeTasks([{ titulo: "Para Editar" }])[0];

  render(
    <TaskList
      tasks={[task]}
      onStatusChange={vi.fn()}
      onEdit={onEdit}
      onDelete={vi.fn()}
      filters={defaultFilters}
      onFilterChange={vi.fn()}
    />,
  );

  await user.click(screen.getByRole("button", { name: "Editar" }));
  expect(onEdit).toHaveBeenCalledWith(task);
});

it("chama onDelete ao confirmar exclusão", async () => {
  const user = userEvent.setup();
  const onDelete = vi.fn().mockResolvedValue();
  vi.stubGlobal("confirm", vi.fn().mockReturnValue(true));

  const tasks = makeTasks([{ id: 9, titulo: "Para Excluir" }]);
  render(
    <TaskList
      tasks={tasks}
      onStatusChange={vi.fn()}
      onEdit={vi.fn()}
      onDelete={onDelete}
      filters={defaultFilters}
      onFilterChange={vi.fn()}
    />,
  );

  await user.click(screen.getByRole("button", { name: "Excluir" }));
  expect(onDelete).toHaveBeenCalledWith(9);

  vi.unstubAllGlobals();
});

it("não chama onDelete ao cancelar exclusão", async () => {
  const user = userEvent.setup();
  const onDelete = vi.fn();
  vi.stubGlobal("confirm", vi.fn().mockReturnValue(false));

  const tasks = makeTasks([{ titulo: "Não Excluir" }]);
  render(
    <TaskList
      tasks={tasks}
      onStatusChange={vi.fn()}
      onEdit={vi.fn()}
      onDelete={onDelete}
      filters={defaultFilters}
      onFilterChange={vi.fn()}
    />,
  );

  await user.click(screen.getByRole("button", { name: "Excluir" }));
  expect(onDelete).not.toHaveBeenCalled();

  vi.unstubAllGlobals();
});

it("chama onFilterChange ao digitar na busca", async () => {
  const user = userEvent.setup();
  const onFilterChange = vi.fn();

  render(
    <TaskList
      tasks={[]}
      onStatusChange={vi.fn()}
      onEdit={vi.fn()}
      onDelete={vi.fn()}
      filters={defaultFilters}
      onFilterChange={onFilterChange}
    />,
  );

  await user.type(screen.getByLabelText(/buscar tarefas/i), "teste");
  expect(onFilterChange).toHaveBeenCalled();
});
