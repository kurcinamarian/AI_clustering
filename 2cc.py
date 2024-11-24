import random
import plotly.graph_objs as go
import math
##########################################################################################

#globalne premenne a ich prvotna inicializacia

#Pocet pociatocnych bodov a vsetkych bodov
first_num = int(input("Zadaj pocet prvych bodov: "))
total_num = int(input("Zadaj pocet vsetkych bodov: "))

#vyber typu klastrovania
if input("Chces klastrovat pomocou centroidu alebo medoidu?(c/m): ") == "m":
    medoid = True
else:
    medoid = False

#data o suradniciach bodov
points_x = [0] * total_num
points_y = [0] * total_num

#pocet klastrov
clusters_num = total_num
#data o prvkoch v jednotlivych klastroch
clusters = [[] for _ in range(total_num)]
#data o suradniciach centra klastrov
clusters_x = [0] * total_num
clusters_y = [0] * total_num

#matica vsetkych vzdialenosti klastrov
distances = [[0.0] * total_num for _ in range(total_num)]

#########################################################################################################

#funkcia na vytvorenie bodov
def create_points():
    global points_x, points_y, clusters_x, clusters_y, clusters
    # rozmery platna
    x_min, x_max = -5000, 5000
    y_min, y_max = -5000, 5000
    #vytvorenie pociatocnych bodov
    for i in range(first_num):
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)
        while x in clusters_x and y in clusters_y:
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
        points_x[i] = x
        points_y[i] = y
    #vytvorenie ostatnych bodov
    for i in range(first_num, total_num):
        #vyber rodica noveho bodu
        point_parent = random.randint(0, i - 1)
        #vytvorenie offsetu ak je bod vzdialeny od okraja viac ako 100
        if -4900 < points_x[point_parent] < 4900:
            x_offset = random.randint(-100, 100)
        #ak nie je vytvorenie upraveneho offsetu
        elif points_x[point_parent] <= -4900:
            x_offset = random.randint(5000 + points_x[point_parent], 100)
        else:
            x_offset = random.randint(-100, 5000 - points_x[point_parent])

        # vytvorenie offsetu ak je bod vzdialeny od okraja viac ako 100
        if -4900 < points_y[point_parent] < 4900:
            y_offset = random.randint(-100, 100)
        # ak nie je vytvorenie upraveneho offsetu
        elif points_y[point_parent] <= -4900:
            y_offset = random.randint(5000 + points_y[point_parent], 100)
        else:
            y_offset = random.randint(-100, 5000 - points_y[point_parent])

        #vytvorenie noveho bodu s offsetom od rodica
        points_x[i] = points_x[point_parent] + x_offset
        points_y[i] = points_y[point_parent] + y_offset
    #kopirovanie dat bodov do dat klastrov, na zaciatku je kazdy bod vlastnym klastrom
    clusters_x = points_x.copy()
    clusters_y = points_y.copy()
    for i in range(clusters_num):
        clusters[i].append(i)

#funkcia na vypocet pociatocnej matice vzdialenosti
def calculate_initial_distances():
    global distances, clusters_num, clusters_x, clusters_y
    for i in range(clusters_num):
        for j in range(i + 1, clusters_num):
            #vypocet vzdialenosti pomocou pytagorovej vety
            distances[i][j] = math.sqrt((clusters_x[i] - clusters_x[j]) ** 2 + (clusters_y[i] - clusters_y[j]) ** 2)
            distances[j][i] = distances[i][j]

#funkcie na najdnie najblizsich klastrov
def find_min():
    global distances, clusters_num
    min_distance = distances[0][1]
    min_a, min_b = 0,1
    for i in range(clusters_num - 1):
        for j in range(i + 1, clusters_num):
            if distances[i][j] < min_distance:
                min_distance = distances[i][j]
                min_a, min_b = i, j
    return min_a, min_b

#funkcia na kontroly podmienky: priemerna vzdialenost bodov od stredu nie je viac ako 500
def average(previous, adding):
    global points_x, points_y, clusters
    combined_points = clusters[previous] + clusters[adding]
    num_points = len(combined_points)

    #vypocitanie teoretickeho noveho centroidu
    sum_x, sum_y = 0,0
    for point in combined_points:
        sum_x += points_x[point]
        sum_y += points_y[point]
    center_x = sum_x / num_points
    center_y = sum_y / num_points
    #ak pouzivame medoid, najdeme najblizsi bod k centroidu(medoid) sa stane centrom
    if medoid:
        min_distance = math.sqrt((points_x[0] - center_x) ** 2 + (points_y[0] - center_y) ** 2)
        min_point = 0
        for point in combined_points:
            distance = math.sqrt((points_x[point] - center_x) ** 2 + (points_y[point] - center_y) ** 2)
            if distance < min_distance:
                min_distance = distance
                min_point = point
        center_x = points_x[min_point]
        center_y = points_y[min_point]
    #vypocet suctu vzdialenosti od centra
    total_distance = 0
    for point in combined_points:
        total_distance += math.sqrt((points_x[point] - center_x) ** 2 + (points_y[point] - center_y) ** 2)
    #overenie podmienky
    return total_distance / num_points < 500

