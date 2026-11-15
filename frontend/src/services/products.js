export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8001";
const PRODUCTS_URL = `${API_URL}/products/`;

const userId = import.meta.env.VITE_USER_ID ?? "1";

async function request(url, options = {}, fallbackMessage) {
  try {
    const response = await fetch(url, options);
    const body = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(body.detail || fallbackMessage);
    }
    return body;
  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error("Não foi possível conectar à API.");
    }
    throw error;
  }
}

export function listProducts() {
  return request(PRODUCTS_URL, {}, "Erro ao carregar os produtos.").then(
    (products) => products.map(mapProduct),
  );
}

export function createProduct({ name, description, price, stock }) {
  return request(
    PRODUCTS_URL,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": userId,
      },
      body: JSON.stringify({
        nome: name,
        descricao: description || "",
        preco: price,
        estoque: stock,
      }),
    },
    "Erro ao cadastrar o produto.",
  ).then(mapProduct);
}

function mapProduct(product) {
  return {
    id: product.id,
    name: product.nome,
    description: product.descricao,
    price: product.preco,
    stock: product.estoque,
    sellerId: product.seller_id,
  };
}
