from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.endpoints import registro
from app.database import create_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(registro.router, prefix="/api/v1")
