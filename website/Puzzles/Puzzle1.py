import random
import enchant

# Function to generate a random word from a list
def generate_random_word():
    word_list = ["dates", "space", "clock", "quant", "loops", "pulse", "timer", "speed", "sonic", "light", "stars", "sound", "watch", "visit", "storm", "crash", "shift", "glide"]
    return random.choice(word_list)

# Function to check if a word is valid using enchant
def is_valid_word(word):
    english_dict = enchant.Dict("en_US")
    return english_dict.check(word)

# Function to play the Wordle game and return feedback as a string
def play_wordle(secret_word, guessed_word):
    feedback = ""

    # Count occurrences of each letter in secret_word
    secret_letter_count = {}
    for letter in secret_word:
        if letter != ' ':
            secret_letter_count[letter] = secret_letter_count.get(letter, 0) + 1

    for i in range(len(secret_word)):
        if secret_word[i] == guessed_word[i]:
            feedback += "*"  # Char is in the correct position
        elif guessed_word[i] in secret_letter_count and secret_letter_count[guessed_word[i]] > 0:
            feedback += "x"  # Char is in the word but not in the correct position
            secret_letter_count[guessed_word[i]] -= 1
        else:
            feedback += "_"  # Char is not present in the word

    return feedback


# Function to check if a guessed word is correct
def is_correct_word(secret_word, guessed_word):
    return secret_word == guessed_word
