"""Autorização: você pode fazer isso? (falha -> 403). Matriz em docs/MATRIZ_PERMISSOES.md"""


def test_admin_publica_comunicado_e_vira_autor(client, h_admin):
    r = client.post("/comunicados", json={"titulo": "Aviso", "conteudo": "Texto"}, headers=h_admin)
    assert r.status_code == 201
    assert r.json()["autor"]["email"] == "admin@connectplus.com"
    client.delete(f"/comunicados/{r.json()['id']}", headers=h_admin)


def test_colaborador_nao_publica_403(client, h_colab):
    r = client.post("/comunicados", json={"titulo": "a", "conteudo": "b"}, headers=h_colab)
    assert r.status_code == 403


def test_colaborador_nao_edita_403(client, h_colab, comunicado):
    assert client.put(f"/comunicados/{comunicado}", json={"titulo": "z"}, headers=h_colab).status_code == 403


def test_colaborador_nao_exclui_403(client, h_colab, comunicado):
    assert client.delete(f"/comunicados/{comunicado}", headers=h_colab).status_code == 403
    # e o comunicado continua existindo
    assert client.get(f"/comunicados/{comunicado}", headers=h_colab).status_code == 200


def test_sem_token_e_401_e_nao_403(client, comunicado):
    """Sem identificação = 401; identificado sem permissão = 403 (são erros diferentes)."""
    assert client.post("/comunicados", json={"titulo": "a", "conteudo": "b"}).status_code == 401
    assert client.put(f"/comunicados/{comunicado}", json={"titulo": "z"}).status_code == 401
    assert client.delete(f"/comunicados/{comunicado}").status_code == 401


def test_nao_e_possivel_escolher_autor_nem_perfil(client, h_admin):
    r = client.post("/comunicados", json={"titulo": "x", "conteudo": "y", "autor_id": 2}, headers=h_admin)
    assert r.status_code == 422
    r = client.post("/comunicados", json={"titulo": "x", "conteudo": "y", "perfil": "administrador"}, headers=h_admin)
    assert r.status_code == 422


def test_admin_nao_edita_comunicado_de_outro_admin_403(client, h_admin2, comunicado):
    r = client.put(f"/comunicados/{comunicado}", json={"titulo": "invadido"}, headers=h_admin2)
    assert r.status_code == 403


def test_admin_nao_exclui_comunicado_de_outro_admin_403(client, h_admin, h_admin2, comunicado):
    assert client.delete(f"/comunicados/{comunicado}", headers=h_admin2).status_code == 403
    assert client.get(f"/comunicados/{comunicado}", headers=h_admin).status_code == 200


def test_admin_le_comunicado_de_outro_admin_200(client, h_admin2, comunicado):
    assert client.get(f"/comunicados/{comunicado}", headers=h_admin2).status_code == 200
