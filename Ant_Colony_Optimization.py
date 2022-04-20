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

#------------------------------------------------------------------



df = pd.read_csv('data/scraping_data.csv')
df = df.drop(df.columns[[0]], axis=1)
df = df[df['Distance'] != 0]

#------------------------------------------------------------------



dist_matrix = []

def fix_matrix(n, df):

    dist = []

    df = df[df['Start'] == cities[n]]
    df = df['Distance']
    for val in df:
        dist.append(val)
    return dist



for i in range(120):
    num = i
    df = df
    distances = fix_matrix(n=num, df=df)
    dist_matrix.append(distances)

#------------------------------------------------------------------



matrix = np.array(dist_matrix)

distance_matrix = spatial.distance.cdist(matrix, matrix, metric='euclidean')


def cal_total_distance(routine):
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])



from sko.ACA import ACA_TSP

aca = ACA_TSP(func=cal_total_distance, n_dim=120,
              size_pop=50, max_iter=10,
              distance_matrix=distance_matrix)

best_x, best_y = aca.run()


fig, ax = plt.subplots(1, 2)
best_points_ = np.concatenate([best_x, [best_x[0]]])
best_points_coordinate = matrix[best_points_, :]
ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
pd.DataFrame(aca.y_best_history).cummin().plot(ax=ax[1])
plt.show()

#------------------------------------------------------------------