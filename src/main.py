import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth import router as authRouter
from src.service.routing.tarif import tarif_router

def get_application() -> FastAPI:
    app = FastAPI(title="AlfaBilling", version="1.0.0", openapi_prefix= '/api')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(authRouter)
    app.include_router(tarif_router, prefix='/tarif')
    return app


app: FastAPI = get_application()

@app.get("/")
def main():
    return "main"

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, reload=True, workers=2)
