import { useState } from "react";
import { validateProduct } from "../validation";

export function ProductForm({ onAdd }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [stock, setStock] = useState("");
  const [errors, setErrors] = useState({});

  function handleSubmit(event) {
    event.preventDefault();
    const result = validateProduct({ name, description, price, stock });
    setErrors(result.errors);

    if (Object.keys(result.errors).length > 0) return;

    onAdd(result.values);
    setName("");
    setDescription("");
    setPrice("");
    setStock("");
  }

  return (
    <form
      aria-label="Cadastrar produto"
      className="space-y-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
      noValidate
      onSubmit={handleSubmit}
    >
      <div>
        <p className="text-sm font-semibold text-brand-700">Área do vendedor</p>
        <h2 className="text-xl font-bold">Publique um produto</h2>
      </div>
      <FieldError error={errors.name} id="product-name-error">
        <label className="block text-sm font-medium" htmlFor="product-name">
          Nome do produto
        </label>
        <input
          aria-describedby={errors.name ? "product-name-error" : undefined}
          aria-invalid={Boolean(errors.name)}
          className="mt-1 w-full rounded-lg border border-slate-300 p-2.5 outline-none focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
          id="product-name"
          onChange={(event) => setName(event.target.value)}
          value={name}
        />
      </FieldError>
      <div>
        <label
          className="block text-sm font-medium"
          htmlFor="product-description"
        >
          Descrição
        </label>
        <textarea
          className="mt-1 w-full rounded-lg border border-slate-300 p-2.5 outline-none focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
          id="product-description"
          onChange={(event) => setDescription(event.target.value)}
          rows={3}
          value={description}
        />
      </div>
      <div className="grid gap-4 sm:grid-cols-2">
        <FieldError error={errors.price} id="product-price-error">
          <label className="block text-sm font-medium" htmlFor="product-price">
            Preço (R$)
          </label>
          <input
            aria-describedby={errors.price ? "product-price-error" : undefined}
            aria-invalid={Boolean(errors.price)}
            className="mt-1 w-full rounded-lg border border-slate-300 p-2.5 outline-none focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
            id="product-price"
            min="0.01"
            onChange={(event) => setPrice(event.target.value)}
            step="0.01"
            type="number"
            value={price}
          />
        </FieldError>
        <FieldError error={errors.stock} id="product-stock-error">
          <label className="block text-sm font-medium" htmlFor="product-stock">
            Estoque
          </label>
          <input
            aria-describedby={errors.stock ? "product-stock-error" : undefined}
            aria-invalid={Boolean(errors.stock)}
            className="mt-1 w-full rounded-lg border border-slate-300 p-2.5 outline-none focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
            id="product-stock"
            min="0"
            onChange={(event) => setStock(event.target.value)}
            step="1"
            type="number"
            value={stock}
          />
        </FieldError>
      </div>
      <button
        className="rounded-lg bg-brand-600 px-4 py-2.5 font-semibold text-white transition hover:bg-brand-700"
        type="submit"
      >
        Publicar produto
      </button>
    </form>
  );
}

function FieldError({ children, error, id }) {
  return (
    <div>
      {children}
      {error && (
        <p className="mt-1 text-sm text-red-700" id={id} role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
