import random
import enchant

# Function to generate a random word from a list
def generate_random_word():
    word_list = [
        "Arrow", "Caves", "Chief", "Flame", "Grass", "Hunts", "Rocks", "Skull", "Stone", "Swamp", "Wheel", "Woods",
        "Skins", "Tribe", "Earth", "Spear", "Water", "Wheat", "Crops", "Nomad", "Fires", "Boars", "Bones",
        "Flint", "Tools", "Knife", "Trees", "Boats"
    ] 
    return random.choice(word_list)

# Function to check if a word is valid using enchant
def is_valid_word(word):
    english_dict = enchant.Dict("en_US")
    return english_dict.check(word)

# Function to play the Wordle game and return feedback as a string
def play_wordle(secret_word, guessed_word):
    secret_list = list(secret_word)
    guessed_list = list(guessed_word)
    feedback = ["_"] * len(secret_list)

    for i in range(len(guessed_list)):
        if guessed_list[i] == secret_list[i]:
            feedback[i] = "*"
            secret_list[i] = guessed_list[i] = None  # Mark the matched letters

    for i in range(len(guessed_list)):
        if guessed_list[i] in secret_list and guessed_list[i]!=None:
            feedback[i] = "x"
            matched_index = secret_list.index(guessed_list[i])
            secret_list[matched_index] = guessed_list[i] = None  # Mark the matched letters

    return "".join(feedback)



# Function to check if a guessed word is correct
def is_correct_word(secret_word, guessed_word):
    return secret_word == guessed_word
