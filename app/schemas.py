from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioOut(BaseModel):
    """Nunca expõe senha nem hash (RN07)."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    email: EmailStr
    perfil: str


def _nao_vazio(v: str | None) -> str | None:
    if v is not None:
        v = v.strip()
        if not v:
            raise ValueError("não pode ser vazio")
    return v


class ComunicadoCreate(BaseModel):
    """Sem campo de autor/perfil: o responsável vem do token (RN06, RN08)."""
    model_config = ConfigDict(extra="forbid")
    titulo: str = Field(max_length=200, examples=["Manutenção programada"])
    conteudo: str = Field(examples=["O sistema ficará fora do ar sábado, das 22h às 23h."])

    _v = field_validator("titulo", "conteudo")(_nao_vazio)


class ComunicadoUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    titulo: str | None = Field(default=None, max_length=200)
    conteudo: str | None = None

    _v = field_validator("titulo", "conteudo")(_nao_vazio)


class ComunicadoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    titulo: str
    conteudo: str
    data_publicacao: datetime
    autor: UsuarioOut
