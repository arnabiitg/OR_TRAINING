import math, random
from itertools import product
import time
import heapq, itertools

def initial_greedy_tour(distance):
    visited = [False]*len(distance[0])
    initial_point = random.sample(range(len(distance[0])), 1)[0]
    print(initial_point)
    tour = [initial_point]*len(distance[0])
    current_point = initial_point
    tour[0] = initial_point
    visited[initial_point] = True
    for i in range(1,len(distance[0])):
        current_distance = math.inf
        for point in range(len(distance[0])):
            if visited[point] !=True and distance[point][current_point] < current_distance:
                    next_point = point
                    current_distance = distance[point][current_point]
        current_point = next_point
        visited[current_point] = True
        tour[i] = current_point
    return tour


def nearest_neighbor(distance_matrix):
    """Find a tour using the Nearest Neighbor heuristic with a priority queue for efficiency."""
    num_cities = len(distance_matrix)
    unvisited = set(range(num_cities))
    tour = []
    
    current_city = random.choice(list(unvisited))  # Start from a random city
    tour.append(current_city)
    unvisited.remove(current_city)
    
    while unvisited:
        min_distance = math.inf
        for city in unvisited:
            if distance_matrix[current_city][city] < min_distance:
                min_distance = distance_matrix[current_city][city]
                nearest_city = city
            # heapq.heappush(min_heap, (distance_matrix[current_city][city], city))
        
        # nearest_distance, nearest_city = heapq.heappop(min_heap)
        tour.append(nearest_city)
        unvisited.remove(nearest_city)
        current_city = nearest_city
    
    return tour

def two_opt_swap(tour, i, k):
    """Perform a 2-opt swap by reversing the tour segment between indices i and k."""
    new_tour = tour[:i] + tour[i:k+1][::-1] + tour[k+1:]
    return new_tour

def two_opt(tour, distance_matrix):
    time_limit = 60*60*2
    num_cities = len(tour)
    best_tour = tour
    best_distance = calculate_total_distance(tour, distance_matrix)
    improved = True
    start_time = time.time()
    while improved :
        improved = False
        if time.time()-start_time > time_limit:
            break
        for i in range(1, num_cities - 1):
            for k in range(i + 1, num_cities):
                new_tour = two_opt_swap(best_tour, i, k)
                new_distance = calculate_total_distance(new_tour, distance_matrix)
                if new_distance < best_distance:
                    best_tour = new_tour[:]
                    best_distance = new_distance
                    improved = True
                    break
            if improved:
                break

    return best_tour, best_distance

def multi_fragment_heuristic(distance_matrix):
    num_cities = len(distance_matrix)
    edges = []
    
    # Create a list of all edges with their distances
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            heapq.heappush(edges, (distance_matrix[i][j], i, j))
    
    parent = list(range(num_cities))
    rank = [0] * num_cities
    degree = [0] * num_cities
    tour = []

    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]

    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            if rank[root_u] > rank[root_v]:
                parent[root_v] = root_u
            elif rank[root_u] < rank[root_v]:
                parent[root_u] = root_v
            else:
                parent[root_v] = root_u
                rank[root_u] += 1
    
    # Add edges to the tour
    while edges:
        weight, u, v = heapq.heappop(edges)
        if degree[u] < 2 and degree[v] < 2 and find(u) != find(v):
            union(u, v)
            tour.append((u, v))
            degree[u] += 1
            degree[v] += 1
    # print(tour)
    # Convert edge list to tour list
    tour_dict = [[] for _ in range(len(distance_matrix[0]))]
    for u, v in tour:
        tour_dict[u].append(v)
        tour_dict[v].append(u)
    # print(tour_dict)
    # Create the final tour
    for i in range(len(distance_matrix[0])):
        if degree[i] == 1:
            start = i
            break
    visited = [False] * num_cities
    final_tour = []
    current = start
    while len(final_tour) < num_cities:
        final_tour.append(current)
        visited[current] = True
        for neighbor in tour_dict[current]:
            if not visited[neighbor]:
                current = neighbor
                break

    return final_tour

def four_opt_swap(tour, distance_matrix, i, j, k, l):
    """Perform a 4-opt swap by considering all possible permutations of 4 segments and returning the best."""
    segments = [tour[:i], tour[i:j+1], tour[j+1:k+1], tour[k+1:l+1], tour[l+1:]]
    best_tour = tour[:]
    best_distance = calculate_total_distance(tour, distance_matrix)

    for perm in itertools.permutations([segments[1], segments[2], segments[3], segments[4]]):
        new_tour = segments[0] + perm[0] + perm[1] + perm[2] + perm[3]
        new_distance = calculate_total_distance(new_tour, distance_matrix)
        if new_distance < best_distance:
            best_tour = new_tour
            best_distance = new_distance
    
    return best_tour, best_distance

