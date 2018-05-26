"""
Programmer: Zachary Champion
Project:    Traveling Sales Lord
Project Description:
    Will use a genetic algorithm to tackle the Traveling Salesman Problem.
File:       TravelingSalesLord.py
File Description:
    Main GA component
"""


def bullshit():
    print("bullshit")


def find_sales_route(max_time, max_gens, pop_size, mutation_chance, tournament_size):
    best_route = ['B', 'C', 'D', 'E', 'F', 'G']
    return best_route

def load_map(filename):
    with filename as map:
        file_contents = map.read()



if __name__ == "__main__":
    #########################
    # Configurables         #
    #########################
    max_time = 30           # Maximum time in seconds the algorithm is allowed to run.
    max_gens = 100000       # Maximum generations the algorithm is allowed to run.
    population_size = 100   # Number of individuals in each generation.
    mutation_chance = 0.03  # Chance of an individual being spontaneously mutated.
    tournament_size = 4     # Number of individuals in the arena in tournaments for breeding.
    #########################
