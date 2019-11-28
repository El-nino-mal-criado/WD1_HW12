from random import randint
import json

def hello():
    print("Welcome to the game Guess a secret number!")
    name = input("Please, enter your name: ").strip().lower().title()
    surname = input("and your surname: ").strip().lower().title()
    print("Thank you! Now...")
    return name, surname

def good_bye():
    print("\nThank you for playing with us. Good bye!")

#function, where user selects the level of dificulty
def select_level():
    level = input(f"Please enter the level of difficulty (easy, medium, hard): ").strip().lower()
    max_num = 100
    if level == "easy":
        max_num = 10
    elif level == "hard":
        max_num = 1000
    return max_num, level

#function for one round of the game
def play_round(min_num = 1, max_num = 100):
    secret_number = randint(min_num, max_num)
    print(f"The computer has just generated the secret number, i.e. an integer between {min_num} and {max_num}. "
          f"Try to guess, which one it is.")
    correct = False
    score = []
    while not correct:
        guess = read_number(min_num, max_num) #user inserts one guess
        score.append(guess)
        if guess == secret_number:
            if len(score) == 1:
                print("Congratulations! You have guessed the secret number in the first trial.")
            else:
                print(f"Congratulations! You have guessed the secret number in {len(score)} trials.")
            correct = True
        elif guess > secret_number:
            print("Wrong! Your number is higher than the secret number. Keep on guessing.")
        else:
            print("Wrong! Your number is lower than the secret number. Keep on guessing.")
    return score

#function that reads users guesses
def read_number(min_num, max_num):
    entry = False
    while not entry:
        try:
            guess = int(input("Enter your guess: ").strip())
            if guess > max_num:
                print(f"ERROR: The entered value is grater than the upper limit ({guess} > {max_num}). Please retry!")
            elif guess < min_num:
                print(f"ERROR: The entered value is lower than the lower limit ({guess} < {min_num}). Please retry!")
            else:
                entry = True
        except ValueError:
            print("ERROR: The value you have entered is not an integer. Please retry!")

    return guess

#the main function of the program
def play():
    name, surname = hello() #calls function hello
    score_dictionary = {"easy": [], "medium": [], "hard": []}
    replay = True
    level_selection = True
    while replay:
        if level_selection:
            max_num, level = select_level() #asks user to select the level of the game
        score = play_round(max_num = max_num) #calls the function that plays a round of the game
        score_dictionary[level].append(score)
        answer_play = input("Would you like to play another round (yes/no)? ").strip().lower() #asks user to play another game and select another level
        if answer_play == "no":
            replay = False
        else:
            answer_level = input("Would you like to select another level of difficulty (yes/no)? ").strip().lower()
            level_selection = True
            if answer_level == "no":
                level_selection = False
    analyse_the_score(score_dictionary, name, surname) #reads the score file if it exists and appends the score of this game to the file
    good_bye() #bids user good bye

#this function reads the score file if it exists and appends the score of this game to the file
def analyse_the_score(score_dictionary, name, surname):
    try:
        with open(f"score_{name}_{surname}.txt", "r") as input_file:
            dictionary = json.loads(input_file.read())
            for level in dictionary:
                for i in range(len(score_dictionary[level])):
                    dictionary[level].append(score_dictionary[level][i])
    except FileNotFoundError:
        dictionary = score_dictionary
    with open(f"score_{name}_{surname}.txt", "w") as output_file:
        output_file.write(json.dumps(dictionary))
    print_score(score_dictionary, dictionary) #print current and total score

#function calculates current and total score
def print_score(score_dictionary, dictionary):
    print("\nYour score in this game:")
    for level in score_dictionary:
        print("Level:", level)
        print("    games played:", len(score_dictionary[level]))
        if len(score_dictionary[level]) != 0:
            print("    your best score:", min(len(x) for x in score_dictionary[level]), "guesses")
    print("\nYour total score:")
    for level in dictionary:
        print("Level:", level)
        print("    games played:", len(dictionary[level]))
        if len(dictionary[level]) != 0:
            print("    your best score:", min(len(x) for x in dictionary[level]), "guesses")

#starts playing the game
if __name__ == "__main__":
    play()
