from fastapi import FastAPI

from database.config import Base, engine
from routes.forecast import forecast_router
from routes.health import health_router
from routes.users import users_router
from routes.register import register_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(health_router)
app.include_router(forecast_router)
app.include_router(users_router)
app.include_router(register_router)