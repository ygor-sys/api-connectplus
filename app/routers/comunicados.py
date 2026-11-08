from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from .. import models, schemas
from ..database import get_db
from ..deps import somente_admin, usuario_atual

router = APIRouter(prefix="/comunicados", tags=["Comunicados"])


def _buscar(db: Session, comunicado_id: int) -> models.Comunicado:
    c = db.get(models.Comunicado, comunicado_id)
    if c is None:  # RN05
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Comunicado não encontrado")
    return c


def _exigir_autor(c: models.Comunicado, usuario: models.Usuario) -> None:
    """Restrição ao próprio recurso: só o autor altera/exclui o seu comunicado -> 403."""
    if c.autor_id != usuario.id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Apenas o autor pode alterar ou excluir este comunicado",
        )


@router.post("", response_model=schemas.ComunicadoOut, status_code=status.HTTP_201_CREATED,
             summary="RF03 - Publicar (admin)")
def publicar(dados: schemas.ComunicadoCreate, db: Session = Depends(get_db),
             admin: models.Usuario = Depends(somente_admin)):
    c = models.Comunicado(titulo=dados.titulo, conteudo=dados.conteudo, autor_id=admin.id)  # RN06
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


@router.get("", response_model=list[schemas.ComunicadoOut], summary="RF04 - Listar")
def listar(db: Session = Depends(get_db), _: models.Usuario = Depends(usuario_atual)):
    stmt = (select(models.Comunicado).options(joinedload(models.Comunicado.autor))
            .order_by(models.Comunicado.data_publicacao.desc(), models.Comunicado.id.desc()))
    return db.scalars(stmt).all()


@router.get("/{comunicado_id}", response_model=schemas.ComunicadoOut, summary="RF04 - Consultar um")
def consultar(comunicado_id: int, db: Session = Depends(get_db),
              _: models.Usuario = Depends(usuario_atual)):
    return _buscar(db, comunicado_id)


@router.put("/{comunicado_id}", response_model=schemas.ComunicadoOut, summary="RF05 - Atualizar (admin autor)")
def atualizar(comunicado_id: int, dados: schemas.ComunicadoUpdate, db: Session = Depends(get_db),
              admin: models.Usuario = Depends(somente_admin)):
    c = _buscar(db, comunicado_id)
    _exigir_autor(c, admin)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        if valor is not None:
            setattr(c, campo, valor)
    db.commit()
    db.refresh(c)
    return c


@router.delete("/{comunicado_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="RF06 - Excluir (admin autor)")
def excluir(comunicado_id: int, db: Session = Depends(get_db),
            admin: models.Usuario = Depends(somente_admin)):
    c = _buscar(db, comunicado_id)
    _exigir_autor(c, admin)
    db.delete(c)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
