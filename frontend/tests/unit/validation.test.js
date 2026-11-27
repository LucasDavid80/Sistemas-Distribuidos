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

  it("rejeita título que ultrapassa o limite de caracteres", () => {
    const { errors } = validateTask({ titulo: "A".repeat(151) });
    expect(errors.titulo).toMatch(/máximo/i);
  });

  it("rejeita descrição que ultrapassa o limite de caracteres", () => {
    const { errors } = validateTask({
      titulo: "Título válido",
      descricao: "X".repeat(1001),
    });
    expect(errors.descricao).toMatch(/máximo/i);
  });

  it("rejeita categoria que ultrapassa o limite de caracteres", () => {
    const { errors } = validateTask({
      titulo: "Título válido",
      categoria: "C".repeat(61),
    });
    expect(errors.categoria).toMatch(/máximo/i);
  });

  it("usa 'Geral' como categoria padrão quando categoria está vazia", () => {
    const { values } = validateTask({
      titulo: "Título válido",
      categoria: "   ",
    });
    expect(values.categoria).toBe("Geral");
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

  it("rejeita nome que ultrapassa o limite de caracteres", () => {
    const { errors } = validateProduct({
      name: "N".repeat(121),
      description: "",
      price: "10",
      stock: "1",
    });
    expect(errors.name).toMatch(/máximo/i);
  });

  it("rejeita preço não numérico", () => {
    const { errors } = validateProduct({
      name: "Produto",
      description: "",
      price: "abc",
      stock: "5",
    });
    expect(errors.price).toBeDefined();
  });

  it("rejeita estoque decimal", () => {
    const { errors } = validateProduct({
      name: "Produto",
      description: "",
      price: "10",
      stock: "1.5",
    });
    expect(errors.stock).toBeDefined();
  });

  it("rejeita estoque vazio", () => {
    const { errors } = validateProduct({
      name: "Produto",
      description: "",
      price: "10",
      stock: "",
    });
    expect(errors.stock).toBeDefined();
  });
});
