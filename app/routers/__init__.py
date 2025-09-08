from app.routers.auth import router as auth_router

from fastapi import FastAPI

app = FastAPI(root_path="/api", prefix="/v1")

app.include_router(auth_router, prefix="/auth")
