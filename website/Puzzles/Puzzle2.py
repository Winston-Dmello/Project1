import random

# Defining 10 different number series
number_series = [
    [0, 1, 1, 2, 3],       # Fibonacci
    [2, 3, 5, 7, 11],      # Prime Numbers
    [1, 3, 6, 10, 15],     # Triangular Numbers
    [1, 8, 27, 64, 125],   # Cubes
    [1, 4, 9, 16, 25],     # Square Numbers
    [0, 1, 10, 11, 100],   # Binary Numbers
    [1, 2, 6, 24, 120],    # Factorial Numbers
    [1, 2, 4, 8, 16],      # Powers of 2
    [0, 1, 3, 7, 15],      # Powers of 2 minus 1
    [1, 3, 9, 27, 81]      # Powers of 3
]

# Defining an array of expected next numbers
next_num = [5, 13, 21, 216, 36, 101, 720, 32, 31, 243]

def generate_modified_series():
    # Generating a random index to select a number series
    random_index = random.randint(0, len(number_series) - 1)

    # Getting the selected number series and its expected next number
    selected_series = number_series[random_index]
    expected_next = next_num[random_index]

    # Appending the expected next number to the selected series
    modified_series = selected_series + [expected_next]
    return modified_series
