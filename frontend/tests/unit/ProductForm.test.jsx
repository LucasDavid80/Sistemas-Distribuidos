import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it, vi } from "vitest";
import { ProductForm } from "../../src/components/ProductForm";

it("mostra erro e não publica produto inválido", async () => {
  const user = userEvent.setup();
  const onAdd = vi.fn();
  render(<ProductForm onAdd={onAdd} />);

  await user.click(screen.getByRole("button", { name: "Publicar produto" }));

  expect(screen.getAllByRole("alert")).toHaveLength(3);
  expect(onAdd).not.toHaveBeenCalled();
});
