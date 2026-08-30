from fastapi import FastAPI

from app.routers import auth
from app.routers import users
from app.routers import drivers
from app.routers import vehicles
from app.routers import rides
from app.routers import ratings


app = FastAPI(
    title="Taxi App API",
    version="1.0.0",
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(ratings.router)
app.include_router(drivers.router)
app.include_router(vehicles.router)
app.include_router(rides.router)


@app.get("/")
def root():
    return {
        "message": "Taxi App API is running"
    }