import random
import time
import matplotlib.pyplot as plt
import statistics


WORD_LIST = ["fig"]

# Define game modes
MODE_SINGLE_PLAYER = "1"
MODE_MULTIPLAYER = "2"
MODE_SIMULATION = "3"

# Define game statistics variables
time_taken_data = []
guesses_data = []

def play_game():
    # Choose a random word from the list
    word = random.choice(WORD_LIST)

    # Initialize variables
    correct_guesses = set()
    incorrect_guesses = set()
    start_time = time.time()

    # Define the hangman image
    hangman = [" _____ ",
               "|     |",
               "|     O",
               "|    /|\\",
               "|    / \\",
               "|",
               "|___"]

    
    while True:
        # Print the word with underscores for unguessed letters
        print(" ".join([letter if letter in correct_guesses else "_" for letter in word]))

        # Print the incorrect guesses and update the hangman image
        if len(incorrect_guesses) > 0:
            print("Incorrect guesses: {}".format(", ".join(sorted(incorrect_guesses))))
            for i in range(len(hangman)):
                if i < len(incorrect_guesses) + 2:
                    print(hangman[i])
                else:
                    print(" " * len(hangman[i]))

        # Get the player's guess
        guess = input("Enter a letter: ").lower()

        # Validate the input
        while not guess.isalpha() or len(guess) != 1:
            guess = input("Invalid input. Please enter a single letter: ").lower()

        # Check if the guess is correct
        if guess in word:
            correct_guesses.add(guess)
        else:
            incorrect_guesses.add(guess)

        # Check if the player has won
        if set(word) == correct_guesses:
            end_time = time.time()
            time_taken = end_time - start_time
            print("Congratulations! You guessed the word '{}' in {:.2f} seconds with {} incorrect guesses.".format(word, time_taken, len(incorrect_guesses)))
            time_taken_data.append(time_taken)
            guesses_data.extend(list(incorrect_guesses))
            break

        # Check if the player has run out of guesses
        if len(incorrect_guesses) >= 6:
            print("Sorry, you have run out of guesses. The word was '{}'.".format(word))
            for i in range(len(hangman)):
                if i == 1:
                    print(hangman[i] + "  Game Over!")
                elif i < 6:
                    print(hangman[i])
                else:
                    print(" " * len(hangman[i]))
            break

def play_single_player():
    play_game()

def play_multiplayer():
    num_players = int(input("Enter the number of players: "))
    times_taken = []  # list to store the time taken by each player

    for i in range(num_players):
        print("Player {}'s turn:".format(i+1))
        start_time = time.time()  # start timing the player's guess
        play_game()
        end_time = time.time()  # stop timing the player's guess
        time_taken = end_time - start_time
        times_taken.append((i+1, time_taken))  # store the player number and their time taken

    # sort the list based on time taken and display the winner
    times_taken.sort(key=lambda x: x[1])
    print("Player {} wins with a time of {:.2f} seconds!".format(times_taken[0][0], times_taken[0][1]))

def play_simulation():
    num_games = int(input("Enter the number of games to simulate: "))
    for i in range(num_games):
        print("Game {}:".format(i+1))
        play_game()

# Get the game mode from the user
mode = input("Choose a game mode:\n1. Single player\n2. Multiplayer\n3. Simulation\n")
while mode not in [MODE_SINGLE_PLAYER, MODE_MULTIPLAYER, MODE_SIMULATION]:
    mode = input("Invalid input. Please choose a game mode:\n1. Single player\n2. Multiplayer\n3. Simulation\n")

# Play the game according to the chosen mode
if mode == MODE_SINGLE_PLAYER:
    play_single_player()
elif mode == MODE_MULTIPLAYER:
    play_multiplayer()
else:
    play_simulation()
    
# Display statistical analysis in graphical format
plt.subplot(2, 1, 1)
plt.hist(time_taken_data, bins=10)
plt.title("Time taken to guess word")
plt.xlabel("Time (seconds)")
plt.ylabel("Frequency")

plt.subplot(2, 1, 2)
guesses_labels, guesses_values = zip(*sorted(((guess, guesses_data.count(guess)) for guess in set(guesses_data)), key=lambda x: x[1], reverse=True))

plt.bar(guesses_labels, guesses_values)
plt.title("Incorrect Guesses")
plt.xlabel("Letter")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha='right')

# Perform statistical analysis
guesses_mean = sum(guesses_values) / len(guesses_values)
guesses_median = guesses_values[len(guesses_values) // 2]
guesses_mode = max(guesses_values)

# Display statistical information
plt.text(0.05, 0.95, "Mean: {:.2f}".format(guesses_mean), transform=plt.gca().transAxes)
plt.text(0.05, 0.90, "Median: {}".format(guesses_median), transform=plt.gca().transAxes)
plt.text(0.05, 0.85, "Mode: {}".format(guesses_mode), transform=plt.gca().transAxes)

plt.show()