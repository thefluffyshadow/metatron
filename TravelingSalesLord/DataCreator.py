"""
Programmer: Zachary Champion
Project:    metatron
Project Description:
    Traveling Sales Lord
File:       DataCreator.py
File Description:
    Creates a text file with a random sample matrix simulating distance information between n number of cities.
"""
from random import expovariate
from string import ascii_uppercase

n = int(input("How many cities?\n"))
file = input("Filename: ")

city_names = []
for i in range(n):
    if i < 26:
        city_names.append(ascii_uppercase[i])
    elif i >= 26:
        city_names.append(ascii_uppercase[(i // 26) - 1] + ascii_uppercase[i % 26])

# Assuming that all cities are connected by _some_ distance; some are obviously going to be prohibitively far away,
# but that's not the concern of the test data creator.
city_matrix = [[int(expovariate(10) * 1000 + 1) for _ in range(n)] for _ in range(n)]

for i in range(n):
    for j in range(n):
        if i == j:
            city_matrix[i][j] = 0
        elif i > j:
            city_matrix[i][j] = city_matrix[j][i]

file_string = "    {}\n".format("".join(["{:4} ".format(i) for i in city_names]))

# Note: Formatting of city names can handle up to 676 cities (26^2).
for i in range(n):
    file_string += "{:>2}  ".format(city_names[i]) + "{}".format("".join(["{:<4} ".format(val) for val in city_matrix[i]])) + "\n"

with open(file, "w") as writer:
    writer.write(file_string)

print("Write Successful!\n{}".format(file_string))
