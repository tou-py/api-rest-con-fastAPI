from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.registro import registro_crud
from app.schemas.registro import RegistroCreate, RegistroRead, RegistroUpdate
from app.database import get_session
from typing import List

router = APIRouter()


@router.post("/registros/", response_model=RegistroRead)
async def crear_registro(
    registro: RegistroCreate, session: AsyncSession = Depends(get_session)
):
    """
    Crea un nuevo registro.
    """
    return await registro_crud.create(session, registro)


@router.get("/registros/{registro_id}", response_model=RegistroRead)
async def leer_registro(registro_id: int, session: AsyncSession = Depends(get_session)):
    """
    Obtiene un registro por su ID.
    """
    registro = await registro_crud.get(session, registro_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro


@router.get("/registros/", response_model=List[RegistroRead])
async def leer_registros(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    """
    Obtiene todos los registros con paginación.
    """
    return await registro_crud.get_all(session, skip=skip, limit=limit)


@router.patch("/registros/{registro_id}", response_model=RegistroRead)
async def actualizar_registro(
    registro_id: int,
    registro: RegistroUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Actualiza un registro existente.
    """
    db_registro = await registro_crud.get(session, registro_id)
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return await registro_crud.update(session, db_registro, registro)


@router.delete("/registros/{registro_id}", response_model=RegistroRead)
async def eliminar_registro(
    registro_id: int, session: AsyncSession = Depends(get_session)
):
    """
    Elimina un registro por su ID.
    """
    db_registro = await registro_crud.get(session, registro_id)
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return await registro_crud.delete(session, registro_id)
