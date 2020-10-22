import random as rand
import requests
import csv


def choose_pokemon():
    pokemon_number = rand.randint(1, 500)
    url = 'https://pokeapi.co/api/v2/pokemon/{}/'.format(pokemon_number)
    response = requests.get(url)
    if response.status_code == 200:
        pokemon = response.json()
        return {
            'name': pokemon['name'],
            'id': pokemon['id'],
            'weight': pokemon['weight'],
            'height': pokemon['height'],
            'base experience': pokemon['base_experience'],
            'moves': len(pokemon['moves'])
        }


def play_round():
    global result
    players_pokemon = choose_pokemon()
    computer_pokemon = choose_pokemon()
    while players_pokemon == computer_pokemon:
        computer_pokemon = choose_pokemon()

    print("Your Pokemon's name is: {} \nPokedex number: {} \nWeight: {} \nHeight: {} \nBase Experience: {} \nMoves: {} ".format(
        players_pokemon["name"], players_pokemon["id"], players_pokemon["weight"], players_pokemon["height"],
        players_pokemon["base experience"], players_pokemon["moves"]))
    print()
    stat = input("Pick a stat - Pokedex number(1), height (2), weight(3), base experience (4) or moves (5): ")
    print()
    try:
        stat = int(stat)
        if stat in range(1, 6):
            if stat == 1:
                stat = "id"
            elif stat == 2:
                stat = "height"
            elif stat == 3:
                stat = "weight"
            elif stat == 4:
                stat = "base experience"
            else:
                stat = "moves"

            players_stat = players_pokemon[stat]
            computer_stat = computer_pokemon[stat]

            print("The opponents Pokemon is: {}".format(computer_pokemon["name"]))
            print()
            if players_stat > computer_stat:
                print("You WIN!! {} vs {} ".format(players_stat, computer_stat))
                result = 1
            elif players_stat < computer_stat:
                print("You LOSE!! {} vs {}".format(players_stat, computer_stat))
                result = 2
            else:
                print("It's a draw {} vs {}".format(players_stat, computer_stat))
                result = 3
        else:
            print("ERROR: stat incorrect")
            print("TRY AGAIN: Please choose a number between 1 and 5")
            play_round()
    except ValueError:
        print("ERROR: stat incorrect")
        print("TRY AGAIN: Please choose a number between 1 and 5")
        play_round()

user_count = 0
computer_count = 0
result = 0


def main():  # code to play multiple rounds in one go
    print("Welcome to Pokemon Top Trumps!")
    print()
    rounds = int(input('Please input number of rounds: '))
    count = 0
    history = [['Player', 'Computer']]
    global user_count, result, computer_count
    while count < rounds:
        count += 1
        play_round()
        if result == 1:
            user_count += 1
            history.append(['1', '0'])
        elif result == 2:
            computer_count += 1
            history.append(['0', '1'])
        else:
            computer_count += 1
            user_count += 1
            history.append(['1', '1'])
    print()
    print("Your score {} : Computer score {}".format(user_count, computer_count))
    history.append([str(user_count), str(computer_count)])
    if user_count > computer_count:
        print("You win!")
    elif user_count < computer_count:
        print("You lose!")
    else:
        print("It's a draw!")
    file = open('results.csv', 'w+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(history)
main()