import random

def generate_magic_square():
    # List of predefined magic arrays
    magic_array = [
        [1, 3, 5, 4, 7, 2, 8, 9, 6],
        [11, 13, 15, 14, 17, 12, 18, 19, 16],
        [21, 23, 25, 24, 27, 22, 28, 29, 26],
        [31, 33, 35, 34, 37, 32, 38, 39, 36],
        [41, 43, 45, 44, 47, 42, 48, 49, 46],
        [51, 53, 55, 54, 57, 52, 58, 59, 56]
    ]

    # List of corresponding answers
    magic_solution = [15, 45, 75, 105, 135, 165]

    # Randomly select a magic array and its corresponding answer
    index = random.randint(0, len(magic_array) - 1)
    array = magic_array[index]
    random.shuffle(array)
    answer = magic_solution[index]
    
    # Return a list containing the selected array and its answer
    return [array, answer]

def check_invalid(given_list, user_guess):
    # Check if all numbers in given_list are present in user_guess
    if not all(num in user_guess for num in given_list):
        return True 

    # Check if any number in user_guess is repeated
    if len(set(user_guess)) != len(user_guess):
        return True 

    return False


def check_magic_sq(array):
    magic_array = array[0]
    magic_const = array[1]

    # Split the magic array into rows
    matrix = [magic_array[i:i+3] for i in range(0, 9, 3)]

    # Sum the rows, columns, and diagonals and check with the magic constant
    for i in range(3):
        row_sum = sum(matrix[i])
        col_sum = sum(matrix[j][i] for j in range(3))

        if row_sum != magic_const or col_sum != magic_const:
            return False

    # Check diagonals
    diag1_sum = matrix[0][0] + matrix[1][1] + matrix[2][2]
    diag2_sum = matrix[0][2] + matrix[1][1] + matrix[2][0]

    return diag1_sum == magic_const and diag2_sum == magic_const

#print(generate_magic_square())
#print(check_magic_sq([[8,1,6,3,5,7,4,9,2],15]))