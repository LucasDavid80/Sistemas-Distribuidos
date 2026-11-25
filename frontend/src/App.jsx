import { useCallback, useEffect, useState } from "react";
import { TaskForm } from "./components/TaskForm";
import { TaskList } from "./components/TaskList";
import { TaskMetrics } from "./components/TaskMetrics";
import {
  createTask,
  deleteTask,
  getTaskMetrics,
  listTasks,
  updateTask,
  updateTaskStatus,
} from "./services/tasks";

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [metrics, setMetrics] = useState({
    total: 0,
    pendentes: 0,
    em_progresso: 0,
    concluidas: 0,
    taxa_conclusao: 0,
  });
  const [filters, setFilters] = useState({
    status: "",
    prioridade: "",
    search: "",
  });
  const [editingTask, setEditingTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [feedback, setFeedback] = useState("");

  const loadData = useCallback(
    async (currentFilters = filters) => {
      setLoading(true);
      setError("");
      try {
        const [tasksData, metricsData] = await Promise.all([
          listTasks(currentFilters),
          getTaskMetrics(),
        ]);
        setTasks(tasksData);
        setMetrics(metricsData);
      } catch (err) {
        setError(err.message || "Erro ao carregar os dados.");
      } finally {
        setLoading(false);
      }
    },
    [filters],
  );

  useEffect(() => {
    loadData(filters);
  }, [filters, loadData]);

  function notify(msg) {
    setFeedback(msg);
    setTimeout(() => setFeedback(""), 4000);
  }

  async function handleSaveTask(values, id) {
    if (id) {
      await updateTask(id, values);
      notify("Tarefa atualizada com sucesso!");
      setEditingTask(null);
    } else {
      await createTask(values);
      notify("Tarefa criada com sucesso!");
    }
    await loadData(filters);
  }

  async function handleStatusChange(id, newStatus) {
    try {
      await updateTaskStatus(id, newStatus);
      notify("Status da tarefa atualizado!");
      await loadData(filters);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDeleteTask(id) {
    try {
      await deleteTask(id);
      notify("Tarefa removida com sucesso!");
      if (editingTask?.id === id) {
        setEditingTask(null);
      }
      await loadData(filters);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      {/* Top Header */}
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6">
          <div className="flex items-center gap-3">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 font-black text-lg text-white shadow-sm">
              TF
            </span>
            <div>
              <h1 className="text-xl font-bold tracking-tight text-slate-900">
                TaskFlow
              </h1>
              <p className="text-xs text-slate-500">
                Gestão Distribuída de Tarefas & Projetos — C216
              </p>
            </div>
          </div>
          <span className="rounded-full bg-emerald-50 px-3 py-1 font-semibold text-emerald-700 text-xs">
            ● Backend Online
          </span>
        </div>
      </header>

      {/* Main Container */}
      <main className="mx-auto max-w-6xl space-y-6 px-4 py-8 sm:px-6">
        {/* Notificações / Feedbacks */}
        {feedback && (
          <div
            className="flex items-center justify-between rounded-xl bg-emerald-50 p-4 text-emerald-800 text-sm shadow-sm"
            role="status"
          >
            <span>{feedback}</span>
            <button
              className="font-bold text-emerald-900 hover:underline"
              onClick={() => setFeedback("")}
              type="button"
            >
              Fechar
            </button>
          </div>
        )}

        {error && (
          <div
            className="flex items-center justify-between rounded-xl bg-rose-50 p-4 text-rose-800 text-sm shadow-sm"
            role="alert"
          >
            <span>{error}</span>
            <button
              className="font-bold text-rose-900 hover:underline"
              onClick={() => setError("")}
              type="button"
            >
              Fechar
            </button>
          </div>
        )}

        {/* Dashboard de Métricas */}
        <TaskMetrics metrics={metrics} />

        {/* Layout de Duas Colunas: Formulário à esquerda, Listagem à direita */}
        <div className="grid items-start gap-6 lg:grid-cols-3">
          <div className="lg:col-span-1">
            <TaskForm
              editingTask={editingTask}
              onCancelEdit={() => setEditingTask(null)}
              onSave={handleSaveTask}
            />
          </div>

          <div className="lg:col-span-2">
            {loading ? (
              <div
                className="rounded-2xl border border-slate-200 bg-white p-12 text-center text-slate-500 shadow-sm"
                role="status"
              >
                <p className="animate-pulse font-medium">
                  Carregando tarefas do sistema...
                </p>
              </div>
            ) : (
              <TaskList
                filters={filters}
                onDelete={handleDeleteTask}
                onEdit={setEditingTask}
                onFilterChange={setFilters}
                onStatusChange={handleStatusChange}
                tasks={tasks}
              />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
