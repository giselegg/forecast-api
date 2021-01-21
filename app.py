from datetime import datetime
from typing import Dict
from fastapi import FastAPI, HTTPException

from services.fetch_forecast import fetch_forecast

app = FastAPI()


@app.get("/health/")
def alive():
    """
    Check if API is alive
    
    Return
        dict: timestamp
    """
    return {"timestamp": datetime.now()}


@app.get("/forecast/")
def empty_forecast():
    """
    Raises exception when user doesn't send city name as parameter
    """
    raise HTTPException(status_code=404, detail="You must enter a city")


@app.get("/forecast/{city_name}")
def get_forecast(city_name: str):
    """
    Get forecast by city name
    
    Parameters
        str: city name
    
    Return
        dict: response from fetch_forecast service
    """
    try:
        response = fetch_forecast(city_name)
        if not response:
            raise Exception
        return response
    except Exception as e:
        print(e)