import math, heapq
from itertools import combinations

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

def calculate_length(routes, customers, depot):
    total_distance = 0
    for route in routes:
        complete_route = [depot.index] + route + [depot.index]
  
        for k in range(len(complete_route) - 1):
            total_distance += length(customers[complete_route[k]], customers[complete_route[k+1]])

    return total_distance


def get_init_solution(customers, n_vehicles, capacity):
    depot = customers[0]
    customers_sorted = sorted(customers[1:], key=lambda customer: length(depot, customer))
    routes = [[] for _ in range(n_vehicles)]
    capacity_remaining = [capacity for _ in range(n_vehicles)]
    
    for customer in customers_sorted:
        for i in range(n_vehicles):
            if capacity_remaining[i] >= customer.demand:
                if not routes[i]:  # If route is empty, add customer at the beginning
                    routes[i].append(customer.index)
                elif len(routes[i]) == 1:
                    routes[i].append(customer.index)
                else:
                    # Compare distances to decide whether to add at the beginning or end
                    if length(customer, customers[routes[i][0]]) < length(customer, customers[routes[i][-1]]):
                        routes[i].insert(1, customer.index)
                    else:
                        routes[i].insert(-2,customer.index)
                capacity_remaining[i] -= customer.demand
                break

    return routes


def two_opt_swap(routes, customers, capacity):
    def calculate_demand(route):
        return sum(customers[node].demand for node in route)
    
    best_routes = routes[:]
    best_distance = calculate_length(routes, customers, customers[0])
    improved = True

    while improved:
        improved = False
        for route_1, route_2 in combinations(range(len(routes)), 2):
            for i in range(1, len(routes[route_1]) - 1):
                for j in range(1, len(routes[route_2])-1):
                    new_route_1 = routes[route_1][:i] + [routes[route_2][j]] + routes[route_1][i+1:]
                    new_route_2 = routes[route_2][:j] + [routes[route_1][i]] + routes[route_2][j+1:]
                    # print(routes[route_1])
                    # print('*'*100)
                    # print(new_route_1)

                    if calculate_demand(new_route_1) <= capacity and calculate_demand(new_route_2) <= capacity:
                        new_routes = best_routes[:]
                        new_routes[route_1] = new_route_1
                        new_routes[route_2] = new_route_2
                        new_distance = calculate_length(new_routes, customers, customers[0])

                        if new_distance < best_distance:
                            best_routes = new_routes[:]
                            best_distance = new_distance
                            improved = True
                        routes = best_routes[:]
    return routes



def two_opt_exchange(routes, customers, capacity):
    def calculate_demand(route, customers):
        return sum(customers[node].demand for node in route)
    def swap_segments(route1, route2, i, j, k, l):
        new_route_1 = route1[:i] + route2[k:l+1] + route1[j+1:]
        new_route_2 = route2[:k] + route1[i:j+1] + route2[l+1:]
        return new_route_1, new_route_2

    best_routes = routes[:]
    best_distance = calculate_length(routes, customers, customers[0])
    improved = True

    while improved:
        improved = False
        for route_1, route_2 in combinations(range(len(routes)), 2):
            for i in range(1, len(routes[route_1]) - 1):
                for j in range(i, len(routes[route_1])):
                    for k in range(1, len(routes[route_2]) - 1):
                        for l in range(k, len(routes[route_2])):
                            new_route_1, new_route_2 = swap_segments(routes[route_1], routes[route_2], i, j, k, l)

                            if calculate_demand(new_route_1, customers) <= capacity and calculate_demand(new_route_2, customers) <= capacity:
                                new_routes = best_routes[:]
                                new_routes[route_1] = new_route_1
                                new_routes[route_2] = new_route_2
                                new_distance = calculate_length(new_routes, customers, customers[0])

                                if new_distance < best_distance:
                                    best_routes = new_routes[:]
                                    best_distance = new_distance
                                    improved = True
                                routes = best_routes[:]
        # print(best_distance)

    return routes


def multi_fragment_heuristic(init_solution, customers):
    # print(customers)
    new_routes = []
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
        # print(final_tour)
        new_routes.append(final_tour)
    
    return new_routes

def main(customers, n_vehicles, capacity):
    # Initialize routes
    init_routes = get_init_solution(customers, n_vehicles, capacity)
    # print(init_routes)

    # Apply 2-opt exchange to improve initial solution
    if len(customers) == 51:
        init_routes = two_opt_exchange(init_routes, customers, capacity)
    # print(init_routes)
    
    # Calculate initial length
    init_length = calculate_length(init_routes, customers, customers[0])
    
    # Apply multi-fragment heuristic
    for route in init_routes:
        route.insert(0, 0)  # Insert depot index at the beginning
    routes = multi_fragment_heuristic(init_routes, customers)
    for route in routes:
        route.remove(0)  # Remove depot index after heuristic
    
    # routes = two_opt_swap(routes, customers, capacity)
    
    # Calculate new length after heuristic
    new_length = calculate_length(routes, customers, customers[0])
    
    # Determine which solution is better
    if new_length < init_length:
        return new_length, routes
    return init_length, init_routes

