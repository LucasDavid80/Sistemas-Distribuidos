export const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8001";
const TASKS_URL = `${API_URL}/tasks/`;
const PROJECTS_URL = `${API_URL}/projects/`;

const userId = import.meta.env.VITE_USER_ID ?? "1";

async function request(url, options = {}, fallbackMessage) {
  try {
    const response = await fetch(url, options);
    if (response.status === 204) {
      return null;
    }
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

export function listTasks(filters = {}) {
  const params = new URLSearchParams();
  if (filters.status) params.append("status", filters.status);
  if (filters.prioridade) params.append("prioridade", filters.prioridade);
  if (filters.search) params.append("search", filters.search);

  const queryString = params.toString();
  const url = queryString ? `${TASKS_URL}?${queryString}` : TASKS_URL;

  return request(url, {}, "Erro ao carregar as tarefas.").then((tasks) =>
    tasks.map(mapTask),
  );
}

export function getTaskMetrics() {
  return request(
    `${API_URL}/tasks/metrics`,
    {},
    "Erro ao carregar métricas das tarefas.",
  );
}

export function createTask({
  titulo,
  descricao,
  prioridade,
  status,
  categoria,
  projectId,
}) {
  return request(
    TASKS_URL,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": userId,
      },
      body: JSON.stringify({
        titulo,
        descricao: descricao || "",
        prioridade: prioridade || "MEDIA",
        status: status || "PENDENTE",
        categoria: categoria || "Geral",
        project_id: projectId || null,
      }),
    },
    "Erro ao cadastrar a tarefa.",
  ).then(mapTask);
}

export function updateTask(id, data) {
  return request(
    `${TASKS_URL}${id}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": userId,
      },
      body: JSON.stringify({
        titulo: data.titulo,
        descricao: data.descricao,
        prioridade: data.prioridade,
        status: data.status,
        categoria: data.categoria,
        project_id: data.projectId ?? null,
      }),
    },
    "Erro ao atualizar a tarefa.",
  ).then(mapTask);
}

export function updateTaskStatus(id, newStatus) {
  return request(
    `${TASKS_URL}${id}/status`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": userId,
      },
      body: JSON.stringify({ status: newStatus }),
    },
    "Erro ao atualizar o status da tarefa.",
  ).then(mapTask);
}

export function deleteTask(id) {
  return request(
    `${TASKS_URL}${id}`,
    {
      method: "DELETE",
      headers: {
        "X-User-Id": userId,
      },
    },
    "Erro ao excluir a tarefa.",
  );
}

export function listProjects() {
  return request(PROJECTS_URL, {}, "Erro ao carregar os projetos.");
}

export function createProject({ nome, descricao }) {
  return request(
    PROJECTS_URL,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-User-Id": userId,
      },
      body: JSON.stringify({ nome, descricao: descricao || "" }),
    },
    "Erro ao cadastrar projeto.",
  );
}

function mapTask(task) {
  return {
    id: task.id,
    titulo: task.titulo,
    descricao: task.descricao,
    prioridade: task.prioridade,
    status: task.status,
    categoria: task.categoria,
    prazo: task.prazo,
    projectId: task.project_id,
    userId: task.user_id,
    createdAt: task.created_at,
    updatedAt: task.updated_at,
  };
}
