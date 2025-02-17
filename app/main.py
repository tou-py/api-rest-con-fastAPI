from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.endpoints import registro, usuarios

# from app.api.v1.endpoints import registro, usuarios
from app.database import create_db
from app.core.logger import app_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Iniciando aplicacion...")
    await create_db()
    yield
    app_logger.info("Aplicacion cerrada correctamente.")


app = FastAPI(lifespan=lifespan)

app.include_router(registro.router, prefix="/api/v1")
app.include_router(usuarios.router, prefix="/api/v1")
