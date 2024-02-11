"""
This code implements a genetic algorithm to solve the travelling salesman problem for a given graph. The algorithm works as follows:

*First, a population of random genomes is initialized, where each genome is a random path in the graph.
*Then, the fitness of each genome is calculated as the total distance travelled on the path.
*The genetic algorithm is then applied to the population for a number of generations.
*In each generation, the fittest individuals are selected using tournament selection.
*Then, crossover is applied to the selected individuals to create new offspring.
*Finally, mutation is applied to the offspring with a given mutation rate.
*The new offspring replace the weakest individuals in the population.
*This process is repeated for a number of generations until a stopping criterion is reached 
 (in this case, a maximum number of generations is defined).
*The fittest individual in the final population is returned as the solution to the travelling salesman problem.
The code defines several functions to implement the genetic algorithm, including:
*fitness(): a function to calculate the fitness of a given genome (i.e. the total distance travelled on the path).
*select_population(): a function to select a random sample of individuals from a given population.
*tournament_selection(): a function to select the fittest individuals from a given population using tournament selection.
*ordered_crossover(): a function to apply ordered crossover to two parent genomes and generate new offspring.
*mutation(): a function to apply mutation to a given genome.
*total_population_score(): a function to calculate the total score of a given population 
 (i.e. the sum of all the fitness scores of the individuals in the population).
*generate_path(): a function to generate a random path in the graph.
*initialize_population(): a function to initialize a random population of given size.
"""


import random
# from math import inf
from dataclasses import dataclass
# from loguru import logger



max = 1000
START_CITY = 'A'
END_CITY = 'H'


# Initialize Parameters.

population_size = 9
maximum_generations = 99
mutation_rate = 1
selection_pressure = 5
convergence_rate = 0.9
threshhold = population_size * max * convergence_rate
# import pdb;pdb.set_trace()


# Initialize Graph.

total_cities = 7

cities = "ABCDEFH"

position = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "H": 6,
}

graph = [
    #   A,  B,   C,  D,   E,   F,   H
    [   0,  5,   8,  max, max, max, max, ],    # A
    [   5,  0,   7,  6,   10,  max, 8,   ],    # B 
    [   8,  7,   0,  max, max, 12,  max, ],    # C
    [ max,  6, max,  0,   max, max, 10,  ],    # D
    [ max, 10, max,  max, 0,   9,   18   ],    # E
    [ max, max, 12,  max, 9,   0,   max  ],    # F
    [ max,  8, max,  10,  18,  max, 0    ],    # H
]


# Define genome class.
# Includes the path taken and fitness.
# Fitness is calculated the total distance travelled on a given path .

@dataclass
class Genome:
    path: str
    fitness: str

# Define fitness function.

def fitness(path):
    """Calculates fitness by adding the distance between all the neigbouring cities in the path,
    and return the total distance traversed in a given path."""

    total_distance = 0
    for i in range(len(path)-1):
        # if there is no path between the two cities return max, else add it to the total distance travelled.
        try:
            if graph[position[path[i]]][position[path[i+1]]] == max:
                return max
        except KeyError:
            import pdb;pdb.set_trace()
        total_distance += graph[position[path[i]]][position[path[i+1]]]
    return total_distance


def select_population(population, number):
    """Function to return a random sample of genomes from a given population."""

    selected = []
    while (len(selected) < number):
        value = random.randint(0, len(population)-1)
        if population[value] not in selected:
            selected.append(population[value])
    return selected


def tournament_selection(population, number):
    """Return a certain number of fittest individuals in a given population."""

    population.sort(key=lambda x: x.fitness)
    fittest = population[0:number]
    return fittest


def ordered_crossover(parent_1, parent_2, crossover_start, crossover_end):
    """Apply ordered cross (OX) on a genome and return the newly generated genome.
    Pairs of selected individuals (parents) are combined to produce offspring through crossover or
    recombination. This involves exchanging genetic material (e.g., sub-tours in the TSP) between parents to
    create new solutions. The crossover operator helps explore the solution space by combining beneficial
    traits from different individuals."""
    
    # Initialize the child with the same length as parents
    p1_path = list(parent_1.path[0:len(parent_1.path)])
    p2_path = list(parent_2.path[0:len(parent_2.path)])
    child = [START_CITY] + ([-1] * (len(p1_path)-2)) + [END_CITY]

    # Copy a subset of genes from parent_1 to the child
    child[crossover_start:crossover_end + 1] = p1_path[crossover_start:crossover_end + 1]
    # logger.debug(child)
    # Fill in the remaining positions in the child with genes from parent_2
    idx_child = 1
    for idx_parent in range(1, len(p2_path)-1):
        if idx_parent < crossover_start or idx_parent > crossover_end:
            # If the gene from parent_2 is not already in the child, add it
            if p2_path[idx_parent] not in child:
                # Find the next empty position in the child
                while child[idx_child] != -1:
                    idx_child += 1
                # Assign the gene from parent_2 to the child
                child[idx_child] = p2_path[idx_parent]
    # print(child)
    # import pdb;pdb.set_trace()
    return Genome(child, fitness(child))


