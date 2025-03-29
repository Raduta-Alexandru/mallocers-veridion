import requests
from time import sleep
import random
import json

host = "http://172.18.4.158:8000"
post_url = f"{host}/submit-word"
get_url = f"{host}/get-word"
status_url = f"{host}/status"

NUM_ROUNDS = 5

def updateAgresivity(low, high, status):
    playerNr = 1
    s = status.json()["status"]
    total_price = s['p1_total_cost'] if playerNr == 1 else s['p2_total_cost']
    enemy_total_price = s['p2_total_cost'] if playerNr == 1 else s['p1_total_cost']
    total_diff = enemy_total_price - total_price
    if total_diff > 0:
        high = min(60, high + 2)
        low = max(1, high - 20)
    else:
        high = max(20, high - 4)
        low = max(1, high - 20)
    return low, high


def what_beats(low, high):
    return random.randint(low, high)

def play_game(player_id):
    low = 20
    high = 40

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
            (low,high) = updateAgresivity(low, high, status)

        choosen_word = what_beats(low, high)
        data = {"player_id": player_id, "word_id": choosen_word, "round_id": round_id}
        response = requests.post(post_url, json=data)
        print(response.json())
        print(low, high)

def main():
    pid = "oJnREy4wVD"
    pid = "1"
    play_game(pid)

if __name__ == "__main__":
    main()