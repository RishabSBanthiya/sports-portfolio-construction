from itertools import product
import math 

#Find all possible portolfios
def find_combinations(outcomes, n):
    if n > len(outcomes):
        return []

    combinations = list(product(*outcomes))
    n_element_combinations = [combo for combo in combinations if len(combo) == n]
    return n_element_combinations

outcomes = []

import csv
# Initialize an empty list to store arrays of pairs
pair_arrays = []

# Open the CSV file for reading
with open('Sep29.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    
    # Skip the header row if present
    next(reader, None)
    
    # Initialize a temporary list for each array of pairs
    temp_array = []
    
    for row in reader :
        # Assuming you want to extract the 2nd and 10th columns (0-based indexing)
        i_value = row[2]
        b_value = row[9]
        
        # Create a pair and append it to the temporary array
        pair = (i_value, b_value)
        temp_array.append(pair)
        
        # Check if you've reached the 10th row
        if len(temp_array) == 10:
            # Append the temporary array to the main list
            pair_arrays.append(temp_array)
            # Reset the temporary array
            temp_array = []

# Append any remaining values to the main list
if temp_array:
        pair_arrays.append(temp_array)
pair_arrays = pair_arrays[:3]
transposed = list(map(list, zip(*pair_arrays)))

points = find_combinations(transposed, 10)

coords= []
for point in points:
    ep = 0.000000000
    prob = 1.000000000000000
    for val in point:
        ep +=  float(val[1]) 
        prob *= float(val[0]) / 100.000000000000
    coords.append([100*prob, ep])

er = 0.00000000
ep = 0.00000000
el = 0.000000000
p_count =  0
for i in coords:
    er += i[0] * i[1] / 100
    if i[1] > 100:
        ep+= i[0]
        p_count+=1
    else:
        el+= i[0]
    

from matplotlib import pyplot as plt
plt.scatter(*zip(*coords))
plt.show()

print("Profit percentage", ep)
print("Loss percentage", el)
print("Expected return", er)
print("No. of Proft making porfolios", p_count)
print("No. of  porfolios", len(coords))
print("Percentage of profit making portfolios", p_count/len(coords) * 100.000)