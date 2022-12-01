from bs4 import BeautifulSoup
import requests
import pandas as pd


array_cities = []

url = "https://en.wikipedia.org/wiki/List_of_cities_in_the_European_Union_by_population_within_city_limits"
headers = {'Accept-Language': 'en-US,en;q=0.8'}
response = requests.get(url, headers=headers)
eu_cities_unstructured = BeautifulSoup(response.content, 'html.parser')
eu_cities_unstructured
table = eu_cities_unstructured.find('table', {'class': 'wikitable sortable'})
rows = table.find_all('tr')
headers = [th.text.strip() for th in rows[0].find_all('th')]
eu_cities = []
population = []
country = []
latitude = []
longitude = []
eu_cities_dicitonary = {}
for row in rows[1:]:
    eu_cities.append(row.find_all('td')[1].get_text())
    population.append(row.find_all('td')[3].get_text())
    country.append(row.find_all('td')[2].get_text())

# for link in eu_cities:
#     url = f'https://en.wikipedia.org/wiki/{link}'
#     headers = {'Accept-Language': 'en-US,en;q=0.8'}
#     response = requests.get(url, headers=headers)
#     eu_cities_coordinates.append(
#         BeautifulSoup(response .content, 'html.parser'))
# for city in eu_cities_coordinates:
#     if (len(city.select("span .latitude")) == 0):
#         latitude.append(0)
#         longitude.append(0)
#     else:
#         latitude.append(city.select("span .latitude")[0].get_text())
#         longitude.append(city.select("span .longitude")[0].get_text())


cities_dicitonary = {}
values = [eu_cities, population, country,
          #     latitude, longitude
          ]
cols = ["eu_cities", "population", "country"
        #   , "latitude", "longitude"
        ]
for key, value in zip(cols, values):
    cities_dicitonary[key] = value
# countries
cities_df = pd.DataFrame(cities_dicitonary).head(30)
cities_df.head(3)
