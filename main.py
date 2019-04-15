
import time
import numpy as np
import matplotlib.pyplot as plt

# GLOBALS #
distance_matrix = np.zeros(0)
medoid_list = []
min_sum_row = []
medoids = []
tic = 0
# GLOBALS #

# calc distance between points , return vector of distances
def calc_mannhatan_distance(point,data):
    to_ret = []
    for i in range(len(data)):
        to_ret.append(np.abs(point[0]-data[i][0])+np.abs(point[1]-data[i][1]))
    return to_ret

# input : vector ,output : distance matrix
def get_distance_matrix(vector_data):
    mat_vec = []
    for i in range(len(vector_data)):
        mat_vec.append(calc_mannhatan_distance(vector_data[i], vector_data))
    matrix = np.array(mat_vec)
    return matrix

# input : num of medoids, output: list of medoids
def build_step(vector_data):
    global distance_matrix
    global medoid_list
    distance_matrix = get_distance_matrix(vector_data).tolist()
    #distance_matrix = [[0,8,8,7,7],[8,0,0.5,4,4],[8,0.5,0,4,3],[7,4,4,0,1],[7,4,3,1,0]]
    sum_list = calc_min_distnace(distance_matrix)
    medoid_list.append(distance_matrix[sum_list.index(np.min(sum_list))])

# input : distance matrix, output : list of sums for rows
def calc_min_distnace(dist_matrix):
    sum_list = []
    for i in range(len(dist_matrix)):
        sum_list.append(np.sum(dist_matrix[i]))
    return sum_list

# input : int k, output : update medoid list according to k
def find_next_medoid(k):
    global medoid_list
    min_row = []
    sum = 0
    index = get_index_by_vector(medoid_list[0])
    temp_matrix = np.delete(distance_matrix,index,0).tolist()
    for row in temp_matrix:
        for j in range(len(row)):
            sum += min(row[j],medoid_list[0][j])
        min_row.append(sum)
        sum = 0
    for i in range(1,k):
        min_of_min = np.min(min_row)
        min_sum_row.append(min_of_min)
        medoid_index = min_row.index(min_of_min)
        medoid_vector = temp_matrix[medoid_index]
        distance_matrix_index = get_index_by_vector(medoid_vector)
        medoid_list.append(list(distance_matrix[distance_matrix_index]))
        temp_matrix = np.delete(temp_matrix, medoid_index, 0).tolist()
        min_row.pop(medoid_index)

# input : vector in distance_matrix, output : vector index in distance matrix
def get_index_by_vector(my_vect):
    temp_matrix = distance_matrix
    index = temp_matrix.index(my_vect)
    return index

# input: reference medoid to compare with, output : True if there was a swap in medoid list, false otherwise
def swap_step(chosen_medoid):
    res = False
    min_to_swap = min_sum_row[0]
    index_list = []
    for idx,val in enumerate(medoid_list):
        index_list.append(get_index_by_vector(medoid_list[idx]))
    temp_matrix = []
    for i in range(len(distance_matrix)):
        if i not in index_list:
            temp_matrix.append(distance_matrix[i])
    sum = 0
    local_min_row = []
    for row in temp_matrix:
        for j in range(len(row)):
            sum += min(row[j],chosen_medoid[j])
        local_min_row.append(sum)
        sum = 0
    if min_to_swap > np.min(local_min_row):
        chosen_index = local_min_row.index(np.min(local_min_row))
        new_vector = temp_matrix[chosen_index]
        medoid_list.pop(0)
        medoid_list.append(new_vector)
        min_sum_row.pop(0)
        min_sum_row.append(np.min(local_min_row))
        res = True
    else:
        min_sum_row.pop(0)
    return res

# plot points
def ShowPlot(clusters):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'peru']
    j=0
    for cluster in clusters:
        i = 0
        for point in cluster:
            if i==0:
                plt.scatter(point[0], point[1], color=colors[j],marker='*')
            else:
                plt.scatter(point[0], point[1], color=colors[j])
            i += 1
        j +=1
    plt.show()

# input : none, output : list of clusters
def createClusters():
    cluster_list = []
    for val in medoid_list:
        index_to_add = val.index(0.0)
        cluster_list.append([list(vector_data[index_to_add])])
    cluster_list = pointTocluster(cluster_list)
    return cluster_list

# input : cluster list, output : list of points in cluster
def pointTocluster(cluster_list):
    for val in vector_data:
        min_list = []
        for num in cluster_list:
            min_list.append(np.abs(num[0][0] - val[0]) + np.abs(num[0][1] - val[1]))
        local_min = np.min(min_list)
        if local_min == 0:
            continue
        local_min_index = min_list.index(local_min)
        cluster_list[local_min_index].append(list(val))
    return cluster_list

# set medoid list for printing
def setMedoids():
    for i in range(len(cluster_list)-1):
        medoids.append(cluster_list[i][0])

def getRandPoints(numberOfPoints):
    data_list = []
    for i in range(numberOfPoints):
        x = int(np.random.uniform(low=0, high=20))
        y = int(np.random.uniform(low=0, high=20))
        data_list.append([x,y])
    return data_list

def initDataByUser():
    list_data = []
    while True:
        userAns = int(raw_input('Enter 0 for random points, 1 for manual:'))
        if userAns == 1 or userAns == 0:
            break
        else:
            print 'Enter only 1 or 0 - try again'
    global tic
    if userAns == 0:
        numberOfPoints = int(raw_input('Enter desired number of points: '))
        tic = time.time()
        vector_data = np.asarray(getRandPoints(numberOfPoints), dtype=np.float)
    else:
        numberOfPoints = int(raw_input('Enter desired number of points: '))
        'Enter points using only space, for example 1 2'
        for i in range(numberOfPoints):
            point = list(raw_input("Enter two numbers here: ").split())
            list_data.append(point)
        vector_data = np.asarray(list_data, dtype=np.float)
    k = int(raw_input("Enter number of desired medoids : "))
    return vector_data,k


if __name__== "__main__":
    # create points
    #vector_data = np.array([(7,6),(2,6),(3,8),(8,5),(7,4),(4,7),(6,2),(7,3),(6,4),(3,4)],dtype=np.float)
    vector_data, k = initDataByUser()
    build_step(vector_data)
    find_next_medoid(k)
    i = 1
    if k != 1:
        while True:
            chosen_medoid = medoid_list[i]      # The reference medoid to compare with
            res = swap_step(chosen_medoid)      # After swap step check if there is a change
            if len(min_sum_row) == 0:           # No more swaps
                break
            if res == True:                     # There was a swap
                continue
            elif res == False and i == k-1:
                break
            else:
                i +=1
        ### Build clusters and Medoids ###
        cluster_list = createClusters()
        setMedoids()
        ### Build clusters and Medoids ###
        i = 1
        for val in cluster_list:
            print ('Cluster %d ' %i+str((val)))
            i += 1
    else:
        cluster_list = createClusters()
    #print ('Time elapsed : ' + str(time.time() - tic))
    ShowPlot(cluster_list)