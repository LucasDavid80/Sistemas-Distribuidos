export function TaskMetrics({ metrics }) {
  const {
    total = 0,
    pendentes = 0,
    em_progresso = 0,
    concluidas = 0,
    taxa_conclusao = 0,
  } = metrics || {};

  return (
    <section
      aria-label="Métricas de produtividade"
      className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
    >
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4">
        <div>
          <h2 className="text-lg font-bold text-slate-800">
            Painel de Produtividade
          </h2>
          <p className="text-xs text-slate-500">
            Acompanhe o andamento das suas atividades em tempo real
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm font-semibold text-slate-600">
            Progresso Geral:
          </span>
          <span className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-bold text-emerald-800">
            {taxa_conclusao}%
          </span>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div className="rounded-xl border border-slate-100 bg-slate-50 p-3 text-center">
          <p className="text-xs font-medium text-slate-500 uppercase">
            Total de Tarefas
          </p>
          <p
            className="mt-1 text-2xl font-black text-slate-800"
            data-testid="metric-total"
          >
            {total}
          </p>
        </div>
        <div className="rounded-xl border border-amber-100 bg-amber-50 p-3 text-center">
          <p className="text-xs font-medium text-amber-700 uppercase">
            Pendentes
          </p>
          <p
            className="mt-1 text-2xl font-black text-amber-800"
            data-testid="metric-pendentes"
          >
            {pendentes}
          </p>
        </div>
        <div className="rounded-xl border border-blue-100 bg-blue-50 p-3 text-center">
          <p className="text-xs font-medium text-blue-700 uppercase">
            Em Progresso
          </p>
          <p
            className="mt-1 text-2xl font-black text-blue-800"
            data-testid="metric-em-progresso"
          >
            {em_progresso}
          </p>
        </div>
        <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-3 text-center">
          <p className="text-xs font-medium text-emerald-700 uppercase">
            Concluídas
          </p>
          <p
            className="mt-1 text-2xl font-black text-emerald-800"
            data-testid="metric-concluidas"
          >
            {concluidas}
          </p>
        </div>
      </div>

      <div className="mt-4">
        <div className="h-2 w-full overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full bg-emerald-500 transition-all duration-500 ease-out"
            style={{ width: `${Math.min(100, Math.max(0, taxa_conclusao))}%` }}
          />
        </div>
      </div>
    </section>
  );
}
