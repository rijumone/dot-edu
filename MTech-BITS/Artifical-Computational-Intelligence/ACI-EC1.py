#!/usr/bin/env python
# coding: utf-8

# In[109]:


distances = [
    [0, 5, 8, float('inf'), float('inf'), float('inf'), float('inf')],
    [5, 0, 7, 6, 10, float('inf'), 8],
    [8, 7, 0, float('inf'), float('inf'), 12, float('inf')],
    [float('inf'), 6, float('inf'), 0, float('inf'), float('inf'), 10],
    [float('inf'), 10, float('inf'), float('inf'), 0, 9, 18],
    [float('inf'), float('inf'), 12, float('inf'), 9, 0, float('inf')],
    [float('inf'), 8, float('inf'), 10, 18, float('inf'), 0],
]


# In[110]:


### shortest distance between two nodes
import heapq

def dijkstra(adj_matrix, start, end):
    num_nodes = len(adj_matrix)
    priority_queue = [(0, start)]
    distances = [float('infinity')] * num_nodes
    distances[start] = 0

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # If the current distance is greater than the known distance, skip
        if current_distance > distances[current_vertex]:
            continue

        # Explore neighbors
        for neighbor, weight in enumerate(adj_matrix[current_vertex]):
            if weight < float('infinity'):
                distance = current_distance + weight

                # If the new distance is shorter, update the distance and push it to the priority queue
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    return distances[end]



# In[111]:


import math

def calculate_average_distance(next_node, unvisited_blood_banks, distances):
    total_distance = 0
    for unvisited_bank in unvisited_blood_banks:
        if unvisited_bank !=6:
            total_distance += dijkstra(distances, next_node, unvisited_bank)
    return total_distance / len(unvisited_blood_banks)-1

def blood_supply_recursive_bfs_a_star(current_node, unvisited_blood_banks, distances, path, total_distance):
    
    if not unvisited_blood_banks:
        # If all blood banks are visited, return to the hospital
        return path + [current_node], total_distance + distances[current_node][6]  # Assuming 0 represents the hospital
    #print('current_node' , current_node , 'unvisited_blood_banks', unvisited_blood_banks, path , total_distance)
    
    
    sorted_unvisited_blood_banks = []
    for next_node in unvisited_blood_banks:
        path_heuristics = distances[current_node][next_node] + calculate_average_distance(next_node, unvisited_blood_banks, distances)
        if distances[current_node][next_node] != 0 and path_heuristics != float('inf') and current_node != next_node:
            sorted_unvisited_blood_banks.append([next_node, path_heuristics])
    sorted_unvisited_blood_banks = sorted(sorted_unvisited_blood_banks, key=lambda x: x[1])
    #print(current_node, sorted_unvisited_blood_banks)   
    sorted_unvisited_blood_banks = [item[0] for item in sorted_unvisited_blood_banks]

    #print('***********')
 
    best_path = []
    best_total_distance = float('inf')
    
    for next_bank in sorted_unvisited_blood_banks:
        
        new_path = path + [current_node]
        new_total_distance = total_distance + distances[current_node][next_bank]

        new_unvisited_blood_banks = set(unvisited_blood_banks)
        new_unvisited_blood_banks.remove(next_bank)

        # Recursively explore the next blood bank
        result_path, result_total_distance = blood_supply_recursive_bfs_a_star(next_bank, new_unvisited_blood_banks, distances, new_path, new_total_distance)
        if result_total_distance < best_total_distance:
                best_path = result_path
                best_total_distance = result_total_distance

    return best_path, best_total_distance

def blood_supply_a_star(distances, starting_node):
    n = len(distances)
    unvisited_blood_banks = set(range(0, n))  # Assuming 6 is the hospital
    #starting_node = 5  # Starting from the A
    unvisited_blood_banks.remove(starting_node)
    path, total_distance = blood_supply_recursive_bfs_a_star(starting_node, unvisited_blood_banks, distances, [], 0)

    # Return to the hospital to complete the delivery
    if len(path)>0 and len(set(path)) == len(path) and path[-1]==6: 
        return path , total_distance
    else:
        return 'Not Possible', 'Not Possible' 

# Example Usage
'''
distances = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
'''
for i in range(0,6):
    optimal_path, optimal_distance = blood_supply_a_star(distances,i)
    print("starting point" ,i)
    print("Optimal Blood Supply Path:", optimal_path)
    print("Optimal Blood Supply Distance:", optimal_distance)
    print('******************')


# In[ ]:




