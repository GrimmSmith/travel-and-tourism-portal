from fastapi import FastAPI
from app.api import auth

app = FastAPI(title="Travel Portal Backend")
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/health")
async def health():
    return {"status": "ok"}
    