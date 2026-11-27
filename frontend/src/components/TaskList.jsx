import { useState } from "react";

const PRIORITY_BADGES = {
  BAIXA: "bg-slate-100 text-slate-700 border-slate-200",
  MEDIA: "bg-amber-100 text-amber-800 border-amber-200",
  ALTA: "bg-rose-100 text-rose-800 border-rose-200",
};

const STATUS_BADGES = {
  PENDENTE: "bg-amber-50 text-amber-700 border-amber-200",
  EM_PROGRESSO: "bg-blue-50 text-blue-700 border-blue-200",
  CONCLUIDA: "bg-emerald-50 text-emerald-700 border-emerald-200",
};

const STATUS_LABELS = {
  PENDENTE: "Pendente",
  EM_PROGRESSO: "Em Progresso",
  CONCLUIDA: "Concluída",
};

export function TaskList({
  tasks,
  onStatusChange,
  onEdit,
  onDelete,
  filters,
  onFilterChange,
}) {
  const [deletingId, setDeletingId] = useState(null);

  async function handleDelete(id) {
    if (window.confirm("Deseja realmente excluir esta tarefa?")) {
      setDeletingId(id);
      try {
        await onDelete(id);
      } finally {
        setDeletingId(null);
      }
    }
  }

  return (
    <div className="space-y-4">
      {/* Barra de Filtros e Busca */}
      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <div className="grid gap-3 sm:grid-cols-3">
          <div>
            <label
              className="block text-xs font-semibold text-slate-500 uppercase"
              htmlFor="search-task"
            >
              Buscar tarefas
            </label>
            <input
              className="mt-1 w-full rounded-lg border border-slate-300 p-2 text-sm outline-none transition focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
              id="search-task"
              onChange={(e) =>
                onFilterChange({ ...filters, search: e.target.value })
              }
              placeholder="Digite para buscar..."
              value={filters.search || ""}
            />
          </div>
          <div>
            <label
              className="block text-xs font-semibold text-slate-500 uppercase"
              htmlFor="filter-status"
            >
              Status
            </label>
            <select
              className="mt-1 w-full rounded-lg border border-slate-300 p-2 text-sm outline-none transition focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
              id="filter-status"
              onChange={(e) =>
                onFilterChange({ ...filters, status: e.target.value })
              }
              value={filters.status || ""}
            >
              <option value="">Todos os status</option>
              <option value="PENDENTE">Pendente</option>
              <option value="EM_PROGRESSO">Em Progresso</option>
              <option value="CONCLUIDA">Concluída</option>
            </select>
          </div>
          <div>
            <label
              className="block text-xs font-semibold text-slate-500 uppercase"
              htmlFor="filter-priority"
            >
              Prioridade
            </label>
            <select
              className="mt-1 w-full rounded-lg border border-slate-300 p-2 text-sm outline-none transition focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
              id="filter-priority"
              onChange={(e) =>
                onFilterChange({ ...filters, prioridade: e.target.value })
              }
              value={filters.prioridade || ""}
            >
              <option value="">Todas as prioridades</option>
              <option value="ALTA">Alta</option>
              <option value="MEDIA">Média</option>
              <option value="BAIXA">Baixa</option>
            </select>
          </div>
        </div>
      </div>

      {/* Lista de Cards */}
      {tasks.length === 0 ? (
        <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-8 text-center text-slate-500">
          <p className="text-base font-semibold">Nenhuma tarefa encontrada.</p>
          <p className="mt-1 text-sm text-slate-400">
            Cadastre uma nova atividade acima ou ajuste os filtros.
          </p>
        </div>
      ) : (
        <ul aria-label="Lista de tarefas" className="grid gap-4 sm:grid-cols-2">
          {tasks.map((task) => (
            <li
              className="flex flex-col justify-between rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:shadow-md"
              key={task.id}
            >
              <div>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="rounded-md bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">
                    {task.categoria}
                  </span>
                  <div className="flex items-center gap-1.5">
                    <span
                      className={`rounded-full border px-2.5 py-0.5 text-xs font-bold ${
                        PRIORITY_BADGES[task.prioridade] || "bg-slate-100"
                      }`}
                    >
                      {task.prioridade}
                    </span>
                    <span
                      className={`rounded-full border px-2.5 py-0.5 text-xs font-bold ${
                        STATUS_BADGES[task.status] || "bg-slate-100"
                      }`}
                    >
                      {STATUS_LABELS[task.status] || task.status}
                    </span>
                  </div>
                </div>

                <h3 className="mt-3 text-lg font-bold text-slate-900">
                  {task.titulo}
                </h3>

                {task.descricao && (
                  <p className="mt-2 text-sm text-slate-600 whitespace-pre-line">
                    {task.descricao}
                  </p>
                )}
              </div>

              <div className="mt-5 border-t border-slate-100 pt-3">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <div className="flex items-center gap-1">
                    {task.status === "PENDENTE" && (
                      <button
                        className="rounded-lg bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700 hover:bg-blue-100"
                        onClick={() => onStatusChange(task.id, "EM_PROGRESSO")}
                        type="button"
                      >
                        Iniciar
                      </button>
                    )}
                    {task.status !== "CONCLUIDA" && (
                      <button
                        className="rounded-lg bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700 hover:bg-emerald-100"
                        onClick={() => onStatusChange(task.id, "CONCLUIDA")}
                        type="button"
                      >
                        Concluir
                      </button>
                    )}
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      className="rounded-lg border border-slate-200 px-2.5 py-1 text-xs font-semibold text-slate-700 hover:bg-slate-50"
                      onClick={() => onEdit(task)}
                      type="button"
                    >
                      Editar
                    </button>
                    <button
                      className="rounded-lg border border-rose-200 px-2.5 py-1 text-xs font-semibold text-rose-700 hover:bg-rose-50 disabled:opacity-50"
                      disabled={deletingId === task.id}
                      onClick={() => handleDelete(task.id)}
                      type="button"
                    >
                      {deletingId === task.id ? "Excluindo..." : "Excluir"}
                    </button>
                  </div>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
