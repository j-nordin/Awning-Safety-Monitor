from datetime import datetime

import requests

LAT = "57.581368"
LON = "11.941073"
BASE_URL = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/"


def fetch_current_wind(lon=LON, lat=LAT):
    wind_speed, wind_gust_speed = None, None
    res = requests.get(BASE_URL + f"lon/{lon}/lat/{lat}/data.json").json()
    forecasts_hourly = [forecast for forecast in res['timeSeries']]

    now = datetime.now().time()
    closest_forecast_hour = now.hour if now.minute < 30 else now.hour + 1

    closest_forecast = forecasts_hourly[closest_forecast_hour]

    for parameter in closest_forecast['parameters']:
        if parameter['name'] == 'ws':
            wind_speed = float(parameter['values'][0])
        elif parameter['name'] == 'gust':
            wind_gust_speed = float(parameter['values'][0])

    return {'wind_speed': wind_speed, 'wind_gust_speed': wind_gust_speed}


if __name__ == "__main__":
    print(fetch_current_wind())
