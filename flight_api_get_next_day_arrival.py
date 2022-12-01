# Give the city latitude and Longitude and get the next days arrival of every city airport in range 100 klm
import requests
import pandas as pd
import datetime
import requests
# GET THE KEY
import os
from dotenv import load_dotenv
load_dotenv()
UR_API_KEY = os.getenv('DB_ARRIVALS_KEY')


def get_nextday_arrivals(lat, log):

    coordinates = str(lat) + '/' + str(log)
    # counting next day
    date_time = datetime.date.today() + datetime.timedelta(days=1)
    airport_time = date_time.strftime("%Y-%m-%d")
    # api call for the "icao" number of each airport as unique key
    url = f'https://aerodatabox.p.rapidapi.com/airports/search/location/{coordinates}/km/100/16'

    headers = {
        "X-RapidAPI-Key": UR_API_KEY,
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)
    flights = response.json()
    clean_flights = pd.json_normalize(
        flights["items"],

        meta=['dt_txt', ['icao', 'icao'], [
            'name', 'name'], ['location', 'location']],
        errors='ignore'
    )
    clean_flights.rename(columns={'location.lon': 'lon',
                                  'location.lat': 'lat'}, inplace=True)

    # get the list for the airports
    icao_list = pd.DataFrame(clean_flights).icao.to_list()

    icao_for_each_airport = []
    arrivals_for_each_airport = []
    # looping over the icao_list to get all arrivals
    if len(icao_list):
        for icao in icao_list:
            try:
                url = f'https://aerodatabox.p.rapidapi.com/flights/airports/icao/{icao}/{airport_time}T08:00/{airport_time}T20:00'
                querystring = {"withLeg": "true", "direction": "Arrival", "withCancelled": "true", "withCodeshared": "true", "withCargo": "false",
                               "withPrivate": "false", "withLocation": "true"}
                headers = {
                    "X-RapidAPI-Key": UR_API_KEY,
                    "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"}
                response = requests.request(
                    "GET", url, headers=headers, params=querystring)
                arivals_all = response.json()

            except:
                print(f'this{icao} is a private aiport, it doesnt concern u ')
                pass
            # creating arrivals dataframe

            arivals_df = pd.json_normalize(
                arivals_all["arrivals"])
            arivals_df.drop(['status', 'codeshareStatus', 'isCargo',
                             'departure.airport.icao', 'departure.airport.iata', 'departure.quality',
                             'arrival.scheduledTimeLocal', 'arrival.scheduledTimeUtc', 'arrival.quality', 'aircraft.model',
                             'airline.name', 'departure.scheduledTimeLocal',
                             'departure.scheduledTimeUtc', 'departure.terminal', 'callSign',
                             'departure.actualTimeLocal', 'departure.actualTimeUtc', 'aircraft.reg', 'aircraft.modeS',
                             'departure.checkInDesk', 'departure.runwayTimeLocal', "arrival.actualTimeUtc", 'departure.gate',
                             'departure.runwayTimeUtc'], axis=1, inplace=True, errors='ignore')
            arivals_df.rename(columns={'departure.airport.name': 'where_from',
                                       'arrival.actualTimeLocal': 'arrival_time',
                                       'arrival.terminal': 'terminal', }, inplace=True, errors='ignore')
            arivals_df["icao"] = icao
            arrivals_for_each_airport.append(arivals_df)

            #  arrivals_total_detailed = pd.merge(arrivals_total, clean_flights, on='icao', how='inner')

    return pd.concat(arrivals_for_each_airport, ignore_index=True)


"""You can chooose any city but only sure that the coordinates are accurate. """

London = get_nextday_arrivals("51.511142", "-0.103869")
Madrid = get_nextday_arrivals("40.2500", "03.4209")
Rome = get_nextday_arrivals("41.5336", "12.2858")
Paris = get_nextday_arrivals("48.5124", "2.2108")
all_cities_arrival = [Madrid, Rome, Paris]

"""Now that we have the list lets concatinate it and create a (clean)Dataframe with:

"""

all_cities_arrival_df = pd.concat(all_cities_arrival, ignore_index=True)
all_cities_arrival_df['arrival_time'] = pd.to_datetime(
    all_cities_arrival_df['arrival_time'], utc=True)
all_cities_arrival_df['terminal'] = all_cities_arrival_df['terminal'].fillna(
    "not announced")
all_cities_arrival_df['arrival_time'] = all_cities_arrival_df['arrival_time'].fillna(
    0)
