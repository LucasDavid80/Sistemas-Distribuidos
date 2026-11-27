def create_user(client, nome="Lucas", email="lucas@email.com"):
    response = client.post(
        "/users/",
        json={"nome": nome, "email": email, "idade": 23, "role": "client"},
    )
    assert response.status_code == 201
    return response.json()


def test_task_full_flow(client):
    user = create_user(client)

    # 1. Criar tarefa
    payload = {
        "titulo": "Implementar endpoints REST",
        "descricao": "Usar FastAPI",
        "prioridade": "ALTA",
        "status": "PENDENTE",
        "categoria": "Backend",
    }
    create_res = client.post(
        "/tasks/",
        json=payload,
        headers={"X-User-Id": str(user["id"])},
    )
    assert create_res.status_code == 201
    task = create_res.json()
    task_id = task["id"]
    assert task["titulo"] == "Implementar endpoints REST"
    assert task["prioridade"] == "ALTA"
    assert task["status"] == "PENDENTE"
    assert task["categoria"] == "Backend"

    # 2. Obter por ID
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == task_id

    # 3. Listar tarefas
    list_res = client.get("/tasks/")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # 4. Checar Métricas
    metrics_res = client.get("/tasks/metrics")
    assert metrics_res.status_code == 200
    metrics = metrics_res.json()
    assert metrics["total"] >= 1
    assert metrics["pendentes"] >= 1

    # 5. Atualizar Status (PATCH /tasks/{id}/status)
    status_res = client.patch(
        f"/tasks/{task_id}/status",
        json={"status": "EM_PROGRESSO"},
    )
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "EM_PROGRESSO"

    # 6. Atualizar Dados (PUT /tasks/{id})
    update_res = client.put(
        f"/tasks/{task_id}",
        json={
            "titulo": "Implementar endpoints REST e Testes",
            "prioridade": "MEDIA",
            "status": "CONCLUIDA",
        },
    )
    assert update_res.status_code == 200
    assert update_res.json()["titulo"] == "Implementar endpoints REST e Testes"
    assert update_res.json()["status"] == "CONCLUIDA"

    # 7. Excluir Tarefa (DELETE /tasks/{id})
    delete_res = client.delete(f"/tasks/{task_id}")
    assert delete_res.status_code == 204

    # 8. Confirmar remoção (404)
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_task_filters(client):
    user = create_user(client, nome="Filtro User", email="filter@email.com")

    client.post(
        "/tasks/",
        json={"titulo": "Tarefa Bug Fix", "status": "PENDENTE", "prioridade": "ALTA"},
        headers={"X-User-Id": str(user["id"])},
    )
    client.post(
        "/tasks/",
        json={
            "titulo": "Tarefa Documentacao",
            "status": "CONCLUIDA",
            "prioridade": "BAIXA",
        },
        headers={"X-User-Id": str(user["id"])},
    )

    res_concluida = client.get("/tasks/?status=CONCLUIDA")
    assert res_concluida.status_code == 200
    assert all(t["status"] == "CONCLUIDA" for t in res_concluida.json())

    res_search = client.get("/tasks/?search=Bug")
    assert res_search.status_code == 200
    assert any("Bug" in t["titulo"] for t in res_search.json())


def test_project_endpoints(client):
    user = create_user(client, nome="Project User", email="project@email.com")

    res = client.post(
        "/projects/",
        json={"nome": "Sistema Web", "descricao": "Full stack"},
        headers={"X-User-Id": str(user["id"])},
    )
    assert res.status_code == 201
    project = res.json()
    assert project["nome"] == "Sistema Web"

    list_res = client.get("/projects/")
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    del_res = client.delete(f"/projects/{project['id']}")
    assert del_res.status_code == 204
