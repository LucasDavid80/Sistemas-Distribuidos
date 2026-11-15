export const NAME_MAX_LENGTH = 120;

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
