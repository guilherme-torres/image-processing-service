from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.routers import api_router


app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def healthcheck():
    return {"message": "hello, world!"}


app.include_router(api_router)
