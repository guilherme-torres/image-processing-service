from fastapi import FastAPI
from app.api.v1.routers import api_router


app = FastAPI()

@app.get("/ping")
def healthcheck():
    return "pong"


app.include_router(api_router)
