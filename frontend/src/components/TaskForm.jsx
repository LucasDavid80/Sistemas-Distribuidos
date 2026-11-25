import { useEffect, useState } from "react";
import { validateTask } from "../validation";

function FieldError({ error, id, children }) {
  return (
    <div>
      {children}
      {error && (
        <p className="mt-1 text-xs text-rose-600" id={id} role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

export function TaskForm({ onSave, editingTask, onCancelEdit }) {
  const [titulo, setTitulo] = useState("");
  const [descricao, setDescricao] = useState("");
  const [prioridade, setPrioridade] = useState("MEDIA");
  const [status, setStatus] = useState("PENDENTE");
  const [categoria, setCategoria] = useState("Geral");
  const [errors, setErrors] = useState({});
  const [submitError, setSubmitError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (editingTask) {
      setTitulo(editingTask.titulo || "");
      setDescricao(editingTask.descricao || "");
      setPrioridade(editingTask.prioridade || "MEDIA");
      setStatus(editingTask.status || "PENDENTE");
      setCategoria(editingTask.categoria || "Geral");
      setErrors({});
      setSubmitError("");
    } else {
      setTitulo("");
      setDescricao("");
      setPrioridade("MEDIA");
      setStatus("PENDENTE");
      setCategoria("Geral");
      setErrors({});
      setSubmitError("");
    }
  }, [editingTask]);

  async function handleSubmit(event) {
    event.preventDefault();
    const result = validateTask({
      titulo,
      descricao,
      prioridade,
      status,
      categoria,
    });
    setErrors(result.errors);

    if (Object.keys(result.errors).length > 0) return;

    setSubmitError("");
    setSubmitting(true);
    try {
      await onSave(result.values, editingTask?.id);
      if (!editingTask) {
        setTitulo("");
        setDescricao("");
        setPrioridade("MEDIA");
        setStatus("PENDENTE");
        setCategoria("Geral");
      }
    } catch (error) {
      setSubmitError(error.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form
      aria-label={editingTask ? "Editar tarefa" : "Cadastrar tarefa"}
      className="space-y-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
      noValidate
      onSubmit={handleSubmit}
    >
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div>
          <h2 className="text-lg font-bold text-slate-800">
            {editingTask ? "Editar Tarefa" : "Nova Tarefa"}
          </h2>
          <p className="text-xs text-slate-500">
            {editingTask
              ? `Atualizando informações da tarefa #${editingTask.id}`
              : "Preencha as informações da atividade que deseja gerenciar"}
          </p>
        </div>
        {editingTask && (
          <button
            className="rounded-lg border border-slate-300 px-3 py-1 text-xs font-semibold text-slate-600 hover:bg-slate-100"
            onClick={onCancelEdit}
            type="button"
          >
            Cancelar Edição
          </button>
        )}
      </div>

      <FieldError error={errors.titulo} id="task-title-error">
        <label
          className="block text-sm font-medium text-slate-700"
          htmlFor="task-title"
        >
          Título da Tarefa *
        </label>
        <input
          aria-describedby={errors.titulo ? "task-title-error" : undefined}
          aria-invalid={Boolean(errors.titulo)}
          className="mt-1 w-full rounded-lg border border-slate-300 p-2.5 outline-none transition focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
          id="task-title"
          onChange={(event) => setTitulo(event.target.value)}
          placeholder="Ex: Implementar testes E2E do sistema"
          value={titulo}
        />
      </FieldError>

      <div>
        <label
          className="block text-sm font-medium text-slate-700"
          htmlFor="task-description"
        >
          Descrição detalhada
        </label>
        <textarea
          className="mt-1 w-full rounded-lg border border-slate-300 p-2.5 outline-none transition focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
          id="task-description"
          onChange={(event) => setDescricao(event.target.value)}
          placeholder="Ex: Detalhes, dependências ou notas sobre a tarefa..."
          rows={3}
          value={descricao}
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <FieldError error={errors.prioridade} id="task-priority-error">
          <label
            className="block text-sm font-medium text-slate-700"
            htmlFor="task-priority"
          >
            Prioridade
          </label>
          <select
            className="mt-1 w-full rounded-lg border border-slate-300 p-2.5 outline-none transition focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
            id="task-priority"
            onChange={(event) => setPrioridade(event.target.value)}
            value={prioridade}
          >
            <option value="BAIXA">Baixa</option>
            <option value="MEDIA">Média</option>
            <option value="ALTA">Alta</option>
          </select>
        </FieldError>

        <FieldError error={errors.status} id="task-status-error">
          <label
            className="block text-sm font-medium text-slate-700"
            htmlFor="task-status"
          >
            Status
          </label>
          <select
            className="mt-1 w-full rounded-lg border border-slate-300 p-2.5 outline-none transition focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
            id="task-status"
            onChange={(event) => setStatus(event.target.value)}
            value={status}
          >
            <option value="PENDENTE">Pendente</option>
            <option value="EM_PROGRESSO">Em Progresso</option>
            <option value="CONCLUIDA">Concluída</option>
          </select>
        </FieldError>

        <FieldError error={errors.categoria} id="task-category-error">
          <label
            className="block text-sm font-medium text-slate-700"
            htmlFor="task-category"
          >
            Categoria
          </label>
          <input
            className="mt-1 w-full rounded-lg border border-slate-300 p-2.5 outline-none transition focus:border-brand-600 focus:ring-2 focus:ring-brand-50"
            id="task-category"
            onChange={(event) => setCategoria(event.target.value)}
            placeholder="Ex: Backend, Frontend, DevOps"
            value={categoria}
          />
        </FieldError>
      </div>

      {submitError && (
        <p
          className="rounded-lg bg-rose-50 p-3 text-sm text-rose-700"
          role="alert"
        >
          {submitError}
        </p>
      )}

      <button
        className="w-full rounded-lg bg-brand-600 py-3 font-semibold text-white shadow-sm transition hover:bg-brand-700 focus:outline-none focus:ring-4 focus:ring-brand-100 disabled:opacity-60"
        disabled={submitting}
        type="submit"
      >
        {submitting
          ? "Salvando..."
          : editingTask
            ? "Atualizar Tarefa"
            : "Cadastrar Tarefa"}
      </button>
    </form>
  );
}
