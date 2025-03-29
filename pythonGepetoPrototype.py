import requests
from time import sleep
import random
import json

with open('cuvinte.json') as file:
    data = json.load(file)

host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5
player_id = None


def previous_round(status, round_id, sys_word):
    if round_id == 1:
        return random.choice(data[20:41])["id"]

    p1_id = status.get("p1_id")
    p2_id = status.get("p2_id")
    player = 1 if player_id == p1_id else 2

    if player == 1:
        mycost = status["p1_word_cost"]
        mytotal = status["p1_total_cost"]
        enemycost = status["p2_word_cost"]
        enemytotal = status["p2_total_cost"]
        outcome = status["p1_won"]
    else:
        mycost = status["p2_word_cost"]
        mytotal = status["p2_total_cost"]
        enemycost = status["p1_word_cost"]
        enemytotal = status["p1_total_cost"]
        outcome = status["p2_won"]

    cost_diff = mytotal - enemytotal

    if outcome:
        target_cost = max(1, mycost - abs(cost_diff) // 2)
    else:
        if cost_diff < 0:
            target_cost = min(45, mycost + abs(cost_diff) // 2)
        else:
            target_cost = min(45, mycost + abs(cost_diff) // 3)

    best_word = min(data, key=lambda w: abs(w["cost"] - target_cost))
    return best_word["id"]


def what_beats(word, round_id, status):
    return previous_round(status, round_id, word)


def play_game(pid):
    global player_id
    player_id = pid

    for round_id in range(1, NUM_ROUNDS + 1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)
            print(response.json())
            sys_word = response.json()['word']
            round_num = response.json()['round']
            sleep(1)

        if round_id > 1:
            status_response = requests.get(status_url).json()
            status = status_response["status"]
            print(status)
        else:
            status = {}

        chosen_word = what_beats(sys_word, round_id, status)
        data_payload = {"player_id": player_id, "word_id": chosen_word, "round_id": round_id}
        response = requests.post(post_url, json=data_payload)
        print(response.json())
