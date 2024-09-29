from fastapi import FastAPI
from routers.api_router import api_router
from fastapi.middleware.cors import CORSMiddleware
from database.connect import engine
from database.models import Base

app = FastAPI(
    title="API для управления складом",
    description="Простое API для управления складом. Позволяет добавлять, удалять, обновлять и получать продукты и заказы.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
