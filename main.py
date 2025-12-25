from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.database import global_init, create_db_and_tables, delete_db_and_tables
from routers.auth import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    global_init()
    await create_db_and_tables()
    yield
    await delete_db_and_tables()


def create_application():
    return FastAPI(
        title="Auth APP",
        description="Тестовое задание",
        version="0.0.1",
        responses={404: {"description": "Not found"}},
        default_response_class=ORJSONResponse,
        lifespan=lifespan
    )


app = create_application()


def _configure():
    app.include_router(router)


_configure()