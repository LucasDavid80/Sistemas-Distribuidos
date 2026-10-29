import { useState } from "react";
import { ProductForm } from "./components/ProductForm";
import { ProductList } from "./components/ProductList";

export default function App() {
  const [products, setProducts] = useState([]);
  const [screen, setScreen] = useState("home");

  function addProduct(product) {
    setProducts((current) => [
      ...current,
      { ...product, id: crypto.randomUUID() },
    ]);
  }

  if (screen === "buyer") {
    return (
      <MarketplacePage
        description="Explore as ofertas publicadas por vendedores da comunidade."
        onBack={() => setScreen("home")}
        title="Encontre o que você precisa"
      >
        <section aria-labelledby="products-heading">
          <p className="text-sm font-semibold text-brand-700">
            Área do comprador
          </p>
          <h2 className="mb-4 text-2xl font-bold" id="products-heading">
            Produtos disponíveis
          </h2>
          <ProductList products={products} />
        </section>
      </MarketplacePage>
    );
  }

  if (screen === "seller") {
    return (
      <MarketplacePage
        description="Cadastre seus produtos. Nesta prática, os anúncios ficam apenas neste navegador."
        onBack={() => setScreen("home")}
        title="Publique suas ofertas"
      >
        <ProductForm onAdd={addProduct} />
      </MarketplacePage>
    );
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-5xl items-center p-4 sm:p-8">
      <section className="w-full rounded-3xl bg-slate-900 p-6 text-white shadow-xl sm:p-12">
        <p className="text-sm font-semibold tracking-wide text-emerald-300 uppercase">
          Marketplace local
        </p>
        <h1 className="mt-3 max-w-2xl text-4xl font-bold sm:text-5xl">
          O que você deseja fazer hoje?
        </h1>
        <p className="mt-4 max-w-2xl text-lg text-slate-300">
          Escolha seu perfil para publicar produtos ou explorar as ofertas da
          comunidade.
        </p>
        <div className="mt-8 grid gap-4 sm:grid-cols-2">
          <button
            className="rounded-2xl bg-brand-600 p-6 text-left transition hover:bg-brand-700 focus:outline-none focus:ring-4 focus:ring-emerald-300"
            onClick={() => setScreen("buyer")}
            type="button"
          >
            <span className="block text-xl font-bold">Sou comprador</span>
            <span className="mt-2 block text-emerald-50">
              Ver produtos disponíveis e encontrar ofertas.
            </span>
          </button>
          <button
            className="rounded-2xl border border-slate-600 p-6 text-left transition hover:border-slate-400 hover:bg-slate-800 focus:outline-none focus:ring-4 focus:ring-slate-400"
            onClick={() => setScreen("seller")}
            type="button"
          >
            <span className="block text-xl font-bold">Sou vendedor</span>
            <span className="mt-2 block text-slate-300">
              Cadastrar um produto para a comunidade encontrar.
            </span>
          </button>
        </div>
      </section>
    </main>
  );
}

function MarketplacePage({ children, description, onBack, title }) {
  return (
    <main className="mx-auto min-h-screen max-w-5xl p-4 sm:p-8">
      <header className="mb-8 rounded-2xl bg-slate-900 p-6 text-white sm:p-10">
        <button
          className="text-sm font-semibold text-emerald-300 underline underline-offset-4"
          onClick={onBack}
          type="button"
        >
          ← Voltar ao início
        </button>
        <h1 className="mt-5 text-3xl font-bold sm:text-4xl">{title}</h1>
        <p className="mt-3 max-w-2xl text-slate-300">{description}</p>
      </header>
      {children}
    </main>
  );
}
