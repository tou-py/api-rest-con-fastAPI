from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.registro import registro_crud
from app.models.registro import Registro
from app.schemas.registro import (
    RegistroCreate,
    RegistroRead,
    RegistroUpdate,
    APIResponse,
)
from app.database import get_session
from typing import List

router = APIRouter()


@router.post("/registros/", response_model=APIResponse[RegistroRead])
async def crear_registro(
    registro: RegistroCreate, session: AsyncSession = Depends(get_session)
):
    """
    Crea un nuevo registro.
    """
    try:
        db_registro = await registro_crud.create(session, registro)
        return APIResponse(
            data=db_registro,
            message="Registro creado correctamente",
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@router.get("/registros/{registro_id}", response_model=APIResponse[RegistroRead])
async def leer_registro(registro_id: int, session: AsyncSession = Depends(get_session)):
    """
    Obtiene un registro por su ID.
    """
    try:
        db_registro = await registro_crud.get(session, registro_id)
        if not db_registro:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return APIResponse(
            data=db_registro,
            message="Registro obtenido",
            status_code=status.HTTP_200_OK,
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.get("/registros/", response_model=APIResponse[List[RegistroRead]])
async def leer_registros(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    """
    Obtiene todos los registros con paginación.
    """
    try:
        registros = await registro_crud.get_all(session, skip=skip, limit=limit)
        return APIResponse(
            data=registros,  # Devuelve la lista de registros directamente
            message="Registros obtenidos correctamente",
            status_code=status.HTTP_200_OK,
            pagination={"skip": skip, "limit": limit, "total": len(registros)},
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ex))


@router.patch("/registros/{registro_id}", response_model=APIResponse[RegistroRead])
async def actualizar_registro(
    registro_id: int,
    registro: RegistroUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Actualiza un registro existente.
    """
    try:
        db_registro = await registro_crud.get(session, registro_id)
        if not db_registro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado"
            )
        db_registro_actualizado = await registro_crud.update(
            session, db_registro, registro
        )
        return APIResponse(
            data=db_registro_actualizado,
            message="Registro actualizado correctamente",
            status_code=status.HTTP_200_OK,
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        )


@router.delete("/registros/{registro_id}", response_model=APIResponse[RegistroRead])
async def eliminar_registro(
    registro_id: int, session: AsyncSession = Depends(get_session)
):
    """
    Elimina un registro por su ID.
    """
    try:
        db_registro = await registro_crud.get(session, registro_id)
        if not db_registro:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        db_registro_eliminado = await registro_crud.delete(session, registro_id)
        return APIResponse(
            data=db_registro_eliminado,
            message="Registro eliminado con exito",
            status_code=status.HTTP_200_OK,
        )
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