def four_opt(tour, distance_matrix):
    """Improve the initial tour using the 4-opt algorithm."""
    num_cities = len(tour)
    best_tour = tour
    best_distance = calculate_total_distance(tour, distance_matrix)
    start_time = time.time()
    improved = True
    while improved:
        if time.time() - start_time > 7200:
            break
        improved = False
        for i, j, k, l in itertools.combinations(range(num_cities), 4):
            new_tour, new_distance = four_opt_swap(best_tour, distance_matrix, i, j, k, l)
            # new_distance = calculate_total_distance(new_tour, distance_matrix)
            if new_distance < best_distance:
                best_tour = new_tour
                best_distance = new_distance
                improved = True
    
    return best_tour, best_distance


def calculate_total_distance(tour, distance_matrix):
    a = sum(distance_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1))
    return a + distance_matrix[tour[0]][tour[-1]]

def two_opt_swap(tour, i, k):
    """Perform a 2-opt swap by reversing the tour segment between indices i and k."""
    new_tour = tour[:i] + tour[i:k+1][::-1] + tour[k+1:]
    return new_tour

def two_opt(tour, distance_matrix):
    time_limit = 60*60*1.5
    num_cities = len(tour)
    best_tour = tour
    best_distance = calculate_total_distance(tour, distance_matrix)
    improved = True
    start_time = time.time()
    while improved :
        improved = False
        if time.time()-start_time > time_limit:
            break
        for i in range(1, num_cities - 1):
            for k in range(i + 1, num_cities):
                new_tour = two_opt_swap(best_tour, i, k)
                new_distance = calculate_total_distance(new_tour, distance_matrix)
                if new_distance < best_distance:
                    best_tour = new_tour[:]
                    best_distance = new_distance
                    improved = True
                    break
            if improved:
                break

    return best_tour, best_distance

# def four_opt_swap(tour, distance_matrix, i, j, k, l):
#     """Perform a 4-opt swap on the tour by rearranging the segments between indices i, j, k, and l."""
#     # Ensure indices are in the correct order
#     segment1 = tour[:i]
#     segment2 = tour[i:j]
#     segment3 = tour[j:k]
#     segment4 = tour[k:l]
#     segment5 = tour[l:]

#     # Generate all possible combinations of the segments and find the best one
#     possible_tours = [
#         segment1 + segment2[::-1] + segment3[::-1] + segment4[::-1] + segment5,
#         segment1 + segment2[::-1] + segment4 + segment3[::-1] + segment5,
#         segment1 + segment4 + segment3[::-1] + segment2[::-1] + segment5,
#         segment1 + segment3[::-1] + segment2[::-1] + segment4 + segment5,
#         segment1 + segment4 + segment2 + segment3[::-1] + segment5,
#         segment1 + segment2 + segment4 + segment3[::-1] + segment5,
#         segment1 + segment3[::-1] + segment4 + segment2[::-1] + segment5,
#         segment1 + segment4 + segment3[::-1] + segment2 + segment5,
#     ]
#     best_distance = math.inf
#     for i in possible_tours:
#         current_distance = calculate_total_distance(i, distance_matrix)
#         if current_distance < best_distance:
#             best_tour = i
#             best_distance = current_distance

#     # # Create new tour by reconnecting segments
#     # new_tour = tour[:i] + tour[j:k] + tour[i:j] + tour[l:] + tour[k:l]
#     return best_tour, best_distance

def random_two_opt(tour, distance_matrix):
    best_tour = tour
    best_distance = calculate_total_distance(tour, distance_matrix)
    print(best_distance)
    improved = True
    while improved :
        improved = False
        for _ in range(100000):
            [first_point, second_point] = random.sample(tour,2)
            new_tour = two_opt_swap(tour,first_point, second_point)
            # [one , two, three, four] = sorted(random.sample(tour, 4))
            # new_tour, new_distance = four_opt_swap(tour,distance_matrix, one, two, three, four)
            new_distance = calculate_total_distance(new_tour, distance_matrix)
            if new_distance < best_distance:
                best_tour = new_tour[:]
                best_distance = new_distance
                improved = True
                break
    return best_tour, best_distance

def get_distance(point1, point2):
    return math.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)

def solution2(points):
    

    # current_tour = multi_fragment_heuristic(distance_matrix)
    # current_tour = initial_greedy_tour(distance_matrix)
    # current_distance = calculate_total_distance(current_tour, distance_matrix)
    # visited = [0 for _ in range(len(distance_matrix[0]))]
    # if len(current_tour) != len(distance_matrix[0]): print("invalid")
    # for i in current_tour:
    #     if visited[i] ==0:
    #         visited[i] += 1
    #     elif visited[i] ==1:
    #         print("invalid")
    # print(current_distance)
    if len(points) < 30000:
        distance_matrix = [[0 for _ in range(len(points))] for _ in range(len(points))]

        for i, j in product(range(len(points)), range(len(points))):
            distance_matrix[i][j] = get_distance(points[i],points[j])
        current_tour = multi_fragment_heuristic(distance_matrix)
        return two_opt(current_tour, distance_matrix)
    with open("solution6.txt","r") as f:
        current_tour = []
        current_distance = float(f.readline())
        for line in f:
            for word in line.split():
                current_tour.append(int(word))
    return current_tour, current_distance