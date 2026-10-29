import { describe, expect, it } from "vitest";
import { validateProduct } from "../../src/validation";

describe("validateProduct", () => {
  it("rejeita nome vazio, preço inválido e estoque negativo", () => {
    const { errors } = validateProduct({
      name: "  ",
      description: "",
      price: "0",
      stock: "-1",
    });

    expect(errors.name).toBeDefined();
    expect(errors.price).toBeDefined();
    expect(errors.stock).toBeDefined();
  });

  it("remove espaços e converte preço e estoque", () => {
    const { errors, values } = validateProduct({
      name: "  Livro  ",
      description: "  Novo  ",
      price: "49.9",
      stock: "2",
    });

    expect(errors).toEqual({});
    expect(values).toEqual({
      name: "Livro",
      description: "Novo",
      price: 49.9,
      stock: 2,
    });
  });
});
