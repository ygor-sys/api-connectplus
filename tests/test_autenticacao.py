"""Autenticação: quem é você? (falha -> 401)"""
from tests.conftest import ADMIN


def test_login_admin_retorna_token(client):
    r = client.post("/auth/login", data={"username": ADMIN[0], "password": ADMIN[1]})
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer" and r.json()["access_token"]


def test_login_senha_errada_retorna_401(client):
    r = client.post("/auth/login", data={"username": ADMIN[0], "password": "errada"})
    assert r.status_code == 401


def test_login_email_inexistente_retorna_401(client):
    r = client.post("/auth/login", data={"username": "ninguem@x.com", "password": "123"})
    assert r.status_code == 401


def test_me_sem_token_retorna_401(client):
    assert client.get("/auth/me").status_code == 401


def test_me_com_token_invalido_retorna_401(client):
    r = client.get("/auth/me", headers={"Authorization": "Bearer token.falso.qualquer"})
    assert r.status_code == 401


def test_me_retorna_perfil_e_nao_expoe_senha(client, h_colab):
    r = client.get("/auth/me", headers=h_colab)
    assert r.status_code == 200
    assert r.json()["perfil"] == "colaborador"
    assert "senha" not in str(r.json()).lower() and "hash" not in str(r.json()).lower()
