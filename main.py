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

# Add CORS Middleware (Optional, based on your needs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust allowed origins for CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the main API router that contains both products and orders
app.include_router(api_router)


# Add startup and shutdown events if needed (Optional)
@app.on_event("startup")
async def startup_event():
    # If you need to create database tables automatically
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Initialize and run the app if this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
