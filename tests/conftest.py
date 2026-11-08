"""Configuração do Pytest: banco temporário isolado + fixtures de login."""
import os
import tempfile

# Precisa vir ANTES de importar app: o banco de testes é um arquivo temporário,
# então os testes nunca mexem no connectplus.db real.
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp.name}"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app import models  # noqa: E402
from app.database import SessionLocal  # noqa: E402
from app.main import app  # noqa: E402
from app.security import gerar_hash  # noqa: E402

ADMIN = ("admin@connectplus.com", "admin123")
COLAB = ("colaborador@connectplus.com", "colab123")
ADMIN2 = ("admin2@connectplus.com", "admin2123")


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as c:  # dispara o lifespan (cria tabelas e usuários)
        yield c


def _headers(client, email, senha):
    r = client.post("/auth/login", data={"username": email, "password": senha})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture(scope="session")
def h_admin(client):
    return _headers(client, *ADMIN)


@pytest.fixture(scope="session")
def h_admin2(client):
    """Segundo administrador (criado só nos testes) para validar a regra do autor."""
    with SessionLocal() as db:
        db.add(models.Usuario(nome="Admin 2", email=ADMIN2[0], senha_hash=gerar_hash(ADMIN2[1]),
                              perfil=models.ADMINISTRADOR))
        db.commit()
    return _headers(client, *ADMIN2)


@pytest.fixture(scope="session")
def h_colab(client):
    return _headers(client, *COLAB)


@pytest.fixture
def comunicado(client, h_admin):
    """Cria um comunicado como admin e o remove ao final do teste."""
    r = client.post("/comunicados", json={"titulo": "Manutenção", "conteudo": "Sábado 22h"}, headers=h_admin)
    assert r.status_code == 201
    cid = r.json()["id"]
    yield cid
    client.delete(f"/comunicados/{cid}", headers=h_admin)
