"""
# TODO:
    - Make work with more than 2 players
    - Make work with uneven teams
    - Make GUI a thing (command line ofc)
"""

import json

STARTING_ELO = 1000


def expected_score(playera: str, playerb: str):
    """
    Calculates the percentage chance that Player A has to win against Player B
    :param playera: The first player
    :param playerb: The second player
    :return: The chance that the first player has to win against Player B
    :raise IndexError: Either Player A or Player B is not in ranking.json
    """
    rb = STARTING_ELO
    ra = STARTING_ELO
    init_rankings = json.load(open("ranking.json"))
    try:
        ra = init_rankings[playera]
    except KeyError:
        data = json.load(open("ranking.json"))
        data.update({playera: STARTING_ELO})

        with open("ranking.json", "w") as fout:
            json.dump(data, fout, sort_keys=True, indent=4)
        expected_score(playera, playerb)
    try:
        rb = init_rankings[playerb]
    except KeyError:
        data = json.load(open("ranking.json"))
        data.update({playerb: STARTING_ELO})

        with open("ranking.json", "w") as fout:
            json.dump(data, fout, sort_keys=True, indent=4)
        expected_score(playera, playerb)

    return 1 / (1 + 10 ** ((rb - ra) / 400))


def expected_score_as_percent(playera: str, playerb: str):
    # return expected_score(playera, playerb) * 100
    return "{}% chance {} will win".format(round((expected_score(playera, playerb) * 100), 2), playera)


def add_game(playera: str, playerb: str, winner: int):
    """
    Adds a game to games.json
    :param playera: The first player
    :param playerb: The second player
    :param winner: The player that won
    :return: The new elo of both players
    """
    data = json.load(open("games.json"))
    if type(data) is dict:
        data = [data]

    outcome = [0] * 2
    if winner == 1:
        outcome[0] = 1
    else:
        outcome[1] = 1

    data.append({
        "Player A": {
            "Name": playera,
            "Outcome": outcome[0]
        },
        "Player B": {
            "Name": playerb,
            "Outcome": outcome[1]
        }
    })

    with open("games.json", "w") as fout:
        json.dump(data, fout, sort_keys=True, indent=4)

    update_rankings(playera, playerb, winner)


def update_rankings(playera: str, playerb: str, winner: int):
    """
    Updates elo values in ranking.json
    :param playera: The first player
    :param playerb: The second player
    :param winner: The player that won
    :return: N/A
    """
    outcome = [0] * 2
    if winner == 1:
        outcome[0] = 1
    else:
        outcome[1] = 1

    init_rankings = json.load(open("ranking.json"))
    expecteda = expected_score(playera, playerb)
    expectedb = expected_score(playerb, playera)
    try:
        olda = init_rankings[playera]
    except KeyError:
        olda = STARTING_ELO
    try:
        oldb = init_rankings[playerb]
    except KeyError:
        oldb = STARTING_ELO
    newa = round((olda + 32 * (outcome.pop(0) - expecteda)), 2)
    newb = round((oldb + 32 * (outcome.pop(0) - expectedb)), 2)

    data = json.load(open("ranking.json"))
    data[playera] = newa
    data[playerb] = newb

    with open("ranking.json", "w") as fout:
        json.dump(data, fout, sort_keys=True, indent=4)


def gui():
    pass


add_game("test1", "test2", 1)
