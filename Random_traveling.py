

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



df = pd.read_csv('data/scraping_data.csv')

df = df.drop(df.columns[[0]], axis=1)
df = df[df['Distance'] != 0]

#-----------------------------------------------------------------------------



def travel(start_city, cities):
    if cities.shape[0] == 0:
        return 0
    targets = cities[cities['Start'] == start_city]
    target = targets.sample(n=1)
    target_city: str = target['Target'].values[0]
    distance = target['Distance'].values[0]
    cities = cities[cities['Start'] != start_city]
    cities = cities[cities['Target'] != start_city]

    return travel(target_city, cities) + distance

#-----------------------------------------------------------------------------



def travel_loop(cities):
    total_distance = 0
    start_city: str = cities['Target'].sample(n=1).values[0]

    while cities.shape[0] > 0:
        targets = cities[cities['Start'] == start_city]
        target = targets.sample(n=1)
        target_city: str = target['Target'].values[0]
        distance = target['Distance'].values[0]
        total_distance += distance
        print(start_city, target_city, distance, total_distance)
        start_city = target_city
        cities = cities[cities['Start'] != start_city]
        cities = cities[cities['Target'] != start_city]
    return total_distance





n = 10 # How many times you want randomize.
distances = []

for _ in range(n):
    cities = df[:]
    start_city: str = cities['Target'].sample(n=1).values[0]
    distances.append(travel(start_city, cities))

#-----------------------------------------------------------------------------


route = sorted(distances, key=lambda x: float(x))
print(f'The shortest route: {route[0]}')


fig,ax = plt.subplots(1,1)
a = np.array(distances)
ax.hist(a, bins='auto')
plt.show()
