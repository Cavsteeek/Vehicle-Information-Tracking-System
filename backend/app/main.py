from fastapi import FastAPI
from .database import engine, Base
from .routers import auth_routes, vehicle_routes
from . import scheduler  # starts background jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vehicle Monitoring API")

app.include_router(auth_routes.router)
app.include_router(vehicle_routes.router)
