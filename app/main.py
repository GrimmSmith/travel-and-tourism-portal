from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api import auth

app = FastAPI(title="Travel Portal Backend")

# Serve HTML templates from app/templates
templates = Jinja2Templates(directory="app/templates")

# Include your auth router
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Serve login page
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})