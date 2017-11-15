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
File:       Eugenics.py
File Description:
            Main genetic algorithm component.
"""

from Breeder import Breeder
from random import random
from time import time

#########################
# Configurables         #
#########################
max_time = 20           # Maximum time the algorithm is allowed to run.
max_gens = 100000       # Maximum generations the algorithm is allowed to run.
population_size = 100   # Number of individuals in each generation.
mutation_chance = 0.03  # Chance of an individual being spontaneously mutated.
tournament_size = 4     # Number of individuals in the arena in tournaments for breeding.
#########################

if __name__ == "__main__":

    gen = 0                 # Create the generational index
    global_start = time()   # Remember when the whole process started running.

    Sauron = Breeder(population_size, tournament_size)

    # Do generations until either the time or generations allowed is over the limit.
    while gen < max_gens and time() - gen_start < max_time:
        gen += 1            # Increment the generation count.

        # Breed the current generation to create the next.
        for _ in range(Sauron.population_size):
            child = Sauron.breed(Sauron.mating_ritual())

            if random() <= mutation_chance:
                child = Sauron.mutate(child)    # If it pleases the fates of chance, mutate the child.

            Sauron.next_population.append(child)  # Put the child in the next generation.

        # TODO: Note noteworthy things about the new generation.

        # TODO: Once I have a way to examine errors in the minions, log any program that comes up clean.
