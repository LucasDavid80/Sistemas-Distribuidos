import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it } from "vitest";
import App from "../../src/App";

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

  expect(screen.getByRole("heading", { name: "Notebook" })).toBeInTheDocument();
  expect(screen.getByText("14 polegadas")).toBeInTheDocument();
  expect(screen.getByText("3 em estoque")).toBeInTheDocument();
  expect(
    screen.queryByText("Ainda não há produtos anunciados."),
  ).not.toBeInTheDocument();
});
