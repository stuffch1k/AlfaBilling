from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth import router as authRouter


def get_application() -> FastAPI:
    app = FastAPI(title="AlfaBilling", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(authRouter, prefix='/api')
    return app


app: FastAPI = get_application()
