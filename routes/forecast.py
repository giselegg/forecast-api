from fastapi import APIRouter, HTTPException

from services.fetch_forecast import fetch_forecast

forecast_router = APIRouter(prefix="/forecast")


@forecast_router.get("")
def empty_forecast():
    raise HTTPException(status_code=404, detail="You must enter a city")


@forecast_router.get("/{city_name}")
def get_forecast(city_name: str):
    try:
        response = fetch_forecast(city_name)
        if response:
            return response
    except Exception as e:
        raise HTTPException(status_code=400)
