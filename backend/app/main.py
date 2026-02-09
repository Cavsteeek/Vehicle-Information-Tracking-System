from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from .database import engine, Base
from .routers import auth_routes, vehicle_routes
from . import scheduler  # starts background jobs
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    scheduler.start_scheduler()
    yield

app = FastAPI(
    title="Vehicle Monitoring API",
    lifespan=lifespan
)

origins = [
    "http://localhost:5173",  # Vue dev server
    "http://127.0.0.1:5173",
    "https://vpms.onrender.com"  # deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows frontend
    allow_credentials=True,
    allow_methods=["*"],              # Allows OPTIONS, POST, GET, etc.
    allow_headers=["*"],              # Allows Content-Type and Authorization headers
)

@app.get("/")
def health_check():
    return {"status": "Backend is running", "timestamp": datetime.now()}

app.include_router(auth_routes.router)
app.include_router(vehicle_routes.router)
