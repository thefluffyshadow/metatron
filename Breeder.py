"""
Programmer: Zachary Champion
Project:    metatron
Project Description:
            A program that generates programs in the same language in which the program itself is written.
            Metatron Jr. uses a genetic algorithm to breed programs in python; it writes down anything that works
            (runs without errors) and discard the rest.
            Individuals will be encoded as lists of lines of python which will not include the newline char.
            Gladiatorial combat will determine who gets the honor of breeding (tournament selection will decide breeding
            parents).
File:       Breeder.py
File Description:
            Main genetic algorithm component.
"""

import Minion
from random import seed, randint


class Breeder:
    def __init__(self, max_generations, population_size, mutation_chance, tournament_size):
        # Breeder's policies
        self.max_generations = max_generations
        self.population_size = population_size
        self.mutation_chance = mutation_chance
        self.tournament_size = tournament_size

        # Breeder's records
        # TODO: think of stats to keep track of

    @staticmethod
    def breed(parent1, parent2):
        """
        Breeds two parent programs together to get a single child.
        WISHLIST: Get two children and return the most fit child.
        :param parent1:
        :param parent2:
        :return:
        """
        seed()  # Seed the random functions anew every time.

        gene_bgn = randint(1, min((len(parent1), len(parent2))) - 1)  # Generates a random index in the shorter of
        gene_end = randint(1, min((len(parent1), len(parent2))) - 1)  # parent1 or parent2.

        # I want the gene to be switched from parent1 to parent2 for now.
        # Later, it may just switch the genes between the two parents and return both as children.
        # Also, see function comment above.
        child = parent1[:gene_bgn] + parent2[gene_bgn:gene_end] + parent1[gene_end:]

        return child

    def mutate(self, minion):
        return minion.generate_python()
