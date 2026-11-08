from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models, security
from .database import get_db

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


def usuario_atual(token: str = Depends(oauth2), db: Session = Depends(get_db)) -> models.Usuario:
    """Exige identificação válida (RN01). Sem token/token inválido -> 401."""
    erro = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas ou ausentes",
        headers={"WWW-Authenticate": "Bearer"},
    )
    uid = security.ler_token(token)
    if uid is None:
        raise erro
    usuario = db.get(models.Usuario, uid)
    if usuario is None:
        raise erro
    return usuario


def somente_admin(usuario: models.Usuario = Depends(usuario_atual)) -> models.Usuario:
    """Identificado, mas sem permissão -> 403 (RN02, RN03)."""
    if usuario.perfil != models.ADMINISTRADOR:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operação permitida apenas para administradores",
        )
    return usuario
