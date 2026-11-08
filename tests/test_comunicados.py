"""Funcionalidades da API (1ª parcial continua funcionando)."""
from fastapi.testclient import TestClient

from app.main import app
from tests.conftest import ADMIN, COLAB


def test_colaborador_lista_comunicados_200(client, h_colab, comunicado):
    r = client.get("/comunicados", headers=h_colab)
    assert r.status_code == 200
    assert any(c["id"] == comunicado for c in r.json())


def test_listar_sem_token_retorna_401(client):
    assert client.get("/comunicados").status_code == 401


def test_consultar_inexistente_retorna_404(client, h_admin):
    assert client.get("/comunicados/999999", headers=h_admin).status_code == 404
    assert client.put("/comunicados/999999", json={"titulo": "z"}, headers=h_admin).status_code == 404
    assert client.delete("/comunicados/999999", headers=h_admin).status_code == 404


def test_titulo_ausente_ou_vazio_retorna_422(client, h_admin):
    assert client.post("/comunicados", json={"conteudo": "sem título"}, headers=h_admin).status_code == 422
    assert client.post("/comunicados", json={"titulo": "  ", "conteudo": "x"}, headers=h_admin).status_code == 422


def test_admin_atualiza_comunicado_200(client, h_admin, comunicado):
    r = client.put(f"/comunicados/{comunicado}", json={"titulo": "Corrigido"}, headers=h_admin)
    assert r.status_code == 200 and r.json()["titulo"] == "Corrigido"


def test_admin_exclui_e_depois_404(client, h_admin, comunicado):
    assert client.delete(f"/comunicados/{comunicado}", headers=h_admin).status_code == 204
    assert client.get(f"/comunicados/{comunicado}", headers=h_admin).status_code == 404


def test_dados_persistem_apos_reiniciar_aplicacao(client, h_admin, comunicado):
    # novo ciclo de vida da aplicação, mesmo banco
    with TestClient(app) as novo:
        r = novo.post("/auth/login", data={"username": COLAB[0], "password": COLAB[1]})
        h = {"Authorization": f"Bearer {r.json()['access_token']}"}
        assert novo.get(f"/comunicados/{comunicado}", headers=h).status_code == 200
