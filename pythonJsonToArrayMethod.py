import requests
from time import sleep
import random
import json

with open('cuvinte.json') as file:
    data = json.load(file)

class Word:
    def __init__(self, id, name, cost):
        self.id = id
        self.name = name
        self.cost = cost

host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

idPrev = 0

words = [Word(id=int(id_str), name=entry["text"], cost=entry["cost"]) for id_str, entry in data.items()]

def what_beats(round_id, status, player_id, idPrev):
    if round_id == 1:
        return idPrev + 1

    outcome = status["p1_won"] if player_id == 1 else status["p2_won"]
    last_price = status["p1_word_cost"] if player_id == 1 else status["p2_word_cost"]
    total_price = status["p1_total_cost"] if player_id == 1 else status["p2_total_cost"]
    enemy_total_price = status["p2_total_cost"] if player_id == 1 else status["p1_total_cost"]
    total_diff = enemy_total_price - total_price

    if outcome:
        return max(1, idPrev - 2) if total_diff > 0 else max(1, idPrev - 4)
    else:
        return min(60, idPrev + 2) if total_diff > 0 else min(60, idPrev + 4)

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

        choosen_word = what_beats(round_id, status, player_id, idPrev)
        data = {"player_id": player_id, "word_id": choosen_word, "round_id": round_id}
        response = requests.post(post_url, json=data)
        idPrev = choosen_word
        print(response.json())

def main():
    pid = input("Enter your player ID: ").strip()
    if not pid:
        print("Player ID is required!")
        return
    play_game(pid)

if __name__ == "__main__":
    main()