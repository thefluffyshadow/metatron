"""
Programmer:         Zachary Champion
Project:            Project Metatron
Description:        A Genetic Algorithm (GA) which breeds the best sorting algorithm in an arbitrary assembly language
                    named MAL (I've been assured it's not malware).
                    Made for Python 3.6
Date Last Updated:  1 June 2017
"""
from random import random, seed, choice, randint, shuffle
from malpy import cycleanalyzer, parser
from time import time

# Highly necessary global variables and objects for MALpy.
source = {
        'END': 0,       # Each element is the command as the key and the number of arguments it takes
        'BR': 1,        # as the value
        'INC': 1,
        'DEC': 1,
        'MOVE': 2,
        'MOVEI': 2,
        'LOAD': 2,
        'STORE': 2,
        'ADD': 3,
        'SUB': 3,
        'MUL': 3,
        'DIV': 3,
        'BEQ': 3,
        'BLT': 3,
        'BGT': 3
        }
MAL_Parser = parser.Parser()            # Will help parse the MAL instructions.
runner = cycleanalyzer.CycleAnalyzer()  # Evaluates the parsed instructions?

seed()  # Change the random seed each time the code is run.


class Timer:
    def __init__(self):
        self.start_time = time()
        self.end_time = None
        self.duration = None

    def stop_timer(self):
        self.end_time = time()
        self.duration = self.end_time - self.start_time

    def reset_timer(self):
        self.duration = time() - self.start_time
        self.start_time = time()
        self.end_time = None


