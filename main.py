# This is a sample Python script.
from pulp import *
import csv
import itertools

# Input CSV-Objects
objects_1 = []
objects_2 = [] # <- Make this generic
objects_3 = []

with open('input_items.csv') as csv_items:
    has_header = csv.Sniffer().has_header(csv_items.read(1024))
    csv_items.seek(0) # Rewind
    itemsreader = csv.reader(csv_items, delimiter=',')
    if has_header:
        next(itemsreader)
    for row in itemsreader:
        current_item = int(row[0])
        #CLEAN THIS UP
        if current_item == 1:
            objects_1.append([float(row[1]), int(row[2]), int(row[3])])
        if current_item == 2:
            objects_2.append([float(row[1]), int(row[2]), int(row[3])])
        if current_item == 3:
            objects_3.append([float(row[1]), int(row[2]), int(row[3])])
X = len(objects_1) # No. of Objects 1
Y = len(objects_2) # No. of Objects 2
Z = len(objects_3) # No. of Objects 3

def TestAllCases():
    with open('test_pattern.csv') as csv_test_pattern:
        testreader = csv.reader(csv_test_pattern, delimiter=',')
        next(testreader)
        for row in testreader:
            desired_triangles = int(row[0])
            desired_hexagon = int(row[1])
            desired_mini = int(row[2])

            # Initialise LP's for each type
            prob_triangle = LpProblem("NanoleafTriangleProblem", LpMinimize)
            prob_hexagon = LpProblem("NanoleafHexagonProblem", LpMinimize)
            prob_mini = LpProblem("NanoleafMiniTriangleProblem", LpMinimize)

            # Decision Variables
            x = LpVariable.dicts('BuyTriangleBundle', range(X),
                                 lowBound=0,
                                 cat=LpInteger)

            y = LpVariable.dicts('BuyHexagonBundle', range(Y),
                                 lowBound=0,
                                 cat=LpInteger)

            z = LpVariable.dicts('BuyMiniBundle', range(Z),
                                 lowBound=0,
                                 cat=LpInteger)

            # Objective Functions
            # Minimise cost of selected bundles
            prob_triangle += lpSum(
                [x[n] * objects_1[n][0] for n in range(X)]), "Objective: Minimise the cost to buy triangles"
            prob_hexagon += lpSum(
                [y[n] * objects_2[n][0] for n in range(Y)]), "Objective: Minimise the cost to buy hexagons"
            prob_mini += lpSum(
                [z[n] * objects_3[n][0] for n in range(Z)]), "Objective: Minimise the cost to buy mini-triangles"

            # Constraints
            prob_triangle += lpSum([x[n] * objects_1[n][1] for n in range(X)]) >= desired_triangles, (
                "Enough triangles to satisfy desired have to be bought.")
            prob_hexagon += lpSum([y[n] * objects_2[n][1] for n in range(Y)]) >= desired_hexagon, (
                "Enough hexagons to satisfy desired have to be bought.")
            prob_mini += lpSum([z[n] * objects_3[n][1] for n in range(Z)]) >= desired_mini, (
                "Enough mini-triangles to satisfy desired have to be bought.")

            # Solver
            # Write to File / Debugging
            #prob_triangle.writeLP("Nanoleaf_Triangle_Problem.lp")
            prob_hexagon.writeLP("Nanoleaf_Hexagon_Problem.lp")
            #prob_mini.writeLP("Nanoleaf_Mini_Problem.lp")
            # Default solver
            prob_triangle.solve()
            prob_hexagon.solve()
            prob_mini.solve()

            # Outputs
            triangle_sum = 0
            hexagon_sum = 0
            mini_sum = 0
            #print("Solution for Pattern " + row.index())
            print("--- Triangles ---")
            for i in x:
                print("- " + str(x[i].value()) + " for the price of " + str(objects_1[i][0]))
                if x[i].value() >= 1:
                    triangle_sum += x[i].value() * objects_1[i][0]
            print("- Triangle cost is: " + str(triangle_sum))
            print("--- Hexagons ---")
            for i in y:
                print("- " + str(y[i].value()) + " for the price of " + str(objects_2[i][0]))
                if y[i].value() >= 1:
                    hexagon_sum += y[i].value() * objects_2[i][0]
            print("- Hexagon cost is: " + str(hexagon_sum))
            print("--- Mini-triangles ---")
            for i in z:
                print("- " + str(z[i].value()) + " for the price of " + str(objects_3[i][0]))
                if z[i].value() >= 1:
                    mini_sum += z[i].value() * objects_3[i][0]
            print("----------------------")
            print("- Mini-triangle cost is: " + str(mini_sum))
            print("Total is: " +  str(triangle_sum+hexagon_sum+mini_sum))

if __name__ == '__main__':
    print(objects_1)
    print(objects_2)
    print(objects_3)
    TestAllCases()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
