INF = float('inf')  

fare_matrix = [
    [0, 5000, INF, 7000, 6000, 3000, 4000],
    [5000, 0, 2000, 3000, 1000, INF, INF],
    [INF, 2000, 0, 1500, INF, 2500, INF],
    [7000, 3000, 1500, 0, 1200, 3500, 5000],
    [6000, 1000, INF, 1200, 0, INF, INF],
    [3000, INF, 2500, 3500, INF, 0, 2000],
    [4000, INF, INF, 5000, INF, 2000, 0]
]

def floyd_warshall(fare_matrix):
    n = len(fare_matrix)
    dist = [row[:] for row in fare_matrix]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

shortest_paths = floyd_warshall(fare_matrix)
print(shortest_paths[0][0])
def get_cheapest_fare(from_index, to_index):
    return shortest_paths[from_index][to_index]

print("Cheapest fare between Airport and Whitefield:", get_cheapest_fare(0, 2))

# def update_fare(from_index, to_index, new_fare):
#     if fare_matrix[from_index][to_index] != INF:
#         fare_matrix[from_index][to_index] = new_fare
#         fare_matrix[to_index][from_index] = new_fare  
#         return floyd_warshall(fare_matrix)

# shortest_paths = update_fare(0, 2, 2500)  
# print("Updated cheapest fare between Airport and Whitefield:", get_cheapest_fare(0, 2))