from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from passlib.context import CryptContext
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.logger import app_logger
from app.crud.base import CRUDBase, get_transaction

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CRUDUsuario(CRUDBase[Usuario, UsuarioCreate, UsuarioUpdate]):

    async def create(self, session: AsyncSession, obj_in: UsuarioCreate) -> Usuario:
        """
        Sobreescribe el metoo create para hashear la contra antes de guardar el usuario
        """
        # Primero, verificar si el email ya existe en la bd
        existing_user = await self.get_by_email(session, obj_in.email)
        if existing_user:
            raise ValueError("El email ya esta registrado")

        hashed_password = pwd_context.hash(obj_in.password)

        # luego de encriptar la contra se crea el objeto Usuario
        db_obj = Usuario(
            nombres=obj_in.nombres,
            apellidos=obj_in.apellidos,
            email=obj_in.email,
            hashed_password=hashed_password,
        )

        async with get_transaction(session):
            app_logger.info(f"Creando un usuario: {obj_in.email}")
            session.add(db_obj)

        await session.refresh(db_obj)
        app_logger.info(f"Usuario creado exitosamente: {db_obj.email}")
        return db_obj

    async def get_by_email(
        self, session: AsyncSession, email: str
    ) -> Optional[Usuario]:
        """
        Busca un usuario en la bd por su email
        """
        from sqlmodel import select

        result = await session.scalars(select(Usuario).where(Usuario.email == email))
        return result.first()

    async def authenticate(
        self, session: AsyncSession, email: str, password: str
    ) -> Optional[Usuario]:
        """
        Autentica un usuario usando email y contra
        """
        usuario = await self.get_by_email(session, email)

        if usuario and pwd_context.verify(password, usuario.hashed_password):
            return usuario


usuario_crud = CRUDUsuario(Usuario)
