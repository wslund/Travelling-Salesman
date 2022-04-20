import requests
from bs4 import BeautifulSoup
from math import sin, cos, sqrt, atan2, radians
import csv
import pandas as pd



page = requests.get('https://www.infoplease.com/world/geography/major-cities-latitude-longitude-and-corresponding-time-zones')  # Getting page HTML through request
soup = BeautifulSoup(page.content, 'html.parser')  # Parsing content using beautifulsoup

links = soup.select("td")

first = []
second = []
clean = []

for anchor in links:
    d = anchor.text
    first.append(d)

first = list(zip(*[iter(first)]*6))
second_clean = []


for i in first:
    bridge = []
    city = i[0]
    city = city.split(",")
    city = city[0]

    lat1 = i[1]
    lat1 = int(lat1)
    lat2 = i[2]
    lat2 = lat2.split()
    lat_course = lat2[1]

    lon1 = i[3]
    lon1 = int(lon1)
    lon2 = i[4]
    lon2 = lon2.split()
    long_course = lon2[1]

    if lat_course == 'S':
        lat2 = int(lat2[0])
        latitude = f'-{int(lat1)}.{int(lat2)}'
        latitude = float(latitude)


    if lat_course == 'N':
        lat2 = int(lat2[0])
        latitude = f'{int(lat1)}.{int(lat2)}'
        latitude = float(latitude)

    if long_course == 'W':
        lon2 = int(lon2[0])
        longitude = f'-{int(lon1)}.{int(lon2)}'
        longitude = float(longitude)

    if long_course == 'E':
        lon2 = int(lon2[0])
        longitude = f'{int(lon1)}.{int(lon2)}'
        longitude = float(longitude)
    second_clean.append([city, latitude, lat_course, longitude, long_course])

#-------------------------------------------------------------------------------------

third_clean = []



for i in range(len(second_clean)):
    start = second_clean[i]
    start_city = second_clean[i][0]
    for num in range(len(second_clean)):
        R = 6370

        start_lat1 = radians(start[1])
        start_lon1 = radians(start[3])

        target = second_clean[num]
        target_city = second_clean[num][0]
        target_lat2 = radians(target[1])
        target_lon2 = radians(target[3])

        dlon = target_lon2 - start_lon1
        dlat = target_lat2 - start_lat1

        a = sin(dlat / 2) ** 2 + cos(start_lat1) * cos(target_lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        third_clean.append([start_city, target_city, distance])

#-------------------------------------------------------------------------------------



Start = []
Target = []
Distance = []

for i in third_clean:
    start = i[0]
    target =  i[1]
    dist = i[2]
    Start.append(start)
    Target.append(target)
    Distance.append(dist)



dict = {'Start': Start, 'Target': Target, 'Distance': Distance}
df = pd.DataFrame(dict)
df.to_csv('data\scraping_data.csv')

#-------------------------------------------------------------------------------------

