"""
Programmer:        Zachary Champion
Project:           Project Metatron Timer
Description:       Times a few short runs of Metatron and averages the results
Date Last Updated: 8 May 2017
"""
import Metatron
Metatron.Tracer = False
Metatron.Blink_distance = 4

runs = 5
gens_per_run = 500
generations_to_estimate = 10000
times = []

print("Starting timing test...\n")

for i in range(runs):
    run = Metatron.SortingLord(gens_per_run, 100, 0.01, 4)
    meta_timer = Metatron.Timer()
    run.now_go_do_that_voodoo_that_you_do_so_well()
    meta_timer.stop_timer()
    times.append(meta_timer.duration)
    print("==== Test {} complete! ".format(i+1) + '='*100 + "\n\n\n")

avg = sum(times) / len(times)
time_per_gen = avg / gens_per_run

print("\nAverage Time to Run: {:.3f} sec".format(avg))
print("Average time per generation: {:.3f} sec".format(time_per_gen))
print("Projected time for 10,000 generations: {:.3f} minutes".format(time_per_gen * generations_to_estimate / 60))
