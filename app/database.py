from sqlmodel import SQLModel, create_engine, Session
from .config import settings


# Con esto se crea el motor de la base de datos
engine = create_engine(settings.DATABASE_URL, echo=True)


# Obtener la sesion de la base de datos
def get_session():
    with Session(engine) as session:
        yield session


# Si no existen, crea las tablas de la base de datos
def create_db():
    SQLModel.metadata.create_all(engine)
