from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from database.config import SessionLocal
from database.get_db import get_db
from services.auth import check_authorization
from services.fetch_forecast import fetch_forecast
from services.logger import RequestLogger


# Logger
logger = RequestLogger(__name__, "requests.log").logger

# Security
security = HTTPBasic()

# Routes
forecast_router = APIRouter(prefix="/forecast")


@forecast_router.get("")
def empty_forecast(db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if check_authorization(db, credentials):
        raise HTTPException(status_code=404, detail="You must enter a city")


@forecast_router.get("/{city_name}")
def get_forecast(city_name: str, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(security)):
    if check_authorization(db, credentials):
        try:
            response = fetch_forecast(city_name)
            if response:
                logger.info(f"username: {credentials.username}, request: forecast, result: {response}")
                return response
        except Exception as e:
            raise HTTPException(status_code=400)

