import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import App from "../../src/App";

let mockProducts = [];

beforeEach(() => {
  mockProducts = [];
  vi.stubGlobal(
    "fetch",
    vi.fn().mockImplementation((_, options = {}) => {
      if (options.method === "POST") {
        const body = options.body ? JSON.parse(options.body) : {};
        const newProduct = {
          id: mockProducts.length + 1,
          nome: body.nome ?? "Notebook",
          descricao: body.descricao ?? "14 polegadas",
          preco: body.preco ?? 3499.9,
          estoque: body.estoque ?? 3,
          seller_id: 1,
        };
        mockProducts.push(newProduct);
        return Promise.resolve(
          new Response(JSON.stringify(newProduct), {
            status: 201,
            headers: { "Content-Type": "application/json" },
          }),
        );
      }
      return Promise.resolve(
        new Response(JSON.stringify(mockProducts), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      );
    }),
  );
});

afterEach(() => vi.unstubAllGlobals());

it("permite que um vendedor publique um produto para compradores", async () => {
  const user = userEvent.setup();
  render(<App />);

  await user.click(screen.getByRole("button", { name: /sou vendedor/i }));
  await user.type(screen.getByLabelText("Nome do produto"), "Notebook");
  await user.type(screen.getByLabelText("Descrição"), "14 polegadas");
  await user.type(screen.getByLabelText("Preço (R$)"), "3499.90");
  await user.type(screen.getByLabelText("Estoque"), "3");
  await user.click(screen.getByRole("button", { name: "Publicar produto" }));
  await user.click(screen.getByRole("button", { name: /voltar ao início/i }));
  await user.click(screen.getByRole("button", { name: /sou comprador/i }));

  expect(
    await screen.findByRole("heading", { name: "Notebook" }),
  ).toBeInTheDocument();
  expect(screen.getByText("14 polegadas")).toBeInTheDocument();
  expect(screen.getByText("3 em estoque")).toBeInTheDocument();
  expect(
    screen.queryByText("Ainda não há produtos anunciados."),
  ).not.toBeInTheDocument();
});
