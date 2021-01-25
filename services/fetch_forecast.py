from requests import get
from decouple import config


def fetch_forecast(city):
    key = config("KEY")
    try:
        response = get(f"https://api.hgbrasil.com/weather?array_limit=7&fields=only_results,temp,city_name,forecast,max,min,date,description,condition,weekday&key={key}&city_name={city}")
        return response.json()
        if response.status_code != 200:
            raise Exception
    except Exception as e:
        print(e)
