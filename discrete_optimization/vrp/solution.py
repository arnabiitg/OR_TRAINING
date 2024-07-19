import math, heapq
from itertools import product

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def get_init_solution(customers, n_vehicles, capacity):
    # sort the customers by their demand 
    depot = customers[0]
    customers = sorted(customers, key=lambda customer: length(customer,depot))

    # customers = customers[1:]
    init_solution = [[0]]
    current_demand = 0
    index = 0
    for customer in customers[1:]:
        if current_demand +  customer.demand<= capacity:
            init_solution[-1].append(customer.index)
        else:
            init_solution.append([0])
            init_solution[-1].append(customer.index)
            current_demand = 0
        current_demand += customer.demand
    print(init_solution)
    return multi_fragment_heuristic(init_solution, customers)

# def get_distance_matrix(customers, tour):
#     distance_matrix = [[0 for _ in range(len(tour))] for _ in range(len(tour))]

#     for i, j in product(tour, tour):
#         distance_matrix[i][j] = length(customers[i],customers[j])
#         # distance_matrix[j][i] = distance_matrix[i][j] 
#     return distance_matrix

def multi_fragment_heuristic(init_solution, customers):
    # print(customers)
    for k, tour in enumerate(init_solution):
        edges = []
        
        # Create a list of all edges with their distances
        for index, i in enumerate(tour[:-1]):
            for j in tour[index+1:]:
                # print(i,j)
                heapq.heappush(edges, (length(customers[i], customers[j]), i, j))
        
        parent = {i: i for i in tour}  # Corrected initialization
        rank = {i: 0  for i in tour}
        degree = {i: 0  for i in tour}
        tour_edges = []

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
                tour_edges.append((u, v))
                degree[u] += 1
                degree[v] += 1
        
        # Convert edge list to tour list
        tour_dict = {i:[] for i in tour}
        for u, v in tour_edges:
            tour_dict[u].append(v)
            tour_dict[v].append(u)
        
        # Create the final tour
        start = None
        for node, deg in degree.items():
            if deg == 1:
                start = node
                break
        
        if start is None:
            print(f"Tour {k}: No starting point found. Degree: {degree}")
            print(f"Tour edges: {tour_edges}")
            raise Exception("No starting point found for the tour")
        # print(tour_dict)
        visited = set()
        final_tour = []
        current = start
        
        while len(final_tour) < len(tour):
            final_tour.append(current)
            visited.add(current)
            for neighbor in tour_dict[current]:
                if neighbor not in visited:
                    current = neighbor
                    break
        print(final_tour)
        init_solution[k] = final_tour
    
    return init_solution

def solution(customers, n_vehicles, capacity):
    # print(customers)
    depot = customers[0]
    vehicle_tours =  get_init_solution(customers,n_vehicles,capacity)
    obj = 0
    for v in range(0, len(vehicle_tours)):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot,customers[vehicle_tour[0]])
            for i in range(0, len(vehicle_tour)-1):
                obj += length(customers[vehicle_tour[i]],customers[vehicle_tour[i+1]])
            obj += length(customers[vehicle_tour[-1]],depot)


    return obj, vehicle_tours