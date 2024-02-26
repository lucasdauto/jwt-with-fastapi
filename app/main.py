from fastapi import FastAPI
from app.routes import user_router

app = FastAPI()


@app.get("/")
async def health_check():
    return {"status": "ok"}

app.include_router(user_router)