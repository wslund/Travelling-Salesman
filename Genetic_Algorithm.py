import numpy as np
from scipy import spatial
import pandas as pd
import matplotlib.pyplot as plt
import csv




d = []
data = []
with open('data/scraping_data.csv', mode='r') as file:
    csvFile = csv.reader(file)

    for lines in csvFile:
        d.append(lines)

for i in d[1:]:
    data.append(i)

cities = []

for i in data:
    city = i[1]
    if city not in cities:
        cities.append(city)

#-------------------------------------------------------------------------------------------



df = pd.read_csv('data/scraping_data.csv')
df = df.drop(df.columns[[0]], axis=1)
df = df[df['Distance'] != 0]

#-------------------------------------------------------------------------------------------



dist_matrix = []

def fix_matrix(n, df):

    dist = []
    df = df[df['Start'] == cities[n]]
    df = df['Distance']

    for val in df:
        val = int(val)
        dist.append(val)
    return dist



for i in range(120):
    num = i
    df = df
    distances = fix_matrix(n=num, df=df)
    dist_matrix.append(distances)


#-------------------------------------------------------------------------------------------



points_coordinate = np.array(dist_matrix)  # generate coordinate of points
distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')


def cal_total_distance(routine):
    '''The objective function. input routine, return total distance.
    cal_total_distance(np.arange(num_points))
    '''
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])




from sko.GA import GA_TSP

ga_tsp = GA_TSP(func=cal_total_distance, n_dim=len(dist_matrix), size_pop=50, max_iter=1000, prob_mut=0.05)
best_points, best_distance = ga_tsp.run()


fig, ax = plt.subplots(1, 2)
best_points_ = np.concatenate([best_points, [best_points[0]]])
best_points_coordinate = points_coordinate[best_points_, :]
ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
ax[1].plot(ga_tsp.generation_best_Y)
plt.show()

#-------------------------------------------------------------------------------------------