class SortingLord:
    """
    SortingLord is the entity which manages the generational eugenics of his sorting minions.
    It is the overall genetic algorithm manager.
    """

    def __init__(self, max_generations, population_size, mutation_chance, tournament_size):
        """
        :param max_generations: The maximum number of generations that the GA will run.
        :param population_size: The number of minions (candidate sorting programs) per generation.
        :param mutation_chance: The chance as a decimal of mutation if the member is less than average fit
        :param tournament_size: The number of members to go into the tournament
        """
        # Here are the parameters of the GA.
        self.max_generations = max_generations  # How many generations the GA will run for.
        self.population_size = population_size  # How many program candidates are in each population.
        self.mutation_chance = mutation_chance  # Percent chance that a given child will mutate spontaneously.
        self.tournament_size = tournament_size  # Size of the tournaments used in tournament selection.
        # The number of elite clones to keep - proportional to the population size
        self.elite_clones = int(self.population_size / 10) + 1

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
                    print("New elite: {}".format(''.join(minion)))

        if Tracer:
            print("Elites:")
            for member in self.elite_force:
                print("{}".format(''.join(member)))

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
    def spawn_new_instruction():  # TODO
        instruction = choice(list(source.keys())[1:])

        for _ in range(source[instruction]):

            if instruction[0] == 'B' and len(instruction) > 9:
                instruction += ' L' + str(randint(1, 30))

            else:
                instruction += ' ' + choice(['R', 'V'])

                if instruction[-1] == 'R':
                    instruction += str(randint(0, 15)).zfill(2)

                else:
                    instruction += str(randint(1, 64)).zfill(2)

        return instruction + '\n'

    def spawn_new_minion(self):
        """
        Generates a single "program" - a list of MAL instruction strings separated by newlines.
        :return:
        """
        minion_length = 30  # Variable to adjust how many lines each program starts with.

        new_minion = []
        for _ in range(minion_length - 1):
            new_minion.append(self.spawn_new_instruction())
        new_minion.append("END\n")

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
        child = ""
        while len(child) < 15:
            idx1 = randint(1, len(parent1) - 1)
            idx2 = randint(1, len(parent2) - 1)

            child = parent1[:idx1] + parent2[idx2:]

        return child

    def mutate(self, minion):
        """
        Will take a minion (program represented by a list of strings) and use roulette selection to select
        a mutation to perform on the minion's program.
        :param minion:
        :return: minion with one of its instructions removed.
        """
        mutation_weights = [1, 5, 2]
        mutation_idx = [sum(mutation_weights[:i]) for i in mutation_weights]

        mutation = randint(0, mutation_idx[-1])

        if mutation < mutation_idx[0]:  # Shuffle the whole program
            shuffle(minion)
        elif mutation < mutation_idx[1]:  # Insert a new instruction at a random point in the minion's program
            minion.insert(randint(0, len(minion) - 1), self.spawn_new_instruction())
        else:  # Delete a random instruction from the minion's program
            if len(minion) >= 19:
                del minion[randint(0, len(minion) - 2)]  # Cannot delete the END instruction

        return minion

    @staticmethod
    def test_fitness(minion):
        if Tracer:
            print("test_fitness()")
            print("Minion:\n{}".format(''.join(minion)))
        """
        Evaluates the sorting ability (fitness) of a minion (member of the population).
        :param minion: list[str]
        :return: float - the score of the 'program.'
        """
        def count_inversions(num_list):
            inversions = 0

            for i in range(len(num_list) - 1):
                if num_list[i] > num_list[i + 1]:
                    inversions += 1

            return inversions

        # Make a random list of 64 numbers for the memory.
        memory = list(range(64))
        shuffle(memory)

        # Counts the number of inversions present in the list before sorting attempt.
        initial_inversions = count_inversions(memory)

        # Parse the lines in the "program" as a single "file."
        instructions = MAL_Parser.parse(''.join(minion))
        if Tracer:
            print("Instructions:\n{}".format('\n'.join(str(instructions).split(', '))))

        # Gets a list of true and false for where errors are in the lines of instructions.
        errors_mask = [token[0] == 'E' for token in instructions]
        errors = [token for token, err in zip(instructions, errors_mask) if err]

        # This is the part where the fitness of the thing is calculated based on the filtered error list.
        fitness = 0
        fitness -= len(errors)

        # If the code has no errors, runs the sorting program to see how it does.
        if fitness >= 0:
            runner.run(instructions, memory)

            # Adds fitness points based on the number of inversions removed from the initial list.
            fitness += initial_inversions - count_inversions(memory)

        if Tracer:
            print("Fitness: {:2}".format(fitness))
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

            global_timer = Timer()  # Timer to time the entire GA process
            generation_timer = Timer()  # Timer to time individual generations between displays

            for gen in range(self.max_generations + 1):
                generation_best_fitness = -float('inf')

                if Tracer:
                    for i in range(len(self.population)):
                        print("Minion {}: {} | {}".format(i, self.population[i], self.population_fitness[i]))

                for minion in range(self.population_size):
                    child = self.breed(self.select_breeder(), self.select_breeder())

                    if Tracer:
                        print("Child: " + str(child))

                    if self.test_fitness(child) < self.averageFitness and random() < self.mutation_chance:
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

                if gen % Blink_distance == 0 or gen == self.max_generations:
                    generation_timer.stop_timer()
                    print("|| Generation: {:6,} | Best Fitness: {:3} | ".format(gen, generation_best_fitness) +
                          "Average: {:3.2f} | Overall Best: {:3} | Time: {:4.3f} sec ||".format(
                           self.averageFitness, self.bestFitness, generation_timer.duration))
                    generation_timer.reset_timer()

            global_timer.stop_timer()
            output_string = "Best Program (Fitness: {:})\n".format(self.bestFitness) + \
                            "Generations: {:,}".format(self.max_generations) + '\n' + \
                            "Time to run: {:4.3f} sec\n".format(global_timer.duration) + \
                            '='*32 + '\n' + \
                            "{}".format(''.join(self.best_minion))
            scribe.write(output_string)
            print(output_string)


if __name__ == '__main__':

    Tracer = False
    """
    If Tracer is turned on, debugging statements will be printed to the console.
    Also, when running, the GA will run in a shorter "test mode."
    """
    Blink_distance = 4  # Displays messages every x generations.

    if Tracer:
        HedleyLamarr = SortingLord(1, 15, 0.5, 2)

    else:
        HedleyLamarr = SortingLord(5000, 20, 0.2, 4)

    HedleyLamarr.now_go_do_that_voodoo_that_you_do_so_well()
