export const NAME_MAX_LENGTH = 120;
export const TASK_TITLE_MAX_LENGTH = 150;
export const TASK_DESC_MAX_LENGTH = 1000;
export const TASK_CATEGORY_MAX_LENGTH = 60;

export function validateTask({
  titulo = "",
  descricao = "",
  prioridade = "MEDIA",
  status = "PENDENTE",
  categoria = "Geral",
}) {
  const errors = {};
  const trimmedTitulo = titulo.trim();
  const trimmedDescricao = descricao.trim();
  const trimmedCategoria = categoria.trim() || "Geral";

  if (!trimmedTitulo) {
    errors.titulo = "O título da tarefa é obrigatório.";
  } else if (trimmedTitulo.length > TASK_TITLE_MAX_LENGTH) {
    errors.titulo = `O título deve ter no máximo ${TASK_TITLE_MAX_LENGTH} caracteres.`;
  }

  if (trimmedDescricao.length > TASK_DESC_MAX_LENGTH) {
    errors.descricao = `A descrição deve ter no máximo ${TASK_DESC_MAX_LENGTH} caracteres.`;
  }

  if (trimmedCategoria.length > TASK_CATEGORY_MAX_LENGTH) {
    errors.categoria = `A categoria deve ter no máximo ${TASK_CATEGORY_MAX_LENGTH} caracteres.`;
  }

  const validPriorities = ["BAIXA", "MEDIA", "ALTA"];
  if (!validPriorities.includes(prioridade)) {
    errors.prioridade = "Prioridade inválida.";
  }

  const validStatuses = ["PENDENTE", "EM_PROGRESSO", "CONCLUIDA"];
  if (!validStatuses.includes(status)) {
    errors.status = "Status inválido.";
  }

  return {
    errors,
    values: {
      titulo: trimmedTitulo,
      descricao: trimmedDescricao,
      prioridade,
      status,
      categoria: trimmedCategoria,
    },
  };
}

export function validateProduct({ name, description, price, stock }) {
  const errors = {};
  const trimmedName = name.trim();
  const trimmedDescription = description.trim();
  const numericPrice = Number(price);
  const numericStock = Number(stock);

  if (!trimmedName) {
    errors.name = "O nome do produto é obrigatório.";
  } else if (trimmedName.length > NAME_MAX_LENGTH) {
    errors.name = `O nome deve ter no máximo ${NAME_MAX_LENGTH} caracteres.`;
  }

  if (!price || Number.isNaN(numericPrice) || numericPrice <= 0) {
    errors.price = "Informe um preço maior que zero.";
  }

  if (stock === "" || !Number.isInteger(numericStock) || numericStock < 0) {
    errors.stock = "Informe um estoque inteiro igual ou maior que zero.";
  }

  return {
    errors,
    values: {
      name: trimmedName,
      description: trimmedDescription,
      price: numericPrice,
      stock: numericStock,
    },
  };
}
