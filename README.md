# Eugenics, Inc.
## Description
A genetic algorithm which takes generic, compatible lines of valid Python code and tries to develop new programs with it by means of a genetic algorithm (which inspired the macabre project name).

The first iteration of the project, then called Project Metatron (intended to be a pun on the villain Megatron before it was realized that Metatron is the name of an angel in Judaism), was a genetic algorithm that tries to put together a sorting program in a Minimal Assembly Language (MAL) that a classmate wrote for the project.

## Files
* Eugenics.py  
defines the main procedure of the genetic algorithm. This is where configurables are set.
* Breeder.py  
contains the Breeder class, which details breeding, parent selection, & mutation.
* Minion.py  
contains the objects the Breeder operates on. Defines comparison of Minions & the creation of new Minions.
* dna.py  
contains the lines of Python code the genetic algorithm uses for its "gene pool."

## Constraints & Assumptions
* Assumes a .txt file called dna.py within which exists valid Python code lines.
* Only operates on existing lines of Python code; cannot generate its own lines of code.
