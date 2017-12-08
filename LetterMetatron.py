"""
Programmer:         Zachary Champion
Project:            Project Metatron
Description:        A Genetic Algorithm (GA) which breeds a particular string from a pool of chars.

                    The algorithm breeds by concatenating minions (program candidates) together at two different
                        indexes (thus making the length of the minion variable).
                    Parent selection, before that, is done by tournament selection with a definable tournament size.

                    Made for Python 3.6
Date Last Updated:  13 May 2017
"""
from random import random, seed, choice, randint, shuffle
from string import ascii_letters
from time import time

seed()  # Change the random seed each time the code is run.
source = ' ' + ascii_letters + ' '

class SortingLord:
    """
    SortingLord is the entity which manages the generational eugenics of his sorting minions.
    It is the overall genetic algorithm manager.
    """
    def __init__(self, max_time, max_generations, population_size, mutation_chance, tournament_size):
        """
        :param max_generations: The maximum number of generations that the GA will run.
        :param population_size: The number of minions (candidate sorting programs) per generation.
        :param mutation_chance: The chance as a decimal of mutation if the member is less than average fit
        :param tournament_size: The number of members to go into the tournament
        """
        # Here are the parameters of the GA.
        self.max_time = max_time * 60           # How many seconds (input as minutes) the GA will run for.
        self.max_generations = max_generations  # How many generations the GA will run for.
        self.population_size = population_size  # How many program candidates are in each population.
        self.mutation_chance = mutation_chance  # Percent chance that a given child will mutate spontaneously.
        self.tournament_size = tournament_size  # Size of the tournaments used in tournament selection.
        # The number of elite clones to keep - proportional to the population size
        self.elite_clones = int(self.population_size / 30) + 1

        # Here is where the meat of the GA is - this is the information on the population itself and relevant stats
        self.population = [self.spawn_new_minion() for _ in range(self.population_size - self.elite_clones)]
        self.population_fitness = [self.test_fitness(minion) for minion in self.population]
        self.population_next = []           # The list of the upcoming generation
        self.population_fitness_next = []   # The list of the fitness values of the upcoming generation
        self.elite_force = []
        self.recruit_elites()
        self.elite_force_fitness = [self.test_fitness(minion) for minion in self.elite_force]

        # Here is the ledger for the records of the GA's findings
        self.best_minion = None             # The string of the best program so far
        self.bestFitness = -float('inf')    # The value of the best fitness found
        self.worstFitness = float('inf')    # The value of the worst fitness found
        self.averageFitness = 0             # The value of the average fitness of the current generation

    def recruit_elites(self):
        elites = []

        for minion in range(self.elite_clones):
            elites.append(self.population[minion])

        self.elite_force = elites
        for minion in self.population:
            self.try_out_elite(minion)

    def try_out_elite(self, minion):
        for elite in range(len(self.elite_force)):
            if self.test_fitness(minion) > self.test_fitness(self.elite_force[elite]) and \
                            minion not in self.elite_force:
                self.elite_force[elite] = minion
                if Tracer:
                    print("New elite: {}".format(minion))

    def update_fitness_ledgers(self):
        """
        Updates the variables keeping track of the best, worst, and average fitnesses of the current generation.
        Also updates the best_minion variable to keep the best program overall.
        :return:
        """
        if max(self.population_fitness) > self.bestFitness:
            self.bestFitness = max(self.population_fitness)
            self.best_minion = self.population[self.population_fitness.index(self.bestFitness)]

        self.worstFitness = min(self.population_fitness)

        avg = 0
        for fitness in self.population_fitness:
            avg += fitness
        avg /= len(self.population_fitness)
        self.averageFitness = avg

    @staticmethod
    def spawn_new_minion():
        new_minion = [char for char in source]

        return new_minion

    def select_breeder(self):
        """
        Uses tournament selection with a variable sized tournament to select breeding parents.
        :return: winning parent
        """
        tournament_pool = []

        for _ in range(self.tournament_size):
            tournament_pool.append(choice(self.population + self.elite_force))

        winner = tournament_pool[0]
        for gladiator in tournament_pool:
            if self.test_fitness(gladiator) > self.test_fitness(winner):
                winner = gladiator

        if Tracer:
            print("Selected: " + str(winner))

        return winner

    @staticmethod
    def breed(parent1, parent2):
        """
        Will take in two parents and cross them with each other.
        :param parent1: list[str]
        :param parent2: list[str]
        :return: child list[str]
        """
        idx1 = randint(1, len(parent1) - 1)
        idx2 = randint(1, len(parent2) - 1)

        child = parent1[:idx1] + parent2[idx2:]

        return child

    @staticmethod
    def mutate(minion):
        mutation_weights = [1, 3, 3]
        # Mutation 0: Shuffle the string
        # Mutation 1: Add random characters to the end of the string
        # Mutation 2: Increment random characters in the string by 1 character

        mutation_choice = random() * sum(mutation_weights)

        # Turn the mutation weights list into a list of probabilities
        for i in range(len(mutation_weights)):
            mutation_weights[i] = sum(mutation_weights[0:i+1])

        # Mutation 0
        if mutation_choice < mutation_weights[0]:
            shuffle(minion)

            if Tracer:
                print("Mutation - shuffling")
                print("Mutated: " + str(minion))

        # Mutation 1
        elif mutation_choice < mutation_weights[1]:
            delta = randint(2, len(minion))
            for _ in range(delta):
                minion.append(source[randint(0, len(source)) - 1])

            if Tracer:
                print("Mutation - appending characters")
                print("Mutated: " + str(minion))

        # Mutation 2
        elif mutation_choice < mutation_weights[2]:
            for c in range(len(minion)):
                if random() < 0.5:
                    minion[c] = chr(ord(minion[c]) + 1)

            if Tracer:
                print("Mutation - incrementing characters")
                print("Mutated: " + str(minion))

        return minion

    @staticmethod
    def test_fitness(minion):
        scale = len(goal)
        fitness = 0

        if len(minion) != scale:
            fitness -= scale * abs(len(minion) - len(goal))
        else:
            for char in minion:
                if char in goal:
                    fitness += scale

            for i in range(min((len(minion), len(goal)))):
                if minion[i] == goal[i]:
                    fitness += 3 * scale
                else:
                    fitness -= abs(ord(minion[i]) - ord(goal[i]))

        return fitness

    def now_go_do_that_voodoo_that_you_do_so_well(self):
        """
        Main function, runs the whole GA.
        :return: returns nothing.
        """
        with open("theAncientScrolls.txt", 'w') as scribe:
            # Record the first 5 programs to analyze later
            scribe.write("Record of the SortingLord Genetic Algorithm\n" +
                         '='*32 + '\n' +
                         "First 5 programs generated:\n----\n")
            for forefather in range(5):
                scribe.write(''.join(map(str, self.population[forefather])) + '\n----\n')

            # for gen in range(self.max_generations + 1):
            gen = -1
            generation_best_fitness = -float('inf')
            genstart = time()
            glostart = time()

            while generation_best_fitness < self.test_fitness(goal) and \
                            gen < self.max_generations and \
                            time() - glostart < self.max_time:

                if time() - genstart > 1:
                    genstart = time()
                gen += 1

                if Tracer:
                    for i in range(len(self.population)):
                        print("Minion {}: {} | {}".format(i, self.population[i], self.population_fitness[i]))

                for minion in range(self.population_size):
                    child = self.breed(self.select_breeder(), self.select_breeder())

                    if Tracer:
                        print("Child: " + str(child))

                    if random() < self.mutation_chance:
                        child = self.mutate(child)

                    generation_best_fitness = max(self.population_fitness)

                    self.population_next.append(child)
                    self.population_fitness_next.append(self.test_fitness(child))

                self.population = self.population_next
                self.population_fitness = self.population_fitness_next
                self.population_next = []
                self.population_fitness_next = []
                self.update_fitness_ledgers()

                for minion in self.population:
                    self.try_out_elite(minion)

                if Tracer:
                    print("Elites:")
                    for member in self.elite_force:
                        print('> \'' + ''.join(member) + '\'')

                if time() - genstart > 1 or gen == self.max_generations or gen == 0:
                    gen_time = time() - genstart
                    print("|| Generation: {:8,} | Best Fitness: {:8,} ".format(gen, generation_best_fitness) +
                          "| Average: {:8,} | Overall Best: {:8,} | ".format(self.averageFitness, self.bestFitness) +
                          "Time: {:4.3f} sec || {}".format(gen_time, ''.join(choice(self.elite_force))))

            global_timer = time() - glostart

            time_to_run = "{:0>2.0f}:{:0>6.3f}".format(global_timer / 60, global_timer % 60)

            output_end_string = "Best Program (Fitness: {:8,})\n".format(self.bestFitness) + \
                                "Generations: {:8,}\n".format(gen) + \
                                "Time to run: {}\n".format(time_to_run) + \
                                '='*32 + '\n' + \
                                "{}".format(''.join(self.best_minion))
            scribe.write(output_end_string)
            print(output_end_string)


if __name__ == '__main__':

    Tracer = False
    """
    If Tracer is turned on, debugging statements will be printed to the console.
    Also, when running, the GA will run in a shorter "test mode."
    """
    goal = "Champion of the World"

    if Tracer:
        HedleyLamarr = SortingLord(1, 10, 6, 0.5, 2)

    else:
        HedleyLamarr = SortingLord(20, float("inf"), 100, 0.005, 2)

    HedleyLamarr.now_go_do_that_voodoo_that_you_do_so_well()
