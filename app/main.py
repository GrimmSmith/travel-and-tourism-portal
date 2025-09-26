from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api import auth, destinations, bookings  # Import your routers

app = FastAPI(title="Travel Portal Backend")

# Serve HTML templates from app/templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(destinations.router, prefix="/api", tags=["destinations"])
app.include_router(bookings.router, prefix="/api", tags=["bookings"])

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Serve login page
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Serve dashboard page
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# Serve destination page
@app.get("/destinations", response_class=HTMLResponse)
async def destination_page(request: Request):
    return templates.TemplateResponse("destination.html", {"request": request})

# Serve booking page
@app.get("/booking", response_class=HTMLResponse)
async def booking_page(request: Request):
    return templates.TemplateResponse("booking.html", {"request": request})