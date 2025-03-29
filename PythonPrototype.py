import requests
from time import sleep
import random
import json
with open('cuvinte.json') as file:
    data = json.load(file)

host = ""
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

def previous_round(status, round_id):
    #checking if there was a previous round
    if round_id == 1:
        return random.randint(20, 40)
    # determine if we are player 1 or 2
    player = 
    if player == 1:
        mycost = status["p1_word_cost"]
        mytotalcost = status["p1_total_cost"]
        outcome = status["p1_won"]
    else:
        mycost = status["p2_word_cost"]
        mytotalcost = status["p2_total_cost"]
        outcome = status["p2_won"]
    # seeing if we won or lost
    if outcome:
        #we won the previous round




def what_beats(word, round_id, status):
    
    return #the id of the word

def play_game(player_id):

    for round_id in range(1, NUM_ROUNDS+1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            print(response.json())
            sys_word = response.json()['word']
            round_num = response.json()['round']

            sleep(1)

        if round_id > 1:
            status = requests.get(status_url)
            print(status.json())

        choosen_word = what_beats(sys_word)
        data = {"player_id": player_id, "word_id": choosen_word, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())