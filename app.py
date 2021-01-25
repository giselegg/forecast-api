from fastapi import FastAPI

from routes.forecast import forecast_router
from routes.health import health_router
from routes.users import users_router

app = FastAPI()

app.include_router(health_router)
app.include_router(forecast_router)
app.include_router(users_router)
