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
            Breeder class - details how to breed, select parents, etc.
"""

import Minion
from random import seed, randint, choice


class Breeder:
    def __init__(self, population_size, tournament_size):
        # Breeder's policies
        self.population_size = population_size
        self.tournament_size = tournament_size

        # Breeder's inventory
        self.population = [Minion.spawn_program() for _ in range(self.population_size)]
        self.next_population = []

        # Breeder's records - overall
        self.best_minion = None  # Best program so far
        self.elite_force = []  # Here is going to be the list of all the programs that run without errors.

    @staticmethod
    def breed(parents):
        """
        Breeds two parent programs together to get a single child.
        WISHLIST: Get two children and return the most fit child.
        :param parents: (tuple, contains 2 parents)
        :return: a single child minion object
        """
        seed()  # Seed the random functions anew every time.

        # Unpack the parents tuple.
        parent1 = parents[0]
        parent2 = parents[1]

        # Now kith.
        gene_bgn = randint(1, min((len(parent1), len(parent2))) - 1)  # Generates a random index in the shorter of
        gene_end = randint(1, min((len(parent1), len(parent2))) - 1)  # parent1 or parent2.

        # I want the gene to be switched from parent1 to parent2 for now.
        # Later, it may just switch the genes between the two parents and return both as children.
        # Also, see function comment above for possible wish list feature.
        child = parent1[:gene_bgn] + parent2[gene_bgn:gene_end] + parent1[gene_end:]

        return child

    @staticmethod
    def mutate(minion):
        """
        Mutates the minion (python code) in some way.
        Right now, it creates an entirely new program.
        :param minion:
        :return:
        """
        return Minion.spawn_program()

    def mating_ritual(self):
        """
        Uses tournament selection with a variable sized tournament to select breeding parent individuals.
        Returns the two most fit parents in the randomly selected arena to breed.
        :param population:
        :return: a tuple with 2 parents
        """
        # Choose random tournament participants up to the size of the tournament.
        arena = [choice(self.population) for _ in range(self.tournament_size)]

        # Look through the arena for the most and second most fit individuals.
        champion, runnerup = arena[0], arena[1]
        for gladiator in arena:
            if gladiator.fitness > champion.fitness:
                runnerup = champion
                champion = gladiator
            elif gladiator.fitness > runnerup.fitness:
                runnerup = gladiator

        return champion, runnerup
