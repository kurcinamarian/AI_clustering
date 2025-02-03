import random
import plotly.graph_objs as go
import math
##########################################################################################

#Global variables and their initial initialization

#The number of initial points and the total number of points
first_num = int(input("Enter the number of initial points: "))
total_num = int(input("Enter the number of total points: "))

#Select the type of clustering
if input("Do you want to cluster using centroid or medoid?(c/m): ") == "m":
    medoid = True
else:
    medoid = False

#data about the coordinates of points
points_x = [0] * total_num
points_y = [0] * total_num

#number of clusters
clusters_num = total_num
#data about the elements in individual clusters
clusters = [[] for _ in range(total_num)]
#data about the coordinates of the cluster centers
clusters_x = [0] * total_num
clusters_y = [0] * total_num

#matrix of all cluster distances
distances = [[0.0] * total_num for _ in range(total_num)]

#########################################################################################################

#function to create points
def create_points():
    global points_x, points_y, clusters_x, clusters_y, clusters
    #Canvas dimensions
    x_min, x_max = -5000, 5000
    y_min, y_max = -5000, 5000
    #Initial point creation
    for i in range(first_num):
        x = random.randint(x_min, x_max)
        y = random.randint(y_min, y_max)
        while x in clusters_x and y in clusters_y:
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
        points_x[i] = x
        points_y[i] = y
    #Creation of the remaining points
    for i in range(first_num, total_num):
        #Select the parent of the new point
        point_parent = random.randint(0, i - 1)
        #Create the offset if the point is more than 100 units away from the edge
        if -4900 < points_x[point_parent] < 4900:
            x_offset = random.randint(-100, 100)
        #If the offset is not created, modify the offset accordingly
        elif points_x[point_parent] <= -4900:
            x_offset = random.randint(5000 + points_x[point_parent], 100)
        else:
            x_offset = random.randint(-100, 5000 - points_x[point_parent])

        #Creating an offset if the point is more than 100 units away from the edge
        if -4900 < points_y[point_parent] < 4900:
            y_offset = random.randint(-100, 100)
        #If not, create an adjusted offset
        elif points_y[point_parent] <= -4900:
            y_offset = random.randint(5000 + points_y[point_parent], 100)
        else:
            y_offset = random.randint(-100, 5000 - points_y[point_parent])

        #Creating a new point with an offset from the parent
        points_x[i] = points_x[point_parent] + x_offset
        points_y[i] = points_y[point_parent] + y_offset
    #Copying point data into cluster data, where each point is initially its own cluster
    clusters_x = points_x.copy()
    clusters_y = points_y.copy()
    for i in range(clusters_num):
        clusters[i].append(i)

#Function to calculate the initial distance matrix
def calculate_initial_distances():
    global distances, clusters_num, clusters_x, clusters_y
    for i in range(clusters_num):
        for j in range(i + 1, clusters_num):
            #Calculation of distance using the Pythagorean theorem
            distances[i][j] = math.sqrt((clusters_x[i] - clusters_x[j]) ** 2 + (clusters_y[i] - clusters_y[j]) ** 2)
            distances[j][i] = distances[i][j]

#Functions to find the nearest clusters
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

#Function to check the condition: the average distance of points from the center is not more than 500
def average(previous, adding):
    global points_x, points_y, clusters
    combined_points = clusters[previous] + clusters[adding]
    num_points = len(combined_points)

    #Calculation of the theoretical new centroid
    sum_x, sum_y = 0,0
    for point in combined_points:
        sum_x += points_x[point]
        sum_y += points_y[point]
    center_x = sum_x / num_points
    center_y = sum_y / num_points
    #When using the medoid, we find the closest point to the centroid (the medoid becomes the center)
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
    #Calculation of the sum of distances from the center
    total_distance = 0
    for point in combined_points:
        total_distance += math.sqrt((points_x[point] - center_x) ** 2 + (points_y[point] - center_y) ** 2)
    #Condition check
    return total_distance / num_points < 500

#Function to add cluster b to cluster a
def add_cluster(a, b):
    global clusters
    clusters[a].extend(clusters[b])
    clusters[b] = []

#Function to calculate the coordinates of the centroid
def calculate_centroid(a):
    global points_x, points_y, clusters
    sum_x, sum_y = 0,0
    num = len(clusters[a])
    for point_index in clusters[a]:
        sum_x += points_x[point_index]
        sum_y += points_y[point_index]
    return sum_x / num, sum_y / num

#Function to find the coordinates of the medoid, looking for the point with the smallest distance to the centroid
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

#Function used to update the distance matrix and cluster data
def update_distances(a, b):
    global distances, clusters, clusters_x, clusters_y, clusters_num
    #Calculation of new distances from cluster a to other clusters
    for i in range(clusters_num):
        distances[a][i] = math.sqrt((clusters_x[a] - clusters_x[i]) ** 2 + (clusters_y[a] - clusters_y[i]) ** 2)
        distances[i][a] = distances[a][i]
    #Deleting information about cluster b by swapping it with the last valid entry
    clusters[b] = clusters[clusters_num - 1]
    clusters_x[b] = clusters_x[clusters_num - 1]
    clusters_y[b] = clusters_y[clusters_num - 1]
    distances[b] = distances[clusters_num - 1]
    for i in range(clusters_num - 1):
        distances[i][b] = distances[i][clusters_num - 1]
    clusters_num -= 1

#Function to merge two clusters
def merge():
    #Finding the closest clusters
    min_a, min_b = find_min()
    #Condition violation check
    if average(min_a, min_b):
        #Adding cluster b to cluster a
        add_cluster(min_a, min_b)
        #Calculating the centroid
        center_x, center_y = calculate_centroid(min_a)
        #If using a medoid, find the closest point to the centroid (the medoid becomes the center)
        if medoid:
            center_x, center_y = find_medoid(center_x, center_y, min_a)
        clusters_x[min_a] = center_x
        clusters_y[min_a] = center_y
        #Updating the distance matrix and cluster data
        update_distances(min_a, min_b)
        return True
    return False

#Function used to plot the final clusters
def draw():
    global clusters_num, clusters, points_x, points_y, clusters_x, clusters_y
    #Canvas dimensions
    x_min, x_max = -5000, 5000
    y_min, y_max = -5000, 5000
    traces = []

    #Assigning a random color for each cluster
    colors = []
    for i in range(clusters_num):
        hue = i*10
        saturation = 70
        lightness = 50
        colors.append(f'hsl({hue}, {saturation}%, {lightness}%)')
    #Plotting points for each cluster
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
        #Plotting centroids/medoids
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
    #Defining the canvas layout
    layout = go.Layout(
        xaxis=dict(range=[x_min, x_max], title="x"),
        yaxis=dict(range=[y_min, y_max], title="y"),
        title="2c"
    )
    fig = go.Figure(data=traces, layout=layout)
    fig.show()

############################################################################################

#Function to generate points
create_points()
#Function to calculate the initial distance matrix
calculate_initial_distances()
#Clustering process until the condition is violated
while merge():
    if clusters_num % 100 == 0:
        print(clusters_num)
    continue
print("The final number of clusters is: ", clusters_num)
#Plotting the result
draw()

