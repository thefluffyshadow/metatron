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

from random import random, choice
from time import time
from ProgramMetatron.Breeder import Breeder


def build_army(max_time, max_gens, population_size, mutation_chance, tournament_size):
    gen = 0                 # Create the generational index
    global_start = time()   # Remember when the whole process started running.

    Sauron = Breeder(get_genes(), population_size, tournament_size)

    # Do generations until either the time or generations allowed is over the limit.
    while gen < max_gens and time() - global_start < max_time:
        gen += 1            # Increment the generation count.

        # Breed the current generation to create the next.
        for _ in range(Sauron.population_size):
            child = Sauron.breed(Sauron.mating_ritual())

            # If it pleases the fates of chance, mutate the child.
            if random() <= mutation_chance:
                Sauron.mutate(child)

            Sauron.next_population.append(child)  # Put the child in the next generation.

        for minion in Sauron.population:
            if minion.fitness > min_program_len:
                Sauron.elite_force.append(minion)

        # Reset for the next generation?
        Sauron.population = Sauron.next_population
        Sauron.next_population = []

    if len(Sauron.elite_force) > 0:
        # After it is finished running, print to a file all of the programs that worked.
        # Write only the best 10 programs or 10 random programs.
        # Write each program to a separate file named by the minion ID.py
        for _ in range(10):
            p = choice(Sauron.elite_force)
            with open("Minion" + p.id + ".py", "w") as scribe:
                scribe.write("\r\n".join(p.program))
        # Note: at the moment, would break if the length of the elite force happens to be under 10. As it is, that's
        # unlikely, but it could happen with future changes, so this should be fixed.

    # Print to the terminal some overall statistics.
    print("{:,} programs longer than {} lines generated.".format(len(Sauron.elite_force), min_program_len))
    print("Ran for {:,} generations over {:.3f} seconds.".format(gen, time() - global_start))

    return len(Sauron.elite_force)


def get_genes():
    with open("dna.py") as f:
        prog = f.read().split("\n")

    # Filter out blank lines and comment lines
    line = 0
    while line != len(prog):
        if line == 0 and (prog[line].strip() == "" or prog[line].startswith("#")):
            prog = prog[1:]
            continue
        elif prog[line].strip() == "" or prog[line].startswith("#"):
            prog = prog[:line] + prog[line+1:]
            continue
        line += 1

    return prog


if __name__ == "__main__":
    #########################
    # Configurables         #
    #########################
    max_time = 30           # Maximum time in seconds the algorithm is allowed to run.
    max_gens = 100000       # Maximum generations the algorithm is allowed to run.
    population_size = 100   # Number of individuals in each generation.
    mutation_chance = 0.03  # Chance of an individual being spontaneously mutated.
    tournament_size = 4     # Number of individuals in the arena in tournaments for breeding.
    min_program_len = 8     # The minimum length of a working program for it to be recorded.
    #########################

    # Now the show begins!
    strength = build_army(max_time, max_gens, population_size, mutation_chance, tournament_size)

    while strength < 1:
        strength = build_army(max_time, max_gens, population_size, mutation_chance, tournament_size)