def mutation(chromosome):
    """Apply mutation by replacing a random order of cities and return the newly generated genome."""

    # import pdb;pdb.set_trace()
    offspring = []
    possible_postions = []
    for i in range(len(chromosome.path) - 1):
        try:
            offspring.extend(chromosome.path[i])
        except TypeError:
            import pdb;pdb.set_trace()

    for i in range(1, len(offspring)):
        possible_postions.append(i)

    for i in range(mutation_rate):

        position_1, position_2 = random.sample(possible_postions, 2)
        temp = offspring[position_1]
        offspring[position_1] = offspring[position_2]
        offspring[position_2] = temp

    offspring.extend(END_CITY)
    path = "".join(offspring)
    new_offspring = Genome(path, fitness(path))
    return new_offspring


def total_population_score(population):
    """Calculate the total score of the population by adding all of their fitness scores."""

    score = 0
    for individual in population:
        score += individual.fitness
    return float(score)


def initialize_population(population_size, cities):
    """Function to initialize a random population."""
    
    def generate_path(cities, start_city, end_city):
        """Function to generate a random path."""
        # start_city = random.choice(cities)
        remaining_cities = [city for city in cities if city not in [start_city, end_city]]
        random.shuffle(remaining_cities)
        # end_city = start_city
        path = [start_city] + remaining_cities + [end_city]

        '''
        for i in range(len(remaining_cities)):
            if i == 6:
                break
            city = remaining_cities[i]
            if city != end_city:
                path.append(city)
        path.append(end_city)
        '''
        # logger.info(path)
        return ''.join(path)
    
    
    population = []

    for _ in range(population_size):
        path = generate_path(cities, start_city=START_CITY, end_city=END_CITY)
        # import pdb;pdb.set_trace()
        individual = Genome(
            path, 
            fitness(path), # Since each genome is a random path in the graph
        )
        population.append(individual)
    # import pdb;pdb.set_trace()
    return population


# Main Function

def main():

    # Initialize a population.
    # import pdb;pdb.set_trace()
    population = initialize_population(population_size, cities)
    score = total_population_score(population)

    current_gen = 1

    # fittest = []

    # Apply genetic algorithm until a maximum number of generations is reached or the population score is greater than threshhold.
    while True:
        # import pdb;pdb.set_trace()
        print("\n\nGeneration: ", current_gen)
        print("Score: ", score)

        fittest_genomes = tournament_selection(population, selection_pressure)

        # Print Fittest Genomes after selection.
        print("\nFittest Genomes:\nPATH\t\tFITNESS")
        for _ in fittest_genomes:
            print(_.path, "\t", _.fitness)

        new_generation = []
        possible_parents = []

        for i in range(len(fittest_genomes)):
            possible_parents.append(i)

        for i in range(population_size-len(fittest_genomes)):

            parent_1, parent_2 = random.sample(possible_parents, 2)
            new_offspring = ordered_crossover(
                fittest_genomes[parent_1], fittest_genomes[parent_2], 1, 5)
            mutated_new_offspring = mutation(new_offspring)
            new_generation.append(mutated_new_offspring)

        for i in range(len(fittest_genomes)):
            mutated_new_offspring = mutation(fittest_genomes[i])
            new_generation.append(mutated_new_offspring)

        # Print the new generation.
        print("\nNew Generation:\nPATH\t\tFITNESS")
        for i in new_generation:
            print(i.path, "\t", i.fitness)

        # Stopping Criterion.
        if (score <= threshhold or current_gen == maximum_generations):

            # Print the generation number and the shorted distance found by the genetic algorithm.
            print("\n\nGeneration: ", current_gen, "/", maximum_generations)
            fittest_genomes.sort(key=lambda x: x.fitness)
            print("Shortest Distance Found:",
                  fittest_genomes[0].path, fittest_genomes[0].fitness)
            break

        population = new_generation
        score = total_population_score(population)
        current_gen += 1


if __name__ == "__main__":
    main()
