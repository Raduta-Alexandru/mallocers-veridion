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
current_index = random.randint(20, 40)

def previous_round(status, round_id, sys_word):
    global current_index

    if round_id == 1:
        return random.randint(20, 40)

    # Determine which player we are
    p1_id = status["p1_id"]
    p2_id = status["p2_id"]
    player = 1 if player_id == p1_id else 2

    outcome = status["p1_won"] if player == 1 else status["p2_won"]

    if outcome:
        # We won → go a bit weaker (save strength)
        step = random.randint(3, 6)
        current_index = max(0, current_index - step)
    else:
        # We lost → go stronger
        step = random.randint(4, 8)
        current_index = min(len(data) - 1, current_index + step)

    return data[current_index]["id"]


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

def main():
    pid = input("Enter your player ID: ").strip()
    if not pid:
        print("Player ID is required!")
        return
    play_game(pid)

if __name__ == "__main__":
    main()