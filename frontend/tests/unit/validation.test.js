import { describe, expect, it } from "vitest";
import { validateProduct, validateTask } from "../../src/validation";

describe("validateTask", () => {
  it("rejeita título vazio e prioridade ou status inválidos", () => {
    const { errors } = validateTask({
      titulo: "   ",
      prioridade: "INEXISTENTE",
      status: "INVALIDO",
    });

    expect(errors.titulo).toBeDefined();
    expect(errors.prioridade).toBeDefined();
    expect(errors.status).toBeDefined();
  });

  it("remove espaços em branco e aplica valores padrão válidos", () => {
    const { errors, values } = validateTask({
      titulo: "  Desenvolver API  ",
      descricao: "  Endpoints REST com FastAPI  ",
      prioridade: "ALTA",
      status: "EM_PROGRESSO",
      categoria: "  Backend  ",
    });

    expect(errors).toEqual({});
    expect(values).toEqual({
      titulo: "Desenvolver API",
      descricao: "Endpoints REST com FastAPI",
      prioridade: "ALTA",
      status: "EM_PROGRESSO",
      categoria: "Backend",
    });
  });
});

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
