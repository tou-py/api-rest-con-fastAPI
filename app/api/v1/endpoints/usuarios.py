from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import get_session
from app.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate, APIResponse
from app.crud.usuario import usuario_crud

router = APIRouter()


@router.post("/register/", response_model=APIResponse[UsuarioRead])
async def registrar_usuario(
    usuario: UsuarioCreate, session: AsyncSession = Depends(get_session)
):
    """
    Crea un usuario
    """
    try:
        usuario_nuevo = await usuario_crud.create(session, usuario)
        return APIResponse(
            data=usuario_nuevo,
            message="Usuario creado exitosamente",
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        )


@router.post("/login/", response_model=APIResponse[UsuarioRead])
async def login_usuario(
    email: str, password: str, session: AsyncSession = Depends(get_session)
):
    usuario = await usuario_crud.authenticate(session, email, password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas"
        )
    return usuario
