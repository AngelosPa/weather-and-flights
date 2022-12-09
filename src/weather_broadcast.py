

import pandas as pd
import requests
# GET THE KEY
import os
from dotenv import load_dotenv
load_dotenv()
UR_API_KEY = os.getenv('DB_WEATHER_KEY')


def weather_boradcast(towns_list):
    dataframes_for_each_town = []
    API_key = UR_API_KEY
    for town in towns_list:
        weather = requests.get(
            f"http://api.openweathermap.org/data/2.5/forecast?q={town}&appid={API_key}&units=metric")
        weather_resp = weather.json()
        # normalize method can create the dataframe immidiately from an json/ dictionary
        weather_df = pd.json_normalize(
            weather_resp['list'],
            record_path=['weather'],
            meta=['dt_txt', ['main', 'temp'], ['main', 'feels_like'], ['clouds', 'all'], ['rain', '3h'], ['snow', '3h'], ['wind', 'speed'],
                  ['wind', 'deg'], ['main', 'humidity'], ['main', 'pressure']],
            errors='ignore'
        )
        weather_df.drop(['wind.deg', 'main.humidity', 'main.pressure', 'main.feels_like',
                        'icon', 'wind.deg', "rain.3h", "clouds.all",	"snow.3h"], axis=1, inplace=True)
        weather_df.rename(columns={'main': 'outlook',
                                   'description': 'detailed_outlook',
                                   'dt_txt': 'forecast_time',
                                   'main.temp': 'temperature',

                                   'wind.speed': 'wind_speed',
                                   },
                          inplace=True)

        weather_df.insert(0, 'city', weather_resp["city"]["name"])
        weather_df.insert(1, 'country', weather_resp["city"]["country"])

        dataframes_for_each_town.append(weather_df)

    return pd.concat(dataframes_for_each_town, ignore_index=True)




top_cities_weather = weather_boradcast(["Madrid", "Rome", "Paris"])
top_cities_weather.sample(10)
