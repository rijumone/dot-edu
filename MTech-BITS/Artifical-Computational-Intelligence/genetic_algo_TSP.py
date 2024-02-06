import numpy as np
import random

# Define the distance matrix between blood banks (example)
distances = [
    [0, 10, 15, 20],
    [10, 0, -1, 25],
    [15, -1, 0, 30],
    [20, 25, 30, 0]
]

# Parameters for genetic algorithm
population_size = 50
num_generations = 1000
mutation_rate = 0.1

# Fixed ending blood bank (assumed to be the hospital)
ending_bloodbank = 0

# Generate initial population
def generate_population(population_size, starting_bloodbank, ending_bloodbank, reachable_bloodbanks):
    population = []
    for _ in range(population_size):
        individual = list(range(len(reachable_bloodbanks)))
        individual.remove(starting_bloodbank)
        random.shuffle(individual)
        individual.insert(0, starting_bloodbank)
        individual.append(ending_bloodbank)  # Ensure the tour ends at the ending blood bank
        population.append(individual)
    return population

# Calculate total distance of a tour
def calculate_total_distance(tour, distances, ending_bloodbank):
    total_distance = 0
    for i in range(len(tour) - 1):
        if distances[tour[i]][tour[i + 1]] == -1:
            # Unreachable blood bank encountered
            return float('inf')  # Return infinity as the distance
        total_distance += distances[tour[i]][tour[i + 1]]
    # Add distance from last blood bank to ending blood bank
    total_distance += distances[tour[-1]][ending_bloodbank]
    return total_distance

# Selection: Roulette wheel selection
def selection(population, distances):
    fitness_scores = [1 / calculate_total_distance(individual, distances, ending_bloodbank) for individual in population]
    total_fitness = sum(fitness_scores)
    probabilities = [score / total_fitness for score in fitness_scores]
    selected_indices = np.random.choice(len(population), size=population_size, replace=True, p=probabilities)
    return [population[i] for i in selected_indices]

# Crossover: Order crossover (OX1)
def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(1, len(parent1)), 2))
    child1 = [-1] * len(parent1)
    child2 = [-1] * len(parent1)
    for i in range(start, end + 1):
        child1[i] = parent1[i]
        child2[i] = parent2[i]
    idx1, idx2 = 0, 0
    for i in range(len(parent1)):
        if idx1 == start:
            idx1 = end + 1
        if idx2 == start:
            idx2 = end + 1
        if parent2[i] not in child1:
            child1[idx1] = parent2[i]
            idx1 = (idx1 + 1) % len(parent1)
        if parent1[i] not in child2:
            print(child2, idx2)
            child2[idx2] = parent1[i]
            idx2 = (idx2 + 1) % len(parent1)
    return child1, child2

# Mutation: Swap mutation
def mutation(individual):
    if random.random() < mutation_rate:
        idx1, idx2 = sorted(random.sample(range(1, len(individual)), 2))
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# Genetic algorithm
def genetic_algorithm(distances, starting_bloodbank, ending_bloodbank):
    population = generate_population(population_size, starting_bloodbank, ending_bloodbank, range(len(distances)))
    for generation in range(num_generations):
        population = sorted(population, key=lambda x: calculate_total_distance(x, distances, ending_bloodbank))
        selected_population = selection(population, distances)
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutation(child1)
            child2 = mutation(child2)
            new_population.extend([child1, child2])
        population = new_population
    best_tour = min(population, key=lambda x: calculate_total_distance(x, distances, ending_bloodbank))
    return best_tour, calculate_total_distance(best_tour, distances, ending_bloodbank)

# Main function
if __name__ == "__main__":
    starting_bloodbank = int(input("Enter the starting blood bank (index): "))
    best_tour, total_distance = genetic_algorithm(distances, starting_bloodbank, ending_bloodbank)
    print("Best tour:", best_tour)
    print("Total distance:", total_distance)
