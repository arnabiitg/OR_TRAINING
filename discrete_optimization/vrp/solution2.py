import math

def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def not_interior(i, route_i):
    return (i == route_i[0] or i == route_i[-1]) 

def merge_routes(route1, route2, depot, capacity, customer_i, customer_j, customers):
    """
    Merge two routes by connecting customer_i and customer_j directly.
    Ensure the merged route does not exceed the capacity constraint.
    """
    # Determine if customer_i and customer_j are at the ends of their routes
    if customer_i == route1[-1]:
        route1_start = route1
    else:
        route1_start = route1[::-1]

    if customer_j == route2[0]:
        route2_end = route2
    else:
        route2_end = route2[::-1]

    # Merge the routes and check capacity
    merged_route = [depot.index] + route1_start + route2_end + [depot.index]
    merged_demand = sum(customers[nodes].demand for nodes in merged_route)
    
    return merged_route if merged_demand <= capacity else None


def clarke_wright_algo(customers, n_vehicles, capacity):

    depot = customers[0]
    # customers = customers[1:]
    n_customer = len(customers)

    # Calculate the Savings the dictionary
    savings = [] # (saving value, ith customer, jth customer)
    for i in range(1,len(customers)-1):
        for  j in range(i+1, len(customers)):
            value = (distance(depot, customers[i]) + 
                     distance(depot, customers[j]) - 
                     distance(customers[i], customers[j]))
            savings.append((value, i, j))

    # Sort the Savings
    savings.sort(reverse = True, key= lambda x: x[0])

    # Route Initialization
    routes = [[i] for i in range(1,n_customer)]
    merged = True
    # Route Merging 
    while merged:
        merged = False
        for saving in savings:
            s,i, j = saving

            route_i = None
            route_j = None

            for route in routes:
                if i in route and not_interior(i, route):
                    route_i = route
                if j in route and not_interior(j, route):
                    route_j = route

            if route_i and route_j and route_i != route_j:

                # Merge routes 
                merged_route = merge_routes(route_i, route_j, depot, capacity, i, j, customers)

                if merged_route:               
                    routes.remove(route_i)
                    routes.remove(route_j)
                    routes.append(merged_route)
                    merged_route.pop(0)
                    merged_route.pop(-1)
                    merged = True
                

    # Add depot to each route
    total_distance = 0
    for route in routes:
        complete_route = [depot.index] + route + [depot.index]
  
        for k in range(len(complete_route) - 1):
            total_distance += distance(customers[complete_route[k]], customers[complete_route[k+1]])
    if len(routes) <= n_vehicles:    
        return total_distance, routes
    return -1,routes