#funkcia na pridanie klastru b do klastru a
def add_cluster(a, b):
    global clusters
    clusters[a].extend(clusters[b])
    clusters[b] = []

#funkcia na vypocitanie suradnic centroidu
def calculate_centroid(a):
    global points_x, points_y, clusters
    sum_x, sum_y = 0,0
    num = len(clusters[a])
    for point_index in clusters[a]:
        sum_x += points_x[point_index]
        sum_y += points_y[point_index]
    return sum_x / num, sum_y / num

#funkcia na zistenie suradnic medoidu, hladam bod s najmensou vzdialenostou k centroidu
def find_medoid(x,y,cluster_id):
    global points_x,points_y,clusters
    min_distance = math.sqrt((points_x[0] - x) ** 2 + (points_y[0] - y) ** 2)
    min_point = 0
    for point in clusters[cluster_id]:
        distance = math.sqrt((points_x[point] - x) ** 2 + (points_y[point] - y) ** 2)
        if distance < min_distance:
            min_distance = distance
            min_point = point
    return points_x[min_point], points_y[min_point]

#funkcia sluziaca na aktualizovanie matice vzdialenosti a dat o klastroch
def update_distances(a, b):
    global distances, clusters, clusters_x, clusters_y, clusters_num
    #vypocet novych vzdialenosti klastrov od klastru a
    for i in range(clusters_num):
        distances[a][i] = math.sqrt((clusters_x[a] - clusters_x[i]) ** 2 + (clusters_y[a] - clusters_y[i]) ** 2)
        distances[i][a] = distances[a][i]
    #vymazanie informacii o klastri b pomocou jeho vymeny s poslednym platnym zaznamom
    clusters[b] = clusters[clusters_num - 1]
    clusters_x[b] = clusters_x[clusters_num - 1]
    clusters_y[b] = clusters_y[clusters_num - 1]
    distances[b] = distances[clusters_num - 1]
    for i in range(clusters_num - 1):
        distances[i][b] = distances[i][clusters_num - 1]
    clusters_num -= 1

#funkcia na spojenie dvoch klastrov
def merge():
    #najdenie najblizsich klastrov
    min_a, min_b = find_min()
    #kontrola porusenia podmienky
    if average(min_a, min_b):
        #pridanie clastru b do klastru a
        add_cluster(min_a, min_b)
        #vypocitanie centroidu
        center_x, center_y = calculate_centroid(min_a)
        #ak pouzivame medoid, najdeme najbizsi bod k centroidu(medoid) sa stane centrom
        if medoid:
            center_x, center_y = find_medoid(center_x, center_y, min_a)
        clusters_x[min_a] = center_x
        clusters_y[min_a] = center_y
        #aktulizovanie matice vzdialenosti a dat o klastroch
        update_distances(min_a, min_b)
        return True
    return False

#funkcia sluziaca na vykreslenie vyslednych klasterov
def draw():
    global clusters_num, clusters, points_x, points_y, clusters_x, clusters_y
    # rozmery platna
    x_min, x_max = -5000, 5000
    y_min, y_max = -5000, 5000
    traces = []

    #pre kazdy klaster si vytvorim nahodnu farbu
    colors = []
    for i in range(clusters_num):
        hue = i*10
        saturation = 70
        lightness = 50
        colors.append(f'hsl({hue}, {saturation}%, {lightness}%)')
    #vykreslenie bodov pre kazdy klaster
    for cluster_id in range(clusters_num):
        cluster_points_x = []
        for i in clusters[cluster_id]:
            cluster_points_x.append(points_x[i])
        cluster_points_y = []
        for i in clusters[cluster_id]:
            cluster_points_y.append(points_y[i])

        trace = go.Scatter(
            x=cluster_points_x,
            y=cluster_points_y,
            mode='markers',
            marker=dict(color=colors[cluster_id], size=3),
            showlegend=False
        )
        traces.append(trace)
        # vykreslenie centroidov/medoidov
    center_points_x = []
    for i in range(clusters_num):
        center_points_x.append(clusters_x[i])
    center_points_y = []
    for i in range(clusters_num):
        center_points_y.append(clusters_y[i])
    trace = go.Scatter(
        x=center_points_x,
        y=center_points_y,
        mode='markers',
        marker=dict(color='black', size=5),
        showlegend=False
    )
    traces.append(trace)
    #definovanie rozlozenia platna
    layout = go.Layout(
        xaxis=dict(range=[x_min, x_max], title="x"),
        yaxis=dict(range=[y_min, y_max], title="y"),
        title="Zadanie 2c"
    )
    fig = go.Figure(data=traces, layout=layout)
    fig.show()

############################################################################################

#funkcia na vytvorenie bodov
create_points()
#funkcia na vypocet pociatocnej matice vzdialenosti
calculate_initial_distances()
#klastrovaci proces az kym nie je porusena podmienka
while merge():
    if clusters_num % 100 == 0:
        print(clusters_num)
    continue
print("Konecny pocet klastrov je: ", clusters_num)
#vykreslenie vysledku
draw()

