import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1.routers import api_router


app = FastAPI(title="Asynchronous image processing service")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def healthcheck():
    return {"message": "hello, world!"}


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
