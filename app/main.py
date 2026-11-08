from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import select

from . import models
from .database import Base, SessionLocal, engine
from .routers import auth, comunicados
from .security import gerar_hash

USUARIOS_INICIAIS = [
    ("Administrador ConnectPlus", "admin@connectplus.com", "admin123", models.ADMINISTRADOR),
    ("Administrador 2 ConnectPlus", "admin2@connectplus.com", "admin2123", models.ADMINISTRADOR),
    ("Colaborador ConnectPlus", "colaborador@connectplus.com", "colab123", models.COLABORADOR),
]


def criar_usuarios_iniciais():
    """Contas pré-cadastradas para a demonstração (sem cadastro público)."""
    with SessionLocal() as db:
        for nome, email, senha, perfil in USUARIOS_INICIAIS:
            if db.scalar(select(models.Usuario).where(models.Usuario.email == email)) is None:
                db.add(models.Usuario(nome=nome, email=email, senha_hash=gerar_hash(senha), perfil=perfil))
        db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    criar_usuarios_iniciais()
    yield


app = FastAPI(
    title="Central de Comunicados Corporativos - ConnectPlus",
    description="API para publicação e consulta de comunicados internos.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(auth.router)
app.include_router(comunicados.router)
