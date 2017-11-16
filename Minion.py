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
File:       Minion.py
File Description:
            Class which defines the individual, nicknamed a minion in keeping with the whole eugenics lord theme.
"""

from random import randint, shuffle


class Minion:
    def __init__(self, program_id, program):
        self.id = program_id

        # Program is passed in as a list from breeding (or from new generation).
        # If no given program (i.e. from breeding) is passed in, then a new program is generated for the Minion.
        self.program = program

        self.fitness = self.fitness(self.program)

    def __str__(self):
        return "Minion {}:\n{}".format(self.id, '\n'.join(self.program))

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __len__(self):
        return len(self.program)

    def fitness(self, program):
        """
        Measures and returns the fitness of the minion.
        :return: int
        """
        return randint(-1000, 1000)
