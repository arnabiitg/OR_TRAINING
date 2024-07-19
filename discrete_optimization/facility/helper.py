import math
import random
import numpy as np
from ortools.linear_solver import pywraplp

class Facility:
    def __init__(self, id, cost, capacity, x, y):
        self.id = id
        self.cost = cost
        self.capacity = capacity
        self.available = capacity
        self.customers = set()
        self.x = x
        self.y = y

class Customer:
    def __init__(self, id, demand, x, y):
        self.id = id
        self.demand = demand
        self.facility = -1
        self.x = x
        self.y = y

def read_data(filename):
    with open(filename, 'r') as f:
        n_facility, n_customer = map(int, f.readline().split())

        facilities = []
        for id in range(n_facility):
            cost, capacity, x, y = map(float, f.readline().split())
            facilities.append(Facility(id, cost, int(capacity), x, y))

        customers = []
        for id in range(n_customer):
            demand, x, y = map(float, f.readline().split())
            customers.append(Customer(id, int(demand), x, y))

    return facilities, customers

def init_distance_matrix(customers, facilities):
    def distance(a, b):
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    distance_matrix = np.zeros((len(customers), len(facilities)))
    for i, customer in enumerate(customers):
        for j, facility in enumerate(facilities):
            distance_matrix[i][j] = distance(customer, facility)

    return distance_matrix

def init_feature(customers, facilities):
    feature = np.zeros((len(customers), len(facilities)))
    for i in range(len(customers)):
        for j in range(len(facilities)):
            feature[i][j] = facilities[j].cost
    return feature

def get_augmented_cost(facilities, distance_matrix, penalty, lambda_):
    augmented_cost = 0.0
    for facility in facilities:
        for customer in facility.customers:
            augmented_cost += distance_matrix[customer][facility.id] + lambda_ * penalty[customer][facility.id]
        if facility.customers:
            augmented_cost += facility.cost
    return augmented_cost

def init_lambda(customers, cost, alpha):
    return alpha * cost / len(customers)

def init_assignment(customers, facilities, distance_matrix):
    for customer in customers:
        min_distance = float('inf')
        min_facility = -1
        for facility in facilities:
            if min_distance > distance_matrix[customer.id][facility.id] and customer.demand <= facility.available:
                min_distance = distance_matrix[customer.id][facility.id]
                min_facility = facility.id
        facilities[min_facility].customers.add(customer.id)
        facilities[min_facility].available -= customer.demand
        customer.facility = min_facility

def get_cost(facilities, distance_matrix):
    cost = 0.0
    for facility in facilities:
        for customer in facility.customers:
            cost += distance_matrix[customer][facility.id]
        if facility.customers:
            cost += facility.cost
    return cost

def random_sample(n):
    return random.randint(0, n - 1)

def select_customer_to_move(customers, facilities, distance_matrix, penalty, lambda_):
    max_augmented_gain = -float('inf')
    max_customer = []
    max_facility = []
    for customer in customers:
        facility_old = facilities[customer.facility]
        for facility_new in facilities:
            if facility_new.id == facility_old.id:
                continue
            if facility_new.available < customer.demand:
                continue

            augmented_cost_old = distance_matrix[customer.id][facility_old.id] + lambda_ * penalty[customer.id][facility_old.id]
            if len(facility_old.customers) == 1:
                augmented_cost_old += facility_old.cost

            augmented_cost_new = distance_matrix[customer.id][facility_new.id] + lambda_ * penalty[customer.id][facility_new.id]
            if not facility_new.customers:
                augmented_cost_new += facility_new.cost

            augmented_gain = augmented_cost_old - augmented_cost_new

            if max_augmented_gain < augmented_gain:
                max_augmented_gain = augmented_gain
                max_customer = [customer.id]
                max_facility = [facility_new.id]
            elif max_augmented_gain == augmented_gain:
                max_customer.append(customer.id)
                max_facility.append(facility_new.id)

    if max_augmented_gain > 0.0:
        index = random_sample(len(max_customer))
        return max_augmented_gain, max_customer[index], customers[max_customer[index]].facility, max_facility[index]
    else:
        return 0.0, -1, -1, -1

def add_penalty(customers, penalty, feature, augmented_cost, lambda_):
    max_util = -float('inf')
    max_util_customer = []

    for customer in customers:
        facility = customer.facility
        util = feature[customer.id][facility] / (1 + penalty[customer.id][facility])

        if max_util < util:
            max_util = util
            max_util_customer = [customer.id]
        elif max_util == util:
            max_util_customer.append(customer.id)

    for customer_id in max_util_customer:
        facility = customers[customer_id].facility
        penalty[customer_id][facility] += 1
        augmented_cost += lambda_

def save_result(filename, customers, cost):
    with open(filename, 'w') as f:
        f.write(f"{cost} 0\n")
        f.write(' '.join(str(customer.facility) for customer in customers) + '\n')

def search(customers, facilities):
    alpha = 0.05
    distance_matrix = init_distance_matrix(customers, facilities)
    init_assignment(customers, facilities, distance_matrix)
    feature = init_feature(customers, facilities)
    cost = get_cost(facilities, distance_matrix)
    lambda_ = 0.0
    penalty = np.zeros((len(customers), len(facilities)), dtype=int)
    augmented_cost = get_augmented_cost(facilities, distance_matrix, penalty, lambda_)
    best_cost = cost
    best_customers = customers.copy()
    step_limit = 100000

    for step in range(step_limit):
        print(f"[Step {step + 1}/{step_limit}] [Cost {cost}] [Augmented Cost {augmented_cost}] [Best Cost {best_cost}]")

        augmented_cost_gain_by_customer_move, customer_id, facility_old_id, facility_new_id = select_customer_to_move(customers, facilities, distance_matrix, penalty, lambda_)

        if customer_id == -1:
            if lambda_ == 0.0:
                lambda_ = init_lambda(customers, cost, alpha)
            add_penalty(customers, penalty, feature, augmented_cost, lambda_)
        else:
            customer = customers[customer_id]
            facility_old = facilities[facility_old_id]
            facility_new = facilities[facility_new_id]

            cost_old = distance_matrix[customer.id][facility_old.id] + (len(facility_old.customers) == 1) * facility_old.cost
            cost_new = distance_matrix[customer.id][facility_new.id] + (not facility_new.customers) * facility_new.cost
            cost_gain = cost_old - cost_new
            augmented_cost_gain = augmented_cost_gain_by_customer_move

            cost -= cost_gain
            augmented_cost -= augmented_cost_gain

            facility_old.customers.remove(customer.id)
            facility_old.available += customer.demand
            facility_new.customers.add(customer.id)
            facility_new.available -= customer.demand
            customer.facility = facility_new.id

        if best_cost > cost:
            best_cost = cost
            best_customers = customers.copy()
            # save_result("python_output.txt", best_customers, best_cost)

        

def main(filename):
    facilities, customers = read_data(filename)
    search(customers, facilities)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <data-file>")
        print("Example: python main.py data/fl_25_2")
        sys.exit(-1)
    main(sys.argv[1])
