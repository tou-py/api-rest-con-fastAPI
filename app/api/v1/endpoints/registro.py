from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.crud.registro import registro_crud
from app.schemas.registro import RegistroCreate, RegistroRead, RegistroUpdate
from app.database import get_session
from typing import List

router = APIRouter()


@router.post("/registros/", response_model=RegistroRead)
def crear_registro(registro: RegistroCreate, session: Session = Depends(get_session)):
    """
    Crea un nuevo registro.
    """
    return registro_crud.create(session, registro)


@router.get("/registros/{registro_id}", response_model=RegistroRead)
def leer_registro(registro_id: int, session: Session = Depends(get_session)):
    """
    Obtiene un registro por su ID.
    """
    registro = registro_crud.get(session, registro_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro


@router.get("/registros/", response_model=List[RegistroRead])
def leer_registros(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    """
    Obtiene todos los registros con paginación.
    """
    return registro_crud.get_all(session, skip=skip, limit=limit)


@router.patch("/registros/{registro_id}", response_model=RegistroRead)
def actualizar_registro(
    registro_id: int, registro: RegistroUpdate, session: Session = Depends(get_session)
):
    """
    Actualiza un registro existente.
    """
    db_registro = registro_crud.get(session, registro_id)
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro_crud.update(session, db_registro, registro)


@router.delete("/registros/{registro_id}", response_model=RegistroRead)
def eliminar_registro(registro_id: int, session: Session = Depends(get_session)):
    """
    Elimina un registro por su ID.
    """
    db_registro = registro_crud.get(session, registro_id)
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro_crud.delete(session, registro_id)
