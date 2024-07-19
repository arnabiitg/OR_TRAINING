import math, random
from itertools import product
import time
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


def calculate_total_distance(tour, distance_matrix):
    return sum(distance_matrix[tour[i]][tour[i+1]] for i in range(len(tour)-1))

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


# Generate a neighboring tour by swapping two cities
def generate_neighbor(tour):
    """Returns neighbor of  your solution."""
    
    neighbor = tour[:]
        
    
    # func = random.choice([0,1,2,3])
    func = 2
    if func == 0:
        inverse(neighbor)
        
    elif func == 1:
        insert(neighbor)
        
    elif func == 2 :
        swap(neighbor)
    
    else:
        swap_routes(neighbor)
        
    return neighbor 

def inverse(state):
    "Inverses the order of cities in a route between node one and node two"
   
    node_one = random.choice(state)
    new_list = list(filter(lambda city: city != node_one, state)) #route without the selected node one
    node_two = random.choice(new_list)
    state[min(node_one,node_two):max(node_one,node_two)] = state[min(node_one,node_two):max(node_one,node_two)][::-1]
    
    return state

def insert(state):
    "Insert city at node j before node i"
    node_j = random.choice(state)
    state.remove(node_j)
    node_i = random.choice(state)
    index = state.index(node_i)
    state.insert(index, node_j)
    
    return state

def swap(state):
    "Swap cities at positions i and j with each other"
    pos_one = random.choice(range(len(state)))
    pos_two = random.choice(range(len(state)))
    state[pos_one], state[pos_two] = state[pos_two], state[pos_one]
    
    return state

def swap_routes(state):
    "Select a subroute from a to b and insert it at another position in the route"
    subroute_a = random.choice(range(len(state)))
    subroute_b = random.choice(range(len(state)))
    subroute = state[min(subroute_a,subroute_b):max(subroute_a, subroute_b)]
    del state[min(subroute_a,subroute_b):max(subroute_a, subroute_b)]
    insert_pos = random.choice(range(len(state)))
    for i in subroute:
        state.insert(insert_pos, i)
    return state

def get_distance(point1, point2):
    return math.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2)


def simulated_annealing(points, initial_temperature, tolerance, cooling_rate):
    distance_matrix = [[0 for _ in range(len(points))] for _ in range(len(points))]

    for i, j in product(range(len(points)), range(len(points))):
        distance_matrix[i][j] = get_distance(points[i],points[j])

    # print(distance_matrix)
    num_cities = len(distance_matrix)
    # current_tour = generate_initial_tour(num_cities)
    current_tour = initial_greedy_tour(distance_matrix)
    # print(current_tour)
    current_distance = calculate_total_distance(current_tour, distance_matrix)
    print(current_distance)
    best_tour = current_tour[:]
    best_distance = current_distance

    # best_tour, best_distance = two_opt(best_tour,distance_matrix)

    # return best_tour, best_distance

    
    temperature = initial_temperature
    same_solution = 0

    for _ in range(100000):
        neighbor_tour = generate_neighbor(current_tour)
        neighbor_distance = calculate_total_distance(neighbor_tour, distance_matrix)

        # Calculate the acceptance probability
        if neighbor_distance < current_distance:
            acceptance_probability = 1.0
        else:
            acceptance_probability = math.exp((current_distance - neighbor_distance) / temperature)
        
        # Accept the new solution with a certain probability
        if acceptance_probability > random.random():
            current_tour = neighbor_tour
            current_distance = neighbor_distance
            
            # Update the best solution found
            if current_distance < best_distance:
                best_tour = current_tour[:]
                best_distance = current_distance
                # same_solution = 0
            # else:
            #     same_solution += 1
        # else:
        #     same_solution += 1
                
        # if (current_distance - best_distance)/best_distance >= 0.80:
        #     same_solution = 0
        # else:
        #     same_solution += 1

        # Decrease the temperature
        temperature *= cooling_rate
        
        # best_tour, best_distance = two_opt(best_tour,distance_matrix)

    return best_tour, best_distance
