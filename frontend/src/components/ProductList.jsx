const currency = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

export function ProductList({ products }) {
  if (products.length === 0) {
    return (
      <p className="rounded-xl border border-dashed border-slate-300 bg-white p-6 text-slate-600">
        Ainda não há produtos anunciados.
      </p>
    );
  }

  return (
    <ul className="grid gap-4 sm:grid-cols-2" aria-label="Produtos anunciados">
      {products.map((product) => (
        <li
          className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
          key={product.id}
        >
          <div className="flex items-start justify-between gap-3">
            <h3 className="text-lg font-bold">{product.name}</h3>
            <span className="rounded-full bg-brand-50 px-2.5 py-1 text-xs font-semibold text-brand-700">
              {product.stock} em estoque
            </span>
          </div>
          {product.description && (
            <p className="mt-2 text-sm text-slate-600">{product.description}</p>
          )}
          <p className="mt-5 text-xl font-bold text-brand-700">
            {currency.format(product.price)}
          </p>
          <button
            className="mt-4 w-full rounded-lg border border-brand-600 px-4 py-2 font-semibold text-brand-700"
            type="button"
          >
            Tenho interesse
          </button>
        </li>
      ))}
    </ul>
  );
}
