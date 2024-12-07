import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth import router as authRouter
from src.number.routing.number import activated_router, number_router
from src.service.routing.tarif import tarif_router
from src.service.routing.addition_category import category_router
from src.service.routing.addition import addition_router
from src.transaction.routing.payment import payment_router
from src.transaction.routing.write_off import write_off_router

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
    app.include_router(category_router, prefix='/category')
    app.include_router(addition_router, prefix='/addition')
    app.include_router(activated_router, prefix='/activated')
    app.include_router(number_router, prefix='/number')
    app.include_router(write_off_router, prefix='/write_off')
    app.include_router(payment_router, prefix = "/payment")
    return app


app: FastAPI = get_application()

@app.get("/")
def main():
    return "Тут будет пейджа с инфо юзера (номер телефона, остатки и тд)"

if __name__ == "__main__":
    uvicorn.run("__main__:app", host="127.0.0.1", port=8008, reload=True, workers=4)
