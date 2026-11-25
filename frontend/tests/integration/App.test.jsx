import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import App from "../../src/App";

let mockTasks = [];

beforeEach(() => {
  mockTasks = [];
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation((url, options = {}) => {
      const urlStr = String(url);

      if (urlStr.includes("/tasks/metrics")) {
        const total = mockTasks.length;
        const pendentes = mockTasks.filter(
          (t) => t.status === "PENDENTE",
        ).length;
        const em_progresso = mockTasks.filter(
          (t) => t.status === "EM_PROGRESSO",
        ).length;
        const concluidas = mockTasks.filter(
          (t) => t.status === "CONCLUIDA",
        ).length;
        const taxa_conclusao =
          total > 0 ? Math.round((concluidas / total) * 100) : 0;
        return Promise.resolve(
          new Response(
            JSON.stringify({
              total,
              pendentes,
              em_progresso,
              concluidas,
              taxa_conclusao,
            }),
            { status: 200, headers: { "Content-Type": "application/json" } },
          ),
        );
      }

      if (options.method === "POST" && urlStr.includes("/tasks/")) {
        const body = options.body ? JSON.parse(options.body) : {};
        const newTask = {
          id: mockTasks.length + 1,
          titulo: body.titulo ?? "Nova Tarefa",
          descricao: body.descricao ?? "",
          prioridade: body.prioridade ?? "MEDIA",
          status: body.status ?? "PENDENTE",
          categoria: body.categoria ?? "Geral",
          user_id: 1,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };
        mockTasks.push(newTask);
        return Promise.resolve(
          new Response(JSON.stringify(newTask), {
            status: 201,
            headers: { "Content-Type": "application/json" },
          }),
        );
      }

      if (options.method === "PATCH" && urlStr.includes("/status")) {
        const body = options.body ? JSON.parse(options.body) : {};
        const match = urlStr.match(/\/tasks\/(\d+)\/status/);
        const id = match ? Number(match[1]) : 1;
        const task = mockTasks.find((t) => t.id === id);
        if (task) {
          task.status = body.status;
        }
        return Promise.resolve(
          new Response(JSON.stringify(task), {
            status: 200,
            headers: { "Content-Type": "application/json" },
          }),
        );
      }

      if (options.method === "DELETE" && urlStr.includes("/tasks/")) {
        const match = urlStr.match(/\/tasks\/(\d+)/);
        const id = match ? Number(match[1]) : 1;
        mockTasks = mockTasks.filter((t) => t.id !== id);
        return Promise.resolve(new Response(null, { status: 204 }));
      }

      return Promise.resolve(
        new Response(JSON.stringify(mockTasks), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      );
    }),
  );
});

afterEach(() => vi.unstubAllGlobals());

it("cria uma tarefa, exibe na lista, atualiza métricas e permite alterar status", async () => {
  const user = userEvent.setup();
  render(<App />);

  // Espera carregar tela
  expect(
    await screen.findByText("Nenhuma tarefa encontrada."),
  ).toBeInTheDocument();

  // Preenche o formulário
  await user.type(
    screen.getByLabelText(/título da tarefa/i),
    "Criar testes E2E",
  );
  await user.type(
    screen.getByLabelText(/descrição detalhada/i),
    "Testes com Playwright",
  );
  await user.click(screen.getByRole("button", { name: "Cadastrar Tarefa" }));

  // Verifica se a tarefa apareceu na lista
  expect(await screen.findByText("Criar testes E2E")).toBeInTheDocument();
  expect(screen.getByText("Testes com Playwright")).toBeInTheDocument();

  // Verifica métrica
  expect(screen.getByTestId("metric-total")).toHaveTextContent("1");
  expect(screen.getByTestId("metric-pendentes")).toHaveTextContent("1");

  // Inicia a tarefa
  const startBtn = screen.getByRole("button", { name: "Iniciar" });
  await user.click(startBtn);

  // Status atualizado
  expect(
    await screen.findByText("Status da tarefa atualizado!"),
  ).toBeInTheDocument();
  expect(screen.getByTestId("metric-em-progresso")).toHaveTextContent("1");
});
