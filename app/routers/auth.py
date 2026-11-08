from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas, security
from ..database import get_db
from ..deps import usuario_atual

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=schemas.Token, summary="RF01 - Acesso ao sistema")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Use o e-mail no campo `username`."""
    usuario = db.scalar(select(models.Usuario).where(models.Usuario.email == form.username))
    if usuario is None or not security.verificar_senha(form.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return schemas.Token(access_token=security.criar_token(usuario.id))


@router.get("/me", response_model=schemas.UsuarioOut, summary="RF02 - Identificação")
def me(usuario: models.Usuario = Depends(usuario_atual)):
    return usuario
