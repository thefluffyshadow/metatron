#!env python

# This makes printing work like python 3.x, be aware changing this
# will break every print statement and must be fixed manually.
# Comment the next line if you are unfamiliar with python3 printing
from __future__ import print_function

import sys
# import math

# For random ranges and memory shuffling
from random import random, seed, shuffle

# Mal-Python MUST be installed.
# Ask Luke if pip (python's package manager) or malpy gives you troubles.
from malpy import cycleanalyzer, parser

# use numpy for quick averages. may break on windows
# from numpy import mean as avg

seed()  # Change random seed each run. Default is time based.


# declare these as global.
# Re-declared parsers/runners in the fitness function is costly.
Parser = parser.Parser()  # text->parse-tree class.
runner = cycleanalyzer.CycleAnalyzer()  # parse-tree evaluation class.


def fitness(gene):
    # list[str] -> float
    """Evaluates the fitness of a gene.

    Arguments:
        gene (list[str]): a List of each line of the `file`.

    Returns:
        float: the evaluated score of the `file`.

    """
    # Make a random list of numbers 0-63 occurring once each.
    # wrap in list so it is persistent and iterable.
    memory = list(range(64))
    # Fisher-Yates shuffle the memory into a random order.
    shuffle(memory)

    # parse the lines as one file
    token_ast = Parser.parse("".join(gene))

    # list of true and false. true if the ast instruction output an error.
    errors_mask = [token[0] == 'E' for token in token_ast]
    errors = [token for token, err in zip(token_ast, errors_mask) if err]

    score = len(errors)
    # We now have a list of the instructions already parsed
    # and a filtered list of each error.

    # =========================================================================
    # Write your fitness evaluation below.

    # pseudo-code:
    # if there are errors:
    #     return error_evaluation
    # else:
    #     run program and return its scored output or run-time errors

    # Write your fitness evaluation above.
    # =========================================================================

    return score


def selection(population_fitness, value):
    # list[int], float -> int
    """Takes in the fitness list and a float. Determines which index
    to use as a parent selector based on the two.

    Arguments:
        population_fitness (list[int]): The fitness of each population member.
        value (float): a random value used to find the index.

    Returns:
        int: The index of the selected parent.

    """
    p = 0
    # =========================================================================
    # Write your selection below.

    # pseudo-code: Roulette wheel with fitness probability selection
    # while value > population_fitness[p]:
    #     p += 1
    #     value -= population_fitness[p]

    # Write your selection above.
    # =========================================================================
    return p


def crossover(parent_1, parent_2):
    # list[str], list[str] -> list[str]
    """Takes two parents and makes a cross between them.

    Arguments:
        parent_1 (list[str]): the instruction strings for the first parent.
        parent_2 (list[str]): the instruction strings for the second parent.

    Returns:
        (list[str]): The new child `file`.

    """

    # This concatenates two lists together.
    # It WILL NOT create good children.
    # It WILL create valid children.
    # Comment this out once you have made a better crossover.
    child = parent_1 + parent_2

    # =========================================================================
    # Write your crossover below.

    # pseudo-code:
    # child = first_half(parent_1)+last_half(parent_2)

    # Write your crossover above.
    # =========================================================================

    return child


def mutation(gene, gene_fitness=None):
    # list[str], float -> list[str]
    """Mutates a gene based on its fitness.

    Arguments:
        gene (list[str]): The `file` gene.
        gene_fitness (float): The fitness of the gene BEFORE mutation.

    Returns:
        (list[str]): the mutated gene.

    """

    # Too much can happen here to give pseudo-code.
    # Structure this to return a mutated gene.

    return gene


def generate_member():
    # None -> list[str]
    """Creates one `file`, a list of instruction strings.
    Each string (line) must end with \n.

    """
    return ["A\n",
            "List\n",
            "of\n",
            "Strings\n",
            "ending\n",
            "with\n",
            "newlines\n",
            "for\n",
            "each\n",
            "instruction\n"]


def main():
    population_member_size = 100
    max_generation_count = 10000

    # Make a list of random `files` for the initial population.
    population = [generate_member() for _ in range(population_member_size)]

    # Evaluate each member's fitness initial score.
    population_fitness = [fitness(gene) for gene in population]

    # Next population's empty list.
    next_population = []
    next_population_fitness = []

    global_best_score = -float('inf')
    global_best = None

    with open('records.txt', 'w+') as output:
        for i in range(max_generation_count):
            for p in range(population_member_size):
                parent_1_idx = selection(population_fitness, random())
                parent_2_idx = selection(population_fitness, random())

                child = crossover(population[parent_1_idx],
                                  population[parent_2_idx])

                if random() < .003:
                    child = mutation(child)

                next_population.append(child)
                next_population_fitness.append(fitness(child))

            population = next_population
            population_fitness = next_population_fitness
            generation_best = max(population_fitness)
            if generation_best > global_best_score:
                global_best_score = generation_best

                # Get the first population member with best score.
                global_best = population[population_fitness
                                         .index(generation_best)]

            print(i, generation_best)

        output.write("Score: {0}\n---\n{1}".format(global_best_score,
                                                   "".join(global_best)))

    print("Done!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
