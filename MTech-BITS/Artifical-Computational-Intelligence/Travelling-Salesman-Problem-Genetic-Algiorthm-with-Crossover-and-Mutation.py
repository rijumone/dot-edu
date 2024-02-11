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
"""


import random
# from math import inf
from dataclasses import dataclass
# from loguru import logger



max = 999
START_BLOODBANK = 'A'
END_BLOODBANK = 'H'


# Initialize Parameters.

population_size = 9
max_generations = 399
mutation_rate = 1
selection_pressure = 5
convergence_rate = 0.86
threshhold = population_size * max * convergence_rate


# Initialize Graph.

total_bloodbanks = 7


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


@dataclass
class Genome:
    path: str
    fitness : int = None
    
    def __post_init__(self, ):
        self.fitness = fitness(self.path)

# Define fitness function.

def fitness(path):
    """Calculates fitness by adding the distance between all the neigbouring bloodbanks in the path,
    and return the total distance traversed in a given path."""

    total_distance = 0
    for i in range(len(path)-1):
        # if there is no path between the two bloodbanks return max, else add it to the total distance travelled.
        try:
            if graph[position[path[i]]][position[path[i+1]]] == max:
                return max
        except KeyError:
            import pdb;pdb.set_trace()
        total_distance += graph[position[path[i]]][position[path[i+1]]]
    return total_distance



def tournament_selection(population, selection_pressure):
    """Return selection_pressure number of fittest individuals in a given population."""
    # import pdb;pdb.set_trace()
    population.sort(key=lambda x: x.fitness)
    fittest = population[0:selection_pressure]
    return fittest


def apply_ordered_crossover(parent_1, parent_2, crossover_start, crossover_end):
    """Apply ordered cross (OX) on a genome and return the newly generated genome.
    Pairs of selected individuals (parents) are combined to produce offspring through crossover or
    recombination. This involves exchanging genetic material (e.g., sub-tours in the TSP) between parents to
    create new solutions. The crossover operator helps explore the solution space by combining beneficial
    traits from different individuals."""
    
    # Initialize the child with the same length as parents
    p1_path = list(parent_1.path[0:len(parent_1.path)])
    p2_path = list(parent_2.path[0:len(parent_2.path)])
    child = [START_BLOODBANK] + ([-1] * (len(p1_path)-2)) + [END_BLOODBANK]

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
    return Genome(child)


def apply_mutation(chromosome):
    """Apply mutation by replacing a random order of bloodbanks and return the newly generated genome."""

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

    offspring.extend(END_BLOODBANK)
    path = "".join(offspring)
    new_offspring = Genome(path)
    return new_offspring


def calc_total_population_score(population):
    """Calculate the total score of the population by adding all of their fitness scores."""

    return sum([_.fitness for _ in population])

def init_population(population_size, bloodbanks):
    """Function to initialize a random population."""
    
    def generate_path(bloodbanks, start_bloodbank, end_bloodbank):
        """Function to generate a random path."""
        remaining_bloodbanks = [bloodbank for bloodbank in bloodbanks if bloodbank not in [start_bloodbank, end_bloodbank]]
        random.shuffle(remaining_bloodbanks)
        path = [start_bloodbank] + remaining_bloodbanks + [end_bloodbank]
        return ''.join(path)
    
    
    population = []

    for _ in range(population_size):
        path = generate_path(bloodbanks, start_bloodbank=START_BLOODBANK, end_bloodbank=END_BLOODBANK)
        individual = Genome(path)
        population.append(individual)
    return population


# Main Function

def main():
    # Initialize a population.
    population = init_population(population_size, position.keys())

    current_gen = 0

    # fittest = []

    # Apply genetic algorithm until a maximum number of generations is reached or the population score is greater than threshhold.
    while True:
        current_gen += 1
        score = calc_total_population_score(population)
        print("\n\nGeneration: ", current_gen)
        print("Score: ", score)
        # import pdb;pdb.set_trace()
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
            new_offspring = apply_ordered_crossover(
                fittest_genomes[parent_1], fittest_genomes[parent_2], 1, 5)
            mutated_new_offspring = apply_mutation(new_offspring)
            new_generation.append(mutated_new_offspring)

        for i in range(len(fittest_genomes)):
            mutated_new_offspring = apply_mutation(fittest_genomes[i])
            new_generation.append(mutated_new_offspring)

        # Print the new generation.
        print("\nNew Generation:\nPATH\t\tFITNESS")
        for i in new_generation:
            print(i.path, "\t", i.fitness)

        # Stopping Criterion.
        if (score <= threshhold or current_gen >= max_generations):

            # Print the generation number and the shorted distance found by the genetic algorithm.
            print("\n\nGeneration: ", current_gen, "/", max_generations)
            fittest_genomes.sort(key=lambda x: x.fitness)
            print("Shortest Distance Found:",
                  fittest_genomes[0].path, fittest_genomes[0].fitness)
            break

        population = new_generation
        


if __name__ == "__main__":
    main()
"""
Find and print space and time complexity using code in your implementation.
Space Complexity Analysis:
Identify the Inputs:

Similar to the time complexity analysis, identify the inputs that affect the amount of memory used by the algorithm.
Determine Memory Usage:

Analyze the data structures and variables used in the algorithm to determine how much memory is consumed.
Determine Dominant Terms:

Identify the most significant terms in memory usage, which typically correspond to the sizes of data structures or the number of recursive calls.
Express Complexity:

Express the space complexity using Big O notation, focusing on the dominant terms.
"""