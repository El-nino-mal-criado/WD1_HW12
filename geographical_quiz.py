from random import choice
import re
import json

#reads the file containig the data about countries and capitals and creates an internal dictionary {country:capital}
#based on the list of continents the user has entered
def create_dictionary(*continents):
    with open("country-capitals.json") as input_file:
        data = input_file.read()
    country_capitals_dictionary = json.loads(data)
    dictionary = {}
    for continent in continents:
        dictionary_continent = {item["CountryName"]: item["CapitalName"] for item in country_capitals_dictionary
                                if (item["ContinentName"] == continent and item["CapitalName"] != "N/A")}
        dictionary.update(dictionary_continent)
    return dictionary

#the function that plays the game
def play(number_of_attempts = 10, dictionary = {}):
    correct_guesses = 0
    for i in range(number_of_attempts):
        country_name, correct_capital = choice(list(dictionary.items())) #randomly chooses a country from the dictionary
        capital_name = input(f"What is the capital city of {country_name}: ")
        correctness = check_capital(country_name, correct_capital, capital_name) #checks whether user's input is correct
        if correctness:
            correct_guesses += 1
        del dictionary[country_name] #deletes the county from the dictionary, in order to avoid repetition of the same country
    return correct_guesses

#function checks the user's entry with the correct one
def check_capital(country_name, correct_capital, capital_name):
    correctness = False
    if(capital_name.strip().lower().title() == correct_capital):
        print("Correct!")
        correctness = True
    else:
        print(f"Wrong! The capital city of {country_name} is {correct_capital}.")
    return correctness

#function that evatuates user's score
def evaluation(correct_guesses, number_of_attempts):
    ratio = correct_guesses/number_of_attempts
    print("Your score is: ")
    print(f"{correct_guesses} / {number_of_attempts}")
    if ratio == 1.0:
        print("Congratulations! You have answered all the questions correctly. You are a genius!")
    elif ratio >= 0.9:
        print("Excellent! Your knowledge of geography is breathtaking!")
    elif ratio >= 0.7:
        print("Very good! Geography certainly is your cup of tea.")
    elif ratio >= 0.5:
        print("Good. You should be proud of your geographical knowledge.")
    elif ratio >= 0.25:
        print("Not bad! Many people do worse.")
    elif ratio > 0.0:
        print("Oh well, geography does not seem to be your cup of tea.")
    else:
        print("Oh well, do not worry! You will do better next time.")

def say_hello():
    print("Welcome to the Geographical Quiz!")
    print("The aim of this game is to correctly guess the capital cities of the desired number of countries or "
          "their overseas territories across the World.")

#level selection function
def select_level():
    level = input("Please select the level of difficulty (easy, hard): ").strip().lower()
    continents = []
    if(level == "easy"):
        continents = [x for x in re.split("[\s,]+", input("You have selected the easy level. Please, enter the names of"
                                                          " the continents, for which you wish to play the game "
                                                          "(Africa, America, Australia, Asia, Europe): ").strip().lower().title())]
        if "America" in continents:
            continents.remove("America")
            continents.extend(["North America", "South America", "Central America"])
    else:
        continents = ["North America", "South America", "Central America", "Africa", "Australia", "Asia", "Europe",
                      "Antarctica"]
    return continents

#asks user to enter the number of countries, whose capitals they would like to guess
def get_number_of_attempts():
    try:
        number_of_attempts = int(input("Please, enter the number of countries, whose capitals you would like to guess: "))
    except ValueError:
        number_of_attempts = 10
    return number_of_attempts


#here the program starts running
if __name__ == "__main__":
    say_hello()
    continents = select_level()
    dictionary = create_dictionary(*continents)
    number_of_attempts = get_number_of_attempts()
    print("Thank you! Now, let's play!")
    correct_guesses = play(number_of_attempts, dictionary)
    evaluation(correct_guesses, number_of_attempts)
    print("Thank you for playing the Geographical Quiz!")